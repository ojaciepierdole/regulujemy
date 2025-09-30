#!/usr/bin/env python3
"""
Skrypt do naprawy brakujących linków w indeksach
"""

import os

PROJECT_PATH = "/Users/tomek/Documents/Kamyki/Regulujemy.pl"

def fix_blog_index():
    """Naprawia brakujące linki w blog/index.md"""
    blog_index_path = os.path.join(PROJECT_PATH, "blog/index.md")
    
    # Linki do dodania
    missing_links = """
### [Jak sprawdzić czy okno wymaga regulacji?](poradniki/jak-sprawdzic-czy-okno-wymaga-regulacji.md)
*Prosty test domowy w 5 minut*

### [Kiedy regulować okna?](poradniki/kiedy-regulowac-okna.md)
*Najlepsze pory roku i częstotliwość regulacji*
"""
    
    try:
        with open(blog_index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Znajdź miejsce do wstawienia (po istniejących linkach)
        if "[Dlaczego okno się zacina?]" in content:
            # Dodaj po ostatnim artykule
            parts = content.split("[Dlaczego okno się zacina?](poradniki/dlaczego-okno-sie-zacina.md)")
            if len(parts) == 2:
                # Znajdź koniec opisu
                end_idx = parts[1].find('\n\n')
                if end_idx != -1:
                    new_content = parts[0] + "[Dlaczego okno się zacina?](poradniki/dlaczego-okno-sie-zacina.md)" + parts[1][:end_idx] + "\n" + missing_links + parts[1][end_idx:]
                    
                    with open(blog_index_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print("✅ Naprawiono blog/index.md")
                    return True
    except Exception as e:
        print(f"❌ Błąd naprawy blog/index.md: {e}")
    
    return False

def fix_warszawa_index():
    """Naprawia brakujące dzielnice w lokalizacje/warszawa/index.md"""
    warszawa_index_path = os.path.join(PROJECT_PATH, "lokalizacje/warszawa/index.md")
    
    # Sekcje do dodania
    missing_sections = """

### [BIAŁOŁĘKA](Białołęka.md)

**Czas dojazdu:** 25-40 min | **Dzielnica rozwojowa**

Dynamicznie rozwijająca się dzielnica z nowymi osiedlami mieszkaniowymi. Obsługujemy zarówno nowe budownictwo, jak i starsze osiedla. Specjalizujemy się w serwisie okien w okresie pogwarancyjnym.

### [REMBERTÓW](rembertow.md)

**Czas dojazdu:** 30-45 min | **Dzielnica spokojna**

Zielona dzielnica z przewagą domów jednorodzinnych. Świadczymy kompleksowe usługi dla właścicieli domów, w tym regulację okien dachowych i drzwi tarasowych.

### [URSUS](ursus.md)

**Czas dojazdu:** 20-35 min | **Dzielnica mieszkaniowa**

Dzielnica z dużą liczbą osiedli mieszkaniowych i domów. Oferujemy szybkie terminy i konkurencyjne ceny dla mieszkańców Ursusa.

### [WAWER](wawer.md)

**Czas dojazdu:** 25-40 min | **Największa dzielnica**

Rozległa dzielnica z różnorodną zabudową. Docieramy do wszystkich części Wawra, od Falenicy po Radość. Specjalne pakiety dla domów jednorodzinnych.

### [WESOŁA](wesola.md)

**Czas dojazdu:** 30-45 min | **Dzielnica zielona**

Spokojna dzielnica willowa z dużą ilością zieleni. Oferujemy kompleksową obsługę domów, w tym okien dachowych i przeszkleń ogrodowych.

### [WŁOCHY](wlochy.md)

**Czas dojazdu:** 15-30 min | **Blisko lotniska**

Doskonale skomunikowana dzielnica. Szybkie dojazdy i elastyczne terminy. Obsługujemy zarówno mieszkania, jak i obiekty komercyjne.
"""
    
    try:
        with open(warszawa_index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Dodaj przed końcem pliku
        if missing_sections.strip() not in content:
            # Znajdź miejsce przed statystykami lub na końcu
            if "## DLACZEGO WARTO WYBRAĆ" in content:
                parts = content.split("## DLACZEGO WARTO WYBRAĆ")
                new_content = parts[0].rstrip() + "\n" + missing_sections + "\n\n## DLACZEGO WARTO WYBRAĆ" + parts[1]
            else:
                new_content = content.rstrip() + "\n" + missing_sections
            
            with open(warszawa_index_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Naprawiono lokalizacje/warszawa/index.md")
            return True
    except Exception as e:
        print(f"❌ Błąd naprawy warszawa/index.md: {e}")
    
    return False

def fix_lokalizacje_index():
    """Naprawia brakujący link do inne-miasta w lokalizacje/index.md"""
    lokalizacje_index_path = os.path.join(PROJECT_PATH, "lokalizacje/index.md")
    
    try:
        with open(lokalizacje_index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź czy link już istnieje
        if "[Inne Miasta](inne-miasta.md)" not in content:
            # Zamień istniejący tekst
            content = content.replace(
                "[Łódź](inne-miasta.md)",
                "[Inne Miasta](inne-miasta.md)"
            )
            
            with open(lokalizacje_index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Naprawiono lokalizacje/index.md")
            return True
    except Exception as e:
        print(f"❌ Błąd naprawy lokalizacje/index.md: {e}")
    
    return False

def add_cta_template():
    """Tworzy szablon CTA do wykorzystania"""
    cta_template = """
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
    
    template_path = os.path.join(PROJECT_PATH, "analiza-linkow/szablon-cta.md")
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(cta_template)
    
    print(f"✅ Utworzono szablon CTA w: {template_path}")

def main():
    """Główna funkcja naprawcza"""
    print("🔧 Rozpoczynam naprawę brakujących linków...\n")
    
    # Napraw pliki
    fix_blog_index()
    fix_warszawa_index()
    fix_lokalizacje_index()
    add_cta_template()
    
    print("\n✅ Proces naprawy zakończony!")
    print("\n⚠️  Pozostałe pliki wymagają ręcznej edycji.")
    print("📄 Użyj szablonu CTA z: analiza-linkow/szablon-cta.md")

if __name__ == "__main__":
    main()