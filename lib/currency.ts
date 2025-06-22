export interface CurrencyConfig {
  code: string
  symbol: string
  name: string
  exchangeRate: number // Rate to USD
}

export const CURRENCIES: Record<string, CurrencyConfig> = {
  USD: {
    code: "USD",
    symbol: "$",
    name: "US Dollar",
    exchangeRate: 1,
  },
  ZMW: {
    code: "ZMW",
    symbol: "K",
    name: "Zambian Kwacha",
    exchangeRate: 0.037, // Approximate rate - should be fetched from API
  },
  ZAR: {
    code: "ZAR",
    symbol: "R",
    name: "South African Rand",
    exchangeRate: 0.055,
  },
  KES: {
    code: "KES",
    symbol: "KSh",
    name: "Kenyan Shilling",
    exchangeRate: 0.0077,
  },
  NGN: {
    code: "NGN",
    symbol: "₦",
    name: "Nigerian Naira",
    exchangeRate: 0.0012,
  },
}

export function detectUserCurrency(): string {
  if (typeof window === "undefined") return "USD"

  // Try to detect from browser locale
  const locale = navigator.language || "en-US"
  const region = locale.split("-")[1]

  const regionToCurrency: Record<string, string> = {
    ZM: "ZMW", // Zambia
    ZA: "ZAR", // South Africa
    KE: "KES", // Kenya
    NG: "NGN", // Nigeria
    US: "USD",
    GB: "USD", // Default to USD for international
  }

  return regionToCurrency[region] || "USD"
}

export function formatPrice(amount: number, currencyCode = "USD"): string {
  const currency = CURRENCIES[currencyCode] || CURRENCIES.USD
  const convertedAmount = amount / currency.exchangeRate

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency.code,
    minimumFractionDigits: currency.code === "ZMW" ? 0 : 2,
  }).format(convertedAmount)
}

export function convertPrice(amount: number, fromCurrency: string, toCurrency: string): number {
  const from = CURRENCIES[fromCurrency] || CURRENCIES.USD
  const to = CURRENCIES[toCurrency] || CURRENCIES.USD

  // Convert to USD first, then to target currency
  const usdAmount = amount * from.exchangeRate
  return usdAmount / to.exchangeRate
}
