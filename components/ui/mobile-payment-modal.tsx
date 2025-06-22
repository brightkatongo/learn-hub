"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Smartphone, Clock, CheckCircle, AlertCircle, Copy, Phone, RefreshCw } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface MobilePaymentModalProps {
  isOpen: boolean
  onClose: () => void
  course: {
    id: number
    title: string
    instructor: string
    price: number
    image: string
  }
  onPaymentSuccess: () => void
}

interface Provider {
  name: string
  display_name: string
  ussd_code: string
  phone_prefixes: string[]
  instructions: string
}

interface Transaction {
  id: string
  reference_code: string
  status: string
  expires_at: string
  amount: number
  currency: string
  provider_name: string
}

export function MobilePaymentModal({ isOpen, onClose, course, onPaymentSuccess }: MobilePaymentModalProps) {
  const [step, setStep] = useState<"provider" | "phone" | "instructions" | "status">("provider")
  const [selectedProvider, setSelectedProvider] = useState<string>("")
  const [phoneNumber, setPhoneNumber] = useState("")
  const [providers, setProviders] = useState<Provider[]>([])
  const [transaction, setTransaction] = useState<Transaction | null>(null)
  const [instructions, setInstructions] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [timeLeft, setTimeLeft] = useState(0)
  const { toast } = useToast()

  // Load providers on mount
  useEffect(() => {
    if (isOpen) {
      loadProviders()
    }
  }, [isOpen])

  // Timer for payment expiration
  useEffect(() => {
    if (transaction && transaction.expires_at) {
      const expiryTime = new Date(transaction.expires_at).getTime()
      const interval = setInterval(() => {
        const now = new Date().getTime()
        const remaining = Math.max(0, expiryTime - now)
        setTimeLeft(remaining)

        if (remaining === 0) {
          clearInterval(interval)
          checkPaymentStatus()
        }
      }, 1000)

      return () => clearInterval(interval)
    }
  }, [transaction])

  // Poll payment status
  useEffect(() => {
    if (step === "status" && transaction) {
      const interval = setInterval(() => {
        checkPaymentStatus()
      }, 10000) // Check every 10 seconds

      return () => clearInterval(interval)
    }
  }, [step, transaction])

  const loadProviders = async () => {
    try {
      const response = await fetch("/api/mobile-payments/providers/")
      const data = await response.json()
      setProviders(data)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load payment providers",
        variant: "destructive",
      })
    }
  }

  const validatePhoneNumber = async (phone: string) => {
    try {
      const response = await fetch("/api/mobile-payments/validate-phone/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone_number: phone }),
      })
      const data = await response.json()
      return data
    } catch (error) {
      return { is_valid: false, error: "Validation failed" }
    }
  }

  const initiatePayment = async () => {
    setIsLoading(true)

    try {
      const response = await fetch("/api/mobile-payments/initiate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          course_id: course.id,
          provider: selectedProvider,
          phone_number: phoneNumber,
        }),
      })

      const data = await response.json()

      if (response.ok) {
        setTransaction(data.transaction)
        setInstructions(data.instructions)
        setStep("instructions")
        toast({
          title: "Payment Initiated",
          description: "Follow the instructions to complete your payment",
        })
      } else {
        throw new Error(data.error || "Payment initiation failed")
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Payment initiation failed",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const checkPaymentStatus = async () => {
    if (!transaction) return

    try {
      const response = await fetch(`/api/mobile-payments/status/${transaction.reference_code}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      })
      const data = await response.json()

      if (data.status === "confirmed") {
        onPaymentSuccess()
        onClose()
        toast({
          title: "Payment Successful!",
          description: "You now have access to the course",
        })
      } else if (data.status === "failed" || data.status === "expired") {
        toast({
          title: "Payment Failed",
          description: "Please try again or contact support",
          variant: "destructive",
        })
      }

      setTransaction((prev) => (prev ? { ...prev, status: data.status } : null))
    } catch (error) {
      console.error("Status check failed:", error)
    }
  }

  const handleProviderNext = () => {
    if (!selectedProvider) {
      toast({
        title: "Select Provider",
        description: "Please select a mobile money provider",
        variant: "destructive",
      })
      return
    }
    setStep("phone")
  }

  const handlePhoneNext = async () => {
    if (!phoneNumber) {
      toast({
        title: "Enter Phone Number",
        description: "Please enter your phone number",
        variant: "destructive",
      })
      return
    }

    const validation = await validatePhoneNumber(phoneNumber)
    if (!validation.is_valid) {
      toast({
        title: "Invalid Phone Number",
        description: "Please enter a valid Zambian phone number",
        variant: "destructive",
      })
      return
    }

    if (validation.detected_provider !== selectedProvider) {
      toast({
        title: "Provider Mismatch",
        description: `This number belongs to ${validation.detected_provider}, not ${selectedProvider}`,
        variant: "destructive",
      })
      return
    }

    await initiatePayment()
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast({
      title: "Copied!",
      description: "Copied to clipboard",
    })
  }

  const formatTime = (milliseconds: number) => {
    const minutes = Math.floor(milliseconds / 60000)
    const seconds = Math.floor((milliseconds % 60000) / 1000)
    return `${minutes}:${seconds.toString().padStart(2, "0")}`
  }

  const getProviderIcon = (providerName: string) => {
    const icons: Record<string, string> = {
      airtel: "🔴",
      zamtel: "🟢",
      mtn: "🟡",
    }
    return icons[providerName] || "📱"
  }

  const resetModal = () => {
    setStep("provider")
    setSelectedProvider("")
    setPhoneNumber("")
    setTransaction(null)
    setInstructions(null)
    setTimeLeft(0)
  }

  const handleClose = () => {
    resetModal()
    onClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Smartphone className="h-5 w-5 text-blue-600" />
            Mobile Money Payment
          </DialogTitle>
          <DialogDescription>Pay for {course.title} using mobile money</DialogDescription>
        </DialogHeader>

        {/* Progress Indicator */}
        <div className="flex items-center justify-between mb-6">
          {["provider", "phone", "instructions", "status"].map((stepName, index) => (
            <div key={stepName} className="flex items-center">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  step === stepName
                    ? "bg-blue-600 text-white"
                    : ["provider", "phone", "instructions", "status"].indexOf(step) > index
                      ? "bg-green-600 text-white"
                      : "bg-gray-200"
                }`}
              >
                {["provider", "phone", "instructions", "status"].indexOf(step) > index ? (
                  <CheckCircle className="h-4 w-4" />
                ) : (
                  index + 1
                )}
              </div>
              {index < 3 && <div className="w-12 h-0.5 bg-gray-200 mx-2" />}
            </div>
          ))}
        </div>

        {/* Step 1: Provider Selection */}
        {step === "provider" && (
          <div className="space-y-6">
            <div>
              <Label className="text-base font-semibold mb-4 block">Choose Your Mobile Money Provider</Label>
              <RadioGroup value={selectedProvider} onValueChange={setSelectedProvider}>
                <div className="grid gap-3">
                  {providers.map((provider) => (
                    <div
                      key={provider.name}
                      className="flex items-center space-x-3 border rounded-lg p-4 hover:bg-muted/50 transition-colors"
                    >
                      <RadioGroupItem value={provider.name} id={provider.name} />
                      <div className="flex items-center gap-3 flex-1">
                        <div className="text-2xl">{getProviderIcon(provider.name)}</div>
                        <div className="flex-1">
                          <Label htmlFor={provider.name} className="font-medium cursor-pointer">
                            {provider.display_name}
                          </Label>
                          <p className="text-sm text-muted-foreground">
                            USSD: {provider.ussd_code} • Prefixes: {provider.phone_prefixes.join(", ")}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </RadioGroup>
            </div>

            <div className="flex gap-3">
              <Button variant="outline" onClick={handleClose} className="flex-1">
                Cancel
              </Button>
              <Button onClick={handleProviderNext} className="flex-1">
                Next
              </Button>
            </div>
          </div>
        )}

        {/* Step 2: Phone Number */}
        {step === "phone" && (
          <div className="space-y-6">
            <div>
              <Label className="text-base font-semibold mb-4 block">Enter Your Phone Number</Label>
              <div className="space-y-2">
                <Input
                  placeholder="e.g., 097 123 4567"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  className="text-lg"
                />
                <p className="text-sm text-muted-foreground">
                  Enter your {providers.find((p) => p.name === selectedProvider)?.display_name} number
                </p>
              </div>
            </div>

            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                Make sure you have sufficient balance and your phone is nearby to complete the payment.
              </AlertDescription>
            </Alert>

            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setStep("provider")} className="flex-1">
                Back
              </Button>
              <Button onClick={handlePhoneNext} disabled={isLoading} className="flex-1">
                {isLoading ? "Processing..." : "Continue"}
              </Button>
            </div>
          </div>
        )}

        {/* Step 3: Payment Instructions */}
        {step === "instructions" && transaction && instructions && (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Follow These Steps</h3>
              <p className="text-muted-foreground">Complete your payment within {formatTime(timeLeft)}</p>
              <Progress value={(timeLeft / (30 * 60 * 1000)) * 100} className="mt-2" />
            </div>

            <div className="bg-muted/50 p-4 rounded-lg">
              <div className="flex items-center justify-between mb-3">
                <span className="font-medium">Reference Code:</span>
                <div className="flex items-center gap-2">
                  <code className="bg-white px-2 py-1 rounded text-lg font-mono">{transaction.reference_code}</code>
                  <Button size="sm" variant="outline" onClick={() => copyToClipboard(transaction.reference_code)}>
                    <Copy className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="font-medium">Amount:</span>
                <span className="text-lg font-bold">
                  {transaction.amount} {transaction.currency}
                </span>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="font-medium">Step-by-step instructions:</h4>
              <ol className="space-y-2">
                {instructions.steps?.map((step: string, index: number) => (
                  <li key={index} className="flex items-start gap-3">
                    <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-medium flex-shrink-0">
                      {index + 1}
                    </span>
                    <span className="text-sm">{step}</span>
                  </li>
                ))}
              </ol>
            </div>

            <div className="flex gap-3">
              <Button variant="outline" onClick={() => window.open(`tel:${instructions.ussd_code}`)} className="flex-1">
                <Phone className="mr-2 h-4 w-4" />
                Dial {instructions.ussd_code}
              </Button>
              <Button onClick={() => setStep("status")} className="flex-1">
                I've Made Payment
              </Button>
            </div>
          </div>
        )}

        {/* Step 4: Payment Status */}
        {step === "status" && transaction && (
          <div className="space-y-6 text-center">
            <div>
              {transaction.status === "pending" && (
                <>
                  <div className="w-16 h-16 mx-auto mb-4 bg-yellow-100 rounded-full flex items-center justify-center">
                    <Clock className="h-8 w-8 text-yellow-600" />
                  </div>
                  <h3 className="text-lg font-semibold mb-2">Waiting for Confirmation</h3>
                  <p className="text-muted-foreground">
                    We're waiting for payment confirmation. This usually takes 1-2 minutes.
                  </p>
                </>
              )}

              {transaction.status === "confirmed" && (
                <>
                  <div className="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
                    <CheckCircle className="h-8 w-8 text-green-600" />
                  </div>
                  <h3 className="text-lg font-semibold mb-2">Payment Successful!</h3>
                  <p className="text-muted-foreground">
                    Your payment has been confirmed. You now have access to the course.
                  </p>
                </>
              )}

              {(transaction.status === "failed" || transaction.status === "expired") && (
                <>
                  <div className="w-16 h-16 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center">
                    <AlertCircle className="h-8 w-8 text-red-600" />
                  </div>
                  <h3 className="text-lg font-semibold mb-2">Payment Failed</h3>
                  <p className="text-muted-foreground">Your payment could not be processed. Please try again.</p>
                </>
              )}
            </div>

            <div className="bg-muted/50 p-4 rounded-lg">
              <div className="text-sm space-y-1">
                <div className="flex justify-between">
                  <span>Reference:</span>
                  <span className="font-mono">{transaction.reference_code}</span>
                </div>
                <div className="flex justify-between">
                  <span>Status:</span>
                  <Badge variant={transaction.status === "confirmed" ? "default" : "secondary"}>
                    {transaction.status}
                  </Badge>
                </div>
                <div className="flex justify-between">
                  <span>Amount:</span>
                  <span>
                    {transaction.amount} {transaction.currency}
                  </span>
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              {transaction.status === "pending" && (
                <>
                  <Button variant="outline" onClick={checkPaymentStatus} className="flex-1">
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Check Status
                  </Button>
                  <Button variant="outline" onClick={handleClose} className="flex-1">
                    Close
                  </Button>
                </>
              )}

              {transaction.status === "confirmed" && (
                <Button onClick={handleClose} className="flex-1">
                  Continue to Course
                </Button>
              )}

              {(transaction.status === "failed" || transaction.status === "expired") && (
                <>
                  <Button variant="outline" onClick={resetModal} className="flex-1">
                    Try Again
                  </Button>
                  <Button variant="outline" onClick={handleClose} className="flex-1">
                    Close
                  </Button>
                </>
              )}
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  )
}
