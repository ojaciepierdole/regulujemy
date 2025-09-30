#!/usr/bin/env python3
"""
Diagnostyka problemu z blokami w Payload CMS
"""

import requests
import json

# Konfiguracja API
PAYLOAD_URL = "http://localhost:3000"  # Dostosuj do swojego URL
API_KEY = "YOUR_API_KEY"  # Jeśli wymagany

def check_blocks_availability():
    """Sprawdź dostępność bloków w konfiguracji"""
    
    print("🔍 DIAGNOSTYKA BLOKÓW W PAYLOAD CMS")
    print("=" * 50)
    
    # Lista oczekiwanych bloków
    expected_blocks = [
        "cta-block",
        "pricing-block", 
        "faq-block",
        "gallery-block",
        "testimonial-block",
        "service-card-block",
        "location-block",
        "content-block",
        "hero-block"
    ]
    
    print("\n📋 OCZEKIWANE BLOKI:")
    for block in expected_blocks:
        print(f"  - {block}")
    
    print("\n⚠️  MOŻLIWE PRZYCZYNY PROBLEMU:")
    print("""
    1. Bloki nie są zarejestrowane w konfiguracji Payload
    2. Brak importu bloków w payload.config.ts
    3. Nieprawidłowa konfiguracja pola 'blocks' w kolekcji
    4. Problem z typami TypeScript
    5. Błąd w definicji bloków
    """)
    
    print("\n🔧 ROZWIĄZANIE KROK PO KROKU:\n")
    
    print("1. SPRAWDŹ payload.config.ts:")
    print("""
```typescript
import { buildConfig } from 'payload/config';
import { CTABlock } from './blocks/CTABlock';
import { PricingBlock } from './blocks/PricingBlock';
import { FAQBlock } from './blocks/FAQBlock';
// ... importuj pozostałe bloki

export default buildConfig({
  // ... inne konfiguracje
});
```
    """)
    
    print("2. SPRAWDŹ DEFINICJĘ BLOKÓW:")
    print("""
```typescript
// blocks/CTABlock.ts
import { Block } from 'payload/types';

export const CTABlock: Block = {
  slug: 'cta-block',
  labels: {
    singular: 'CTA Block',
    plural: 'CTA Blocks',
  },
  fields: [
    {
      name: 'heading',
      type: 'text',
      required: true,
    },
    // ... pozostałe pola
  ],
};
```
    """)
    
    print("3. SPRAWDŹ KONFIGURACJĘ KOLEKCJI:")
    print("""
```typescript
// collections/Services.ts lub Pages.ts
{
  name: 'content',
  type: 'blocks',
  blocks: [
    CTABlock,
    PricingBlock,
    FAQBlock,
    // ... pozostałe bloki
  ],
}
```
    """)
    
    print("\n4. SPRAWDŹ KONSOLĘ PRZEGLĄDARKI:")
    print("   - Otwórz konsole deweloperską (F12)")
    print("   - Sprawdź błędy JavaScript")
    print("   - Sprawdź Network tab czy bloki są ładowane")
    
    print("\n5. RESTART PAYLOAD CMS:")
    print("   - Zatrzymaj serwer (Ctrl+C)")
    print("   - Wyczyść cache: rm -rf .next")
    print("   - Uruchom ponownie: npm run dev")

if __name__ == "__main__":
    check_blocks_availability()