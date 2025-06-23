export interface PaymentMethod {
  id: string
  name: string
  type: 'card' | 'mobile_money' | 'bank_transfer'
  description: string
  icon: string
  countries: string[]
  currencies: string[]
}

export const PAYMENT_METHODS: PaymentMethod[] = [
  {
    id: 'stripe_card',
    name: 'Credit/Debit Card',
    type: 'card',
    description: 'Pay securely with your credit or debit card',
    icon: '💳',
    countries: ['US', 'GB', 'ZA', 'KE', 'NG'],
    currencies: ['USD', 'ZAR', 'KES', 'NGN']
  },
  {
    id: 'airtel_money',
    name: 'Airtel Money',
    type: 'mobile_money',
    description: 'Pay with Airtel Money mobile wallet',
    icon: '📱',
    countries: ['ZM', 'ZA', 'KE', 'UG', 'TZ'],
    currencies: ['ZMW', 'ZAR', 'KES', 'UGX', 'TZS']
  },
  {
    id: 'mtn_money',
    name: 'MTN Money',
    type: 'mobile_money',
    description: 'Pay with MTN Mobile Money',
    icon: '📲',
    countries: ['ZM', 'GH', 'UG', 'RW', 'CI'],
    currencies: ['ZMW', 'GHS', 'UGX', 'RWF', 'XOF']
  },
  {
    id: 'zamtel_money',
    name: 'Zamtel Money',
    type: 'mobile_money',
    description: 'Pay with Zamtel Money',
    icon: '💰',
    countries: ['ZM'],
    currencies: ['ZMW']
  },
  {
    id: 'mpesa',
    name: 'M-Pesa',
    type: 'mobile_money',
    description: 'Pay with M-Pesa mobile money',
    icon: '💸',
    countries: ['KE', 'TZ', 'MZ'],
    currencies: ['KES', 'TZS', 'MZN']
  },
  {
    id: 'bank_transfer',
    name: 'Bank Transfer',
    type: 'bank_transfer',
    description: 'Direct bank transfer',
    icon: '🏦',
    countries: ['ZM', 'ZA', 'KE', 'NG', 'GH'],
    currencies: ['ZMW', 'ZAR', 'KES', 'NGN', 'GHS']
  }
]

export function detectUserCountry(): string {
  if (typeof window === 'undefined') return 'US'
  
  // Try to detect from browser locale
  const locale = navigator.language || 'en-US'
  const region = locale.split('-')[1]
  
  return region || 'US'
}

export function getAvailablePaymentMethods(country: string): PaymentMethod[] {
  return PAYMENT_METHODS.filter(method => 
    method.countries.includes(country) || method.countries.includes('US')
  )
}

export function getPaymentMethodsByType(type: PaymentMethod['type'], country?: string): PaymentMethod[] {
  let methods = PAYMENT_METHODS.filter(method => method.type === type)
  
  if (country) {
    methods = methods.filter(method => method.countries.includes(country))
  }
  
  return methods
}

export function isPaymentMethodAvailable(methodId: string, country: string, currency: string): boolean {
  const method = PAYMENT_METHODS.find(m => m.id === methodId)
  if (!method) return false
  
  return method.countries.includes(country) && method.currencies.includes(currency)
}