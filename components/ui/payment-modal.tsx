"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { getAvailablePaymentMethods, detectUserCountry, type PaymentMethod } from "@/lib/payments"
import { formatPrice } from "@/lib/currency"
import { CreditCard, Smartphone, Building, Shield, CheckCircle } from "lucide-react"

interface PaymentModalProps {
  isOpen: boolean
  onClose: () => void
  course: {
    id: number
    title: string
    instructor: string
    price: number
    image: string
  }
  currency: string
  onPaymentSuccess: () => void
}

export function PaymentModal({ isOpen, onClose, course, currency, onPaymentSuccess }: PaymentModalProps) {
  const [selectedMethod, setSelectedMethod] = useState<string>("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [phoneNumber, setPhoneNumber] = useState("")
  const [cardDetails, setCardDetails] = useState({
    number: "",
    expiry: "",
    cvv: "",
    name: "",
  })

  const userCountry = detectUserCountry()
  const availablePaymentMethods = getAvailablePaymentMethods(userCountry)

  const getMethodIcon = (type: PaymentMethod["type"]) => {
    switch (type) {
      case "card":
        return <CreditCard className="h-5 w-5" />
      case "mobile_money":
        return <Smartphone className="h-5 w-5" />
      case "bank_transfer":
        return <Building className="h-5 w-5" />
      default:
        return <CreditCard className="h-5 w-5" />
    }
  }

  const handlePayment = async () => {
    setIsProcessing(true)

    // Simulate payment processing
    await new Promise((resolve) => setTimeout(resolve, 2000))

    setIsProcessing(false)
    onPaymentSuccess()
    onClose()
  }

  const selectedPaymentMethod = availablePaymentMethods.find((method) => method.id === selectedMethod)

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-green-600" />
            Secure Payment
          </DialogTitle>
          <DialogDescription>Complete your enrollment for this course</DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Course Summary */}
          <div className="flex items-center gap-4 p-4 bg-muted/50 rounded-lg">
            <img
              src={course.image || "/placeholder.svg"}
              alt={course.title}
              className="w-16 h-16 rounded-lg object-cover"
            />
            <div className="flex-1">
              <h3 className="font-semibold line-clamp-1">{course.title}</h3>
              <p className="text-sm text-muted-foreground">by {course.instructor}</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-primary">{formatPrice(course.price, currency)}</div>
              <Badge variant="secondary" className="text-xs">
                One-time payment
              </Badge>
            </div>
          </div>

          {/* Payment Methods */}
          <div>
            <Label className="text-base font-semibold mb-4 block">Choose Payment Method</Label>
            <RadioGroup value={selectedMethod} onValueChange={setSelectedMethod}>
              <div className="grid gap-3">
                {availablePaymentMethods.map((method) => (
                  <div
                    key={method.id}
                    className="flex items-center space-x-3 border rounded-lg p-4 hover:bg-muted/50 transition-colors"
                  >
                    <RadioGroupItem value={method.id} id={method.id} />
                    <div className="flex items-center gap-3 flex-1">
                      {getMethodIcon(method.type)}
                      <div className="flex-1">
                        <Label htmlFor={method.id} className="font-medium cursor-pointer">
                          {method.name}
                        </Label>
                        <p className="text-sm text-muted-foreground">{method.description}</p>
                      </div>
                      <span className="text-2xl">{method.icon}</span>
                    </div>
                  </div>
                ))}
              </div>
            </RadioGroup>
          </div>

          {/* Payment Details Form */}
          {selectedPaymentMethod && (
            <>
              <Separator />
              <div className="space-y-4">
                <Label className="text-base font-semibold">Payment Details</Label>

                {selectedPaymentMethod.type === "mobile_money" && (
                  <div className="space-y-2">
                    <Label htmlFor="phone">Mobile Number</Label>
                    <Input
                      id="phone"
                      placeholder="e.g., +260 97 123 4567"
                      value={phoneNumber}
                      onChange={(e) => setPhoneNumber(e.target.value)}
                    />
                    <p className="text-sm text-muted-foreground">
                      You will receive a prompt on your phone to complete the payment
                    </p>
                  </div>
                )}

                {selectedPaymentMethod.type === "card" && (
                  <div className="grid gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="cardName">Cardholder Name</Label>
                      <Input
                        id="cardName"
                        placeholder="John Doe"
                        value={cardDetails.name}
                        onChange={(e) => setCardDetails((prev) => ({ ...prev, name: e.target.value }))}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="cardNumber">Card Number</Label>
                      <Input
                        id="cardNumber"
                        placeholder="1234 5678 9012 3456"
                        value={cardDetails.number}
                        onChange={(e) => setCardDetails((prev) => ({ ...prev, number: e.target.value }))}
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="expiry">Expiry Date</Label>
                        <Input
                          id="expiry"
                          placeholder="MM/YY"
                          value={cardDetails.expiry}
                          onChange={(e) => setCardDetails((prev) => ({ ...prev, expiry: e.target.value }))}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="cvv">CVV</Label>
                        <Input
                          id="cvv"
                          placeholder="123"
                          value={cardDetails.cvv}
                          onChange={(e) => setCardDetails((prev) => ({ ...prev, cvv: e.target.value }))}
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}

          {/* Security Notice */}
          <div className="flex items-start gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
            <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
            <div className="text-sm">
              <p className="font-medium text-green-800">Secure Payment</p>
              <p className="text-green-700">
                Your payment information is encrypted and secure. We never store your payment details.
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <Button variant="outline" onClick={onClose} className="flex-1">
              Cancel
            </Button>
            <Button onClick={handlePayment} disabled={!selectedMethod || isProcessing} className="flex-1">
              {isProcessing ? "Processing..." : `Pay ${formatPrice(course.price, currency)}`}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
