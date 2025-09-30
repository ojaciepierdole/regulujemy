#!/usr/bin/env python3
"""
Skrypt do dodawania brakujących elementów (CTA i powiązane strony)
"""

import os

PROJECT_PATH = "/Users/tomek/Documents/Kamyki/Regulujemy.pl"

# Szablon CTA
CTA_TEMPLATE = """
## 📞 Skontaktuj się z nami

**Potrzebujesz profesjonalnej pomocy?**

> **[📞 ZADZWOŃ: 123-456-789]**
> 
> **[📝 ZAMÓW BEZPŁATNĄ WYCENĘ](../../strony/kontakt.md)**
> 
> **[💬 CZAT NA ŻYWO]**

### ✅ Dlaczego Regulujemy.pl?

- **15+ lat doświadczenia** w branży
- **Gwarancja do 5 lat** na wykonane prace
- **Bezpłatny dojazd** w Warszawie
- **Pilne wyjazdy** w 60 minut
- **Przejrzyste ceny** bez ukrytych kosztów
"""

# Szablon powiązanych stron dla różnych kategorii
RELATED_PAGES = {
    'regulacja': """
### Powiązane strony:
- [Naprawa okien](../naprawa-okien/index.md)
- [Wymiana części](../wymiana-czesci/index.md)
- [Uszczelnianie okien](../uszczelnianie/index.md)
- [Cennik usług](../../strony/cennik.md)
""",
    'naprawa': """
### Powiązane strony:
- [Regulacja okien](../regulacja-okien/index.md)
- [Wymiana części](../wymiana-czesci/index.md)
- [Konserwacja okien](../specjalistyczne/index.md)
- [Cennik napraw](../../strony/cennik.md)
""",
    'produkty': """
### Zobacz także:
- [Montaż okien](../../uslugi/montaz-sprzedaz/index.md)
- [Serwis okien](../../uslugi/naprawa-okien/index.md)
- [Cennik produktów](../../strony/cennik.md)
- [Gwarancja](../../strony/gwarancja.md)
""",
    'lokalizacje': """
### Powiązane strony:
- [Inne dzielnice Warszawy](index.md)
- [Cennik usług](../../strony/cennik.md)
- [Kontakt](../../strony/kontakt.md)
- [Opinie klientów](../../strony/opinie.md)
"""
}

def add_cta_to_file(filepath):
    """Dodaje CTA na końcu pliku jeśli go nie ma"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź czy już ma CTA
        if 'Skontaktuj się z nami' in content or 'ZADZWOŃ:' in content:
            return False
        
        # Dodaj CTA przed końcową linią
        if content.rstrip().endswith('!'):
            content = content.rstrip()[:-1] + '\n\n' + CTA_TEMPLATE + '\n\n---\n\n**Regulujemy.pl** - Twój partner w opiece nad oknami!'
        else:
            content = content.rstrip() + '\n\n' + CTA_TEMPLATE
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Błąd: {e}")
        return False

def add_related_pages(filepath, category):
    """Dodaje sekcję powiązanych stron"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź czy już ma powiązane strony
        if 'Powiązane strony:' in content or 'Zobacz także:' in content:
            return False
        
        # Znajdź miejsce do wstawienia (przed CTA jeśli jest)
        if 'Skontaktuj się z nami' in content:
            parts = content.split('## 📞 Skontaktuj się z nami')
            new_content = parts[0].rstrip() + '\n\n---\n\n' + RELATED_PAGES[category] + '\n---\n\n## 📞 Skontaktuj się z nami' + parts[1]
        else:
            new_content = content.rstrip() + '\n\n---\n\n' + RELATED_PAGES[category]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Błąd: {e}")
        return False

def main():
    """Główna funkcja"""
    print("🔧 Dodawanie brakujących elementów...")
    
    # Lista plików do uzupełnienia
    files_to_update = [
        # Usługi regulacja
        ('uslugi/regulacja-okien/regulacja-drewniane.md', 'regulacja', True),
        ('uslugi/regulacja-okien/regulacja-pcv.md', 'regulacja', True),
        ('uslugi/regulacja-okien/regulacja-aluminiowe.md', 'regulacja', True),
        ('uslugi/regulacja-okien/regulacja-zaawansowana.md', 'regulacja', True),
        
        # Usługi naprawa
        ('uslugi/naprawa-okien/naprawa-klamek.md', 'naprawa', False),
        ('uslugi/naprawa-okien/naprawa-okuc.md', 'naprawa', False),
        ('uslugi/naprawa-okien/naprawa-zawiasow.md', 'naprawa', False),
        ('uslugi/naprawa-okien/wymiana-szyb.md', 'naprawa', True),
        ('uslugi/naprawa-okien/wymiana-uszczelek.md', 'naprawa', True),
        
        # Produkty
        ('produkty/okna/okna-pcv.md', 'produkty', False),
        ('produkty/okna/okna-drewniane.md', 'produkty', True),
        ('produkty/okna/okna-aluminiowe.md', 'produkty', True),
        ('produkty/drzwi/drzwi-wewnetrzne-pcv.md', 'produkty', True),
        ('produkty/drzwi/drzwi-wewnetrzne-drewniane.md', 'produkty', True),
        
        # Lokalizacje
        ('lokalizacje/warszawa/ochota.md', 'lokalizacje', True),
        ('lokalizacje/warszawa/ursus.md', 'lokalizacje', True),
        ('lokalizacje/warszawa/wawer.md', 'lokalizacje', True),
        ('lokalizacje/warszawa/wesola.md', 'lokalizacje', True),
    ]
    
    cta_added = 0
    related_added = 0
    
    for file_path, category, needs_cta in files_to_update:
        full_path = os.path.join(PROJECT_PATH, file_path)
        
        if os.path.exists(full_path):
            # Dodaj powiązane strony
            if add_related_pages(full_path, category):
                related_added += 1
                print(f"✅ Dodano powiązane strony: {file_path}")
            
            # Dodaj CTA jeśli potrzebne
            if needs_cta and add_cta_to_file(full_path):
                cta_added += 1
                print(f"✅ Dodano CTA: {file_path}")
        else:
            print(f"❌ Nie znaleziono: {file_path}")
    
    print(f"\n📊 Podsumowanie:")
    print(f"- Dodano CTA: {cta_added} plików")
    print(f"- Dodano powiązane strony: {related_added} plików")

if __name__ == "__main__":
    main()