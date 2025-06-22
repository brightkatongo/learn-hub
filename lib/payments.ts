export interface PaymentMethod {
  id: string
  name: string
  type: "card" | "mobile_money" | "bank_transfer"
  countries: string[]
  icon: string
  description: string
}

export const PAYMENT_METHODS: PaymentMethod[] = [
  {
    id: "stripe",
    name: "Credit/Debit Card",
    type: "card",
    countries: ["*"], // Available globally
    icon: "💳",
    description: "Visa, Mastercard, American Express",
  },
  {
    id: "mtn_momo",
    name: "MTN Mobile Money",
    type: "mobile_money",
    countries: ["ZM", "UG", "GH", "CI", "CM", "BJ", "RW"],
    icon: "📱",
    description: "Pay with MTN Mobile Money",
  },
  {
    id: "airtel_money",
    name: "Airtel Money",
    type: "mobile_money",
    countries: ["ZM", "KE", "TZ", "UG", "RW", "MW", "MG", "TD", "NE"],
    icon: "📱",
    description: "Pay with Airtel Money",
  },
  {
    id: "zamtel_kwacha",
    name: "Zamtel Kwacha",
    type: "mobile_money",
    countries: ["ZM"],
    icon: "📱",
    description: "Pay with Zamtel Kwacha",
  },
  {
    id: "paypal",
    name: "PayPal",
    type: "card",
    countries: ["*"],
    icon: "🅿️",
    description: "Pay with PayPal account",
  },
]

export function getAvailablePaymentMethods(countryCode: string): PaymentMethod[] {
  return PAYMENT_METHODS.filter((method) => method.countries.includes("*") || method.countries.includes(countryCode))
}

export function detectUserCountry(): string {
  if (typeof window === "undefined") return "US"

  const locale = navigator.language || "en-US"
  const region = locale.split("-")[1]

  return region || "US"
}
