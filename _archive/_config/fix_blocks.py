#!/usr/bin/env python3
"""
Skrypt naprawczy - przywraca bloki w Payload CMS
"""

import os
from pathlib import Path

def create_block_definitions():
    """Tworzy definicje bloków dla Payload CMS"""
    
    project_root = Path("/Users/tomek/Documents/Kamyki/01_ACTIVE/Projects/regulujemy-pl")
    blocks_dir = project_root / "_config" / "payload" / "blocks"
    blocks_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔧 TWORZENIE DEFINICJI BLOKÓW DLA PAYLOAD CMS")
    print("=" * 50)
    
    # CTA Block
    cta_block = """import { Block } from 'payload/types';

export const CTABlock: Block = {
  slug: 'cta-block',
  labels: {
    singular: 'Blok CTA',
    plural: 'Bloki CTA',
  },
  fields: [
    {
      name: 'heading',
      type: 'text',
      label: 'Nagłówek',
      required: true,
    },
    {
      name: 'description',
      type: 'textarea',
      label: 'Opis',
    },
    {
      name: 'style',
      type: 'select',
      label: 'Styl',
      defaultValue: 'standard',
      options: [
        { label: 'Standardowy', value: 'standard' },
        { label: 'Awaryjny', value: 'emergency' },
        { label: 'Promocja', value: 'promotion' },
      ],
    },
    {
      name: 'buttons',
      type: 'array',
      label: 'Przyciski',
      maxRows: 3,
      fields: [
        {
          name: 'text',
          type: 'text',
          label: 'Tekst przycisku',
          required: true,
        },
        {
          name: 'link',
          type: 'text',
          label: 'Link',
        },
        {
          name: 'style',
          type: 'select',
          label: 'Styl przycisku',
          options: [
            { label: 'Główny', value: 'primary' },
            { label: 'Dodatkowy', value: 'secondary' },
            { label: 'Telefon', value: 'phone' },
            { label: 'WhatsApp', value: 'whatsapp' },
          ],
        },
      ],
    },
  ],
};
"""
    
    # Pricing Block
    pricing_block = """import { Block } from 'payload/types';

export const PricingBlock: Block = {
  slug: 'pricing-block',
  labels: {
    singular: 'Blok Cennik',
    plural: 'Bloki Cennik',
  },
  fields: [
    {
      name: 'title',
      type: 'text',
      label: 'Tytuł',
      defaultValue: 'Cennik',
    },
    {
      name: 'description',
      type: 'textarea',
      label: 'Opis',
    },
    {
      name: 'pricingItems',
      type: 'array',
      label: 'Pozycje cennika',
      fields: [
        {
          name: 'service',
          type: 'text',
          label: 'Usługa',
          required: true,
        },
        {
          name: 'price',
          type: 'text',
          label: 'Cena',
          required: true,
        },
        {
          name: 'unit',
          type: 'text',
          label: 'Jednostka',
          defaultValue: 'usługa',
        },
        {
          name: 'duration',
          type: 'text',
          label: 'Czas realizacji',
        },
        {
          name: 'highlighted',
          type: 'checkbox',
          label: 'Wyróżniony',
          defaultValue: false,
        },
      ],
    },
    {
      name: 'displayType',
      type: 'select',
      label: 'Sposób wyświetlania',
      defaultValue: 'table',
      options: [
        { label: 'Tabela', value: 'table' },
        { label: 'Karty', value: 'cards' },
        { label: 'Lista', value: 'list' },
      ],
    },
  ],
};
"""
    
    # FAQ Block
    faq_block = """import { Block } from 'payload/types';

export const FAQBlock: Block = {
  slug: 'faq-block',
  labels: {
    singular: 'Blok FAQ',
    plural: 'Bloki FAQ',
  },
  fields: [
    {
      name: 'title',
      type: 'text',
      label: 'Tytuł',
      defaultValue: 'Najczęściej Zadawane Pytania',
    },
    {
      name: 'faqs',
      type: 'array',
      label: 'Pytania i odpowiedzi',
      fields: [
        {
          name: 'question',
          type: 'text',
          label: 'Pytanie',
          required: true,
        },
        {
          name: 'answer',
          type: 'richText',
          label: 'Odpowiedź',
          required: true,
        },
      ],
    },
    {
      name: 'displayType',
      type: 'select',
      label: 'Sposób wyświetlania',
      defaultValue: 'accordion',
      options: [
        { label: 'Accordion', value: 'accordion' },
        { label: 'Lista', value: 'list' },
        { label: 'Karty', value: 'cards' },
      ],
    },
  ],
};
"""
    # Gallery Block
    gallery_block = """import { Block } from 'payload/types';

export const GalleryBlock: Block = {
  slug: 'gallery-block',
  labels: {
    singular: 'Blok Galeria',
    plural: 'Bloki Galeria',
  },
  fields: [
    {
      name: 'title',
      type: 'text',
      label: 'Tytuł',
    },
    {
      name: 'images',
      type: 'array',
      label: 'Zdjęcia',
      fields: [
        {
          name: 'image',
          type: 'upload',
          relationTo: 'media',
          label: 'Zdjęcie',
          required: true,
        },
        {
          name: 'caption',
          type: 'text',
          label: 'Podpis',
        },
      ],
    },
    {
      name: 'displayType',
      type: 'select',
      label: 'Sposób wyświetlania',
      defaultValue: 'grid',
      options: [
        { label: 'Siatka', value: 'grid' },
        { label: 'Masonry', value: 'masonry' },
        { label: 'Karuzela', value: 'carousel' },
        { label: 'Lightbox', value: 'lightbox' },
      ],
    },
    {
      name: 'columns',
      type: 'number',
      label: 'Liczba kolumn',
      min: 2,
      max: 6,
      defaultValue: 4,
    },
  ],
};
"""

    # Testimonial Block
    testimonial_block = """import { Block } from 'payload/types';

export const TestimonialBlock: Block = {
  slug: 'testimonial-block',
  labels: {
    singular: 'Blok Opinie',
    plural: 'Bloki Opinie',
  },
  fields: [
    {
      name: 'title',
      type: 'text',
      label: 'Tytuł',
      defaultValue: 'Opinie Klientów',
    },
    {
      name: 'testimonials',
      type: 'array',
      label: 'Opinie',
      fields: [
        {
          name: 'content',
          type: 'textarea',
          label: 'Treść opinii',
          required: true,
        },
        {
          name: 'author',
          type: 'text',
          label: 'Autor',
          required: true,
        },
        {
          name: 'location',
          type: 'text',
          label: 'Lokalizacja',
        },
        {
          name: 'rating',
          type: 'number',
          label: 'Ocena',
          min: 1,
          max: 5,
          defaultValue: 5,
        },
      ],
    },
    {
      name: 'displayType',
      type: 'select',
      label: 'Sposób wyświetlania',
      defaultValue: 'carousel',
      options: [
        { label: 'Karuzela', value: 'carousel' },
        { label: 'Siatka', value: 'grid' },
        { label: 'Lista', value: 'list' },
      ],
    },
  ],
};
"""

    # Zapisz bloki
    blocks = [
        ('CTABlock.ts', cta_block),
        ('PricingBlock.ts', pricing_block),
        ('FAQBlock.ts', faq_block),
        ('GalleryBlock.ts', gallery_block),
        ('TestimonialBlock.ts', testimonial_block),
    ]
    
    for filename, content in blocks:
        file_path = blocks_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Utworzono: {filename}")
    
    # Utwórz index.ts
    index_content = """// Export wszystkich bloków
export { CTABlock } from './CTABlock';
export { PricingBlock } from './PricingBlock';
export { FAQBlock } from './FAQBlock';
export { GalleryBlock } from './GalleryBlock';
export { TestimonialBlock } from './TestimonialBlock';
"""
    
    index_path = blocks_dir / 'index.ts'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"✅ Utworzono: index.ts")
    
    print("\n📝 INSTRUKCJA INTEGRACJI:")
    print("=" * 50)
    print("""
1. SKOPIUJ pliki z katalogu:
   _config/payload/blocks/
   
   DO katalogu Payload CMS:
   src/blocks/ (lub blocks/)

2. ZAKTUALIZUJ payload.config.ts:
   
   import {
     CTABlock,
     PricingBlock,
     FAQBlock,
     GalleryBlock,
     TestimonialBlock
   } from './blocks';

3. DODAJ bloki do kolekcji Services/Pages:

   {
     name: 'content',
     type: 'blocks',
     label: 'Zawartość',
     blocks: [
       CTABlock,
       PricingBlock,
       FAQBlock,
       GalleryBlock,
       TestimonialBlock,
     ],
   }

4. RESTART serwera:
   - Zatrzymaj serwer (Ctrl+C)
   - npm run dev

5. SPRAWDŹ w edytorze:
   - Otwórz edycję dowolnej usługi/strony
   - Kliknij na pole "Zawartość" 
   - Powinny pojawić się dostępne bloki
""")

if __name__ == "__main__":
    create_block_definitions()