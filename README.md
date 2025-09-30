# Regulujemy.pl - Repozytorium Treści i Danych

## Opis

Repozytorium zawiera dane i treści dla serwisu Regulujemy.pl - platformy oferującej usługi regulacji i produkty hydrauliczne. Projekt służy jako źródło danych do importu oraz miejsce przechowywania struktury treści strony.

## Struktura Repozytorium

```
regulujemy-pl/
├── Cenniki/          # Dane cennikowe w formacie CSV
├── JSON/             # Dane strukturalne w formacie JSON
├── _archive/         # Zarchiwizowane pliki
├── biznes/           # Treści biznesowe
├── blog/             # Artykuły blogowe
├── lokalizacje/      # Dane lokalizacyjne
├── produkty/         # Opisy produktów
├── strony/           # Treści stron
├── uslugi/           # Opisy usług
└── index.md          # Strona główna
```

## Folder `Cenniki/`

Zawiera dane cennikowe w formacie CSV gotowe do importu do systemu CMS:

- **`products [data].csv`** - Lista produktów z cenami, kategoriami, opisami i parametrami dostępności
- **`services [data].csv`** - Lista usług z cenami, czasem trwania, kategoriami i opisami

Pliki te służą do masowego importu lub aktualizacji oferty w systemie zarządzania treścią.

## Folder `JSON/`

Zawiera dane strukturalne w formacie JSON gotowe do importu:

- **`articles [data].json`** - Artykuły i wpisy blogowe
- **`cta_blocks [data].json`** - Bloki Call-to-Action używane na stronie
- **`faq [data].json`** - Często zadawane pytania (FAQ)
- **`locations [data].json`** - Dane o lokalizacjach świadczenia usług
- **`navigation [data].json`** - Struktura nawigacji strony
- **`pages [data].json`** - Treści stron statycznych
- **`testimonials [data].json`** - Opinie klientów

Wszystkie pliki JSON są oznaczone datą i godziną eksportu (format: RRRRMMDD-GGMMSS) i mogą być bezpośrednio importowane do systemu Payload CMS lub innego kompatybilnego systemu.

## Użycie

### Import danych CSV
Pliki CSV z folderu `Cenniki/` można importować bezpośrednio do arkuszy kalkulacyjnych, baz danych lub systemów CMS obsługujących ten format.

### Import danych JSON
Pliki JSON z folderu `JSON/` są przygotowane do importu przez API lub narzędzia administracyjne CMS.

## Uwagi

- Pliki są regularnie aktualizowane - data w nazwie pliku wskazuje na wersję danych
- Przed importem zaleca się wykonanie kopii zapasowej istniejących danych
- Format danych jest zgodny z Payload CMS

---

**Ostatnia aktualizacja:** Wrzesień 2024
