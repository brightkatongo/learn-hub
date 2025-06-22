"use client"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { CURRENCIES } from "@/lib/currency"
import { Globe } from "lucide-react"

interface CurrencySelectorProps {
  selectedCurrency: string
  onCurrencyChange: (currency: string) => void
}

export function CurrencySelector({ selectedCurrency, onCurrencyChange }: CurrencySelectorProps) {
  const currentCurrency = CURRENCIES[selectedCurrency] || CURRENCIES.USD

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="sm" className="gap-2">
          <Globe className="h-4 w-4" />
          {currentCurrency.symbol} {currentCurrency.code}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {Object.entries(CURRENCIES).map(([code, currency]) => (
          <DropdownMenuItem
            key={code}
            onClick={() => onCurrencyChange(code)}
            className="flex items-center justify-between"
          >
            <span>
              {currency.symbol} {currency.code}
            </span>
            <span className="text-sm text-muted-foreground ml-2">{currency.name}</span>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
