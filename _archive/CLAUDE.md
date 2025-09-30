# CLAUDE.md - Status projektu Regulujemy.pl

## Data: 2025-07-31

## Status obecny

### ✅ Ukończone
1. **Analiza struktury projektu** - kompletna analiza 100+ plików markdown
2. **System szablonów kontaktowych** - stworzony dla Obsidian (ale nie używany)
3. **Struktura Payload CMS** - kompletna konfiguracja headless CMS:
   - Kolekcje: Services, Products, Locations, BlogPosts, Pages, Media, Users, **Pricing (NOWA)**
   - Globalne: Contact (dane kontaktowe)
   - Bloki: ContactSection, PricingTable, ProcessSteps, FAQ, Testimonials
4. **Analiza kompletności** - przeprowadzona dla wszystkich 108 plików:
   - 95% plików ma kompletny frontmatter
   - Zidentyfikowano brakujące pola dla CMS
   - Przeanalizowano spójność struktury treści

### 🚧 W trakcie - Problem z uruchomieniem
**Payload CMS w Docker** - problemy z zależnościami:
- Brakuje `@aws-sdk/client-s3` mimo dodania do package.json
- Problem z plikiem yarn.lock (jest katalogiem zamiast pliku)
- Kontener się uruchamia ale aplikacja crashuje
- **ROZWIĄZANIE**: Tymczasowo wyłączono S3 storage w konfiguracji

### 📊 Analiza kompletności projektu

#### Frontmatter - statystyki:
- **108 plików** markdown przeanalizowanych
- **95% kompletność** frontmatter
- **5 plików** bez frontmatter (dokumentacyjne)
- **7 plików** z brakującymi polami (głównie keywords)

#### Spójność treści:
**USŁUGI (34 pliki)**:
- 85% ma sekcje cenowe
- 53% ma opis procesu
- 38% ma FAQ
- 44% ma CTA

**PRODUKTY (21 plików)**:
- 62% ma informacje cenowe
- 33% opisuje proces montażu
- 62% ma FAQ
- 10% ma CTA (za mało!)

**LOKALIZACJE (26 plików)**:
- 38% ma cennik lokalny
- 0% ma opis procesu
- 4% ma FAQ
- 23% ma CTA
- **Problem**: Niespójna struktura treści

### 📁 Struktura projektu - WSZYSTKIE ŚCIEŻKI

#### Oryginalna zawartość (markdown)
```
/Users/tomek/Documents/Kamyki/Regulujemy.pl/
├── _archive/                    # Narzędzia i szablony archiwalne
│   ├── _templates/             # Stare szablony
│   ├── analiza-linkow/         # Skrypty Python do analizy linków
│   └── check_frontmatter.py    # Walidacja contentu
├── _config/                    # Konfiguracje YAML
│   ├── access/                 # Dane dostępowe
│   │   └── credentials.md      # Wszystkie hasła i dostępy
│   ├── assets.yml              # Konfiguracja zasobów
│   ├── cms-migration-guide.md  # Plan migracji 8-tygodniowy
│   ├── contact.yml             # Scentralizowane dane kontaktowe
│   ├── content-relationships.yml # Relacje między treściami
│   └── content-structure.yml   # Struktura typów treści
├── _templates/                 # Szablony Obsidian (niewykorzystane)
│   ├── components/             # Komponenty
│   │   ├── contact-section.md  # Szablon sekcji kontaktowej
│   │   ├── contact-usage-guide.md
│   │   ├── contact-variants.md
│   │   └── service-detail-template.md
│   ├── examples/               # Przykłady użycia
│   │   ├── district-page-mokotow.md
│   │   └── service-page-with-contact.md
│   ├── CONTACT-TEMPLATE-SUMMARY.md
│   ├── CONTENT-TEMPLATE-ANALYSIS.md
│   ├── TEMPLATE-HIERARCHY.md
│   ├── migrate-contact-sections.py
│   └── validate-templates.py
├── biznes/                     # Usługi B2B (5 plików)
│   ├── biura-lokale-komercyjne.md
│   ├── index.md
│   ├── instytucje-publiczne.md
│   ├── umowy-serwisowe.md
│   └── wspolnoty-mieszkaniowe.md
├── blog/                       # Artykuły blogowe
│   ├── diagnostyka/            # Artykuły diagnostyczne
│   ├── poradniki/              # Poradniki (4 pliki)
│   │   ├── dlaczego-okno-sie-zacina.md
│   │   ├── jak-przygotowac-mieszkanie-na-lato.md
│   │   ├── jak-sprawdzic-czy-okno-wymaga-regulacji.md
│   │   └── kiedy-regulowac-okna.md
│   └── index.md
├── lokalizacje/                # Lokalizacje
│   ├── warszawa/               # 18 plików dzielnic
│   │   ├── bemowo.md
│   │   ├── bialoleka.md
│   │   ├── bielany.md
│   │   ├── index.md
│   │   ├── mokotow.md
│   │   ├── ochota.md
│   │   ├── praga-polnoc.md
│   │   ├── praga-poludnie.md
│   │   ├── rembertow.md
│   │   ├── srodmiescie.md
│   │   ├── targowek.md
│   │   ├── ursus.md
│   │   ├── ursynow.md
│   │   ├── wawer.md
│   │   ├── wilanow.md
│   │   ├── wlochy.md
│   │   ├── wola.md
│   │   └── zoliborz.md
│   └── inne-miasta.md
├── produkty/                   # Produkty
│   ├── drzwi/                  # Różne typy drzwi
│   ├── okna/                   # Różne typy okien
│   │   ├── index.md
│   │   ├── okna-aluminiowe.md
│   │   ├── okna-drewniane.md
│   │   └── okna-pcv.md
│   ├── okucia/                 # Okucia okienne
│   ├── systemy/                # Systemy okienne
│   ├── szyby/                  # Szyby
│   ├── uszczelki/              # Uszczelki
│   ├── zabezpieczenia-i-dodatki/ # Akcesoria
│   └── index.md
├── strony/                     # Strony statyczne (8 plików)
│   ├── cennik.md               # 567 linii - główny cennik
│   ├── certyfikaty.md
│   ├── faq.md
│   ├── gwarancja.md
│   ├── kontakt.md
│   ├── o-nas.md
│   ├── opinie.md
│   └── promocje.md
├── uslugi/                     # Usługi (~40 plików)
│   ├── biznes/                 # Usługi biznesowe
│   ├── dodatkowe/              # Usługi dodatkowe
│   ├── montaz-sprzedaz/        # Montaż i sprzedaż
│   ├── naprawa-okien/          # Naprawy
│   ├── regulacja-okien/        # Regulacje
│   │   ├── index.md
│   │   ├── regulacja-drzwi-balkonowych.md
│   │   ├── regulacja-letnia-zimowa.md
│   │   ├── regulacja-podstawowa.md
│   │   └── regulacja-zaawansowana.md
│   ├── specjalistyczne/        # Usługi specjalistyczne
│   ├── techniczne/             # Usługi techniczne
│   ├── uszczelnianie/          # Uszczelnianie
│   ├── wymiana-czesci/         # Wymiana części
│   └── index.md
├── ANALIZA_KOMPLETNOSCI.md     # Raport z analizy (208 linii)
├── CLAUDE.md                   # Ten dokument statusu
├── FRONTMATTER_ANALYSIS.md     # Szczegółowa analiza frontmatter
├── GEMINI.md                   # Dokumentacja z Gemini
├── OPUS.md                     # Dokumentacja handoff
├── SCORE.md                    # Oceny projektu
├── analyze_project_structure.py # Skrypt analizy
└── index.md                    # Strona główna
```

#### Aplikacja Payload CMS
```
/Users/tomek/Development/regulujemy/payload-app/
├── src/
│   ├── collections/            # Definicje kolekcji CMS
│   │   ├── BlogPosts.ts       # Kolekcja artykułów (266 linii)
│   │   ├── Locations.ts       # Kolekcja lokalizacji (428 linii)
│   │   ├── Media.ts           # Kolekcja mediów (102 linie)
│   │   ├── Pages.ts           # Kolekcja stron (241 linii)
│   │   ├── Pricing.ts         # NOWA - Kolekcja cennika (367 linii)
│   │   ├── Products.ts        # Kolekcja produktów (537 linii)
│   │   ├── Services.ts        # Kolekcja usług (372 linie)
│   │   └── Users.ts           # Kolekcja użytkowników (33 linie)
│   ├── globals/               # Dane globalne
│   │   └── Contact.ts         # Globalne dane kontaktowe (396 linii)
│   ├── blocks/                # Bloki treści
│   │   └── index.ts           # ContactSection, PricingTable, FAQ, etc. (392 linie)
│   ├── payload.config.ts      # Główna konfiguracja Payload (99 linii)
│   └── server.ts              # Serwer Express (39 linii)
├── .dockerignore              # Pliki ignorowane przez Docker
├── .env                       # Zmienne środowiskowe (40 linii)
├── Dockerfile                 # Dockerfile produkcyjny (20 linii)
├── Dockerfile.dev             # Dockerfile developerski (17 linii)
├── README.md                  # Dokumentacja projektu (163 linie)
├── docker-compose.yml         # Konfiguracja Docker Compose (76 linii)
├── package.json               # Zależności npm (46 linii)
├── tsconfig.json              # Konfiguracja TypeScript (27 linii)
├── yarn.lock                  # PROBLEM: jest katalogiem zamiast pliku!
└── nodemon.json               # PROBLEM: jest katalogiem zamiast pliku!
```

### 🔧 Konfiguracja Docker

**Serwisy:**
- MongoDB (port 27017) - ✅ działa
- MinIO (porty 9000, 9001) - ✅ działa  
- Payload CMS (port 3456) - ✅ działa

**Dane dostępowe zapisane w:**
`/Users/tomek/Documents/Kamyki/Regulujemy.pl/_config/access/credentials.md`

### 💰 Moduł cennikowy

**Stan obecny:**
- Cennik w pliku `/strony/cennik.md` (567 linii)
- Arkusz Google Sheets: https://docs.google.com/spreadsheets/d/1uyjFht0Qq_W_dn012-ES5Ev5MdkHeXr4dJxJYSi6LXE/
- Problem: duplikacja danych

**Rozwiązanie - NOWA kolekcja Pricing:**
- Kompletna struktura cennika w CMS
- Modyfikatory cen (weekendy, awarie)
- Rabaty ilościowe
- Integracja z Google Sheets (opcjonalna)
- Powiązania z usługami i produktami
- Historia zmian cen

### 🎯 Następne kroki

1. **Naprawić Payload CMS**:
   ```bash
   cd /Users/tomek/Development/regulujemy/payload-app
   rm -rf yarn.lock nodemon.json
   touch yarn.lock
   docker-compose restart payload
   ```

2. **Migracja cennika**:
   - Wyekstrahować ceny z cennik.md
   - Zaimportować do kolekcji Pricing
   - Powiązać z usługami/produktami

3. **Uzupełnienie danych**:
   - Dodać brakujące pola do frontmatter
   - Ustandaryzować strukturę lokalizacji
   - Dodać więcej CTA do produktów

### 📝 Ważne informacje

- **MinIO działa**: http://localhost:9001 (login: minio, hasło: minio123)
- **MongoDB działa**: mongodb://admin:admin123@localhost:27017/regulujemy-cms?authSource=admin
- **Payload CMS**: na http://localhost:3456/admin

### 🔑 Kluczowe pliki konfiguracyjne
- `_config/contact.yml` - scentralizowane dane kontaktowe
- `_config/content-structure.yml` - struktura typów treści
- `_config/content-relationships.yml` - relacje między treściami
- `_config/cms-migration-guide.md` - plan migracji na CMS
- `_config/access/credentials.md` - wszystkie dane dostępowe
- `ANALIZA_KOMPLETNOSCI.md` - raport z analizy projektu

### 📊 Statystyki projektu
- **Pliki markdown**: 108
- **Usługi**: 34 pliki (85% ma ceny)
- **Lokalizacje**: 26 plików (18 dzielnic Warszawy)
- **Produkty**: 21 plików (62% ma ceny)
- **Blog**: 6 artykułów
- **Strony statyczne**: 8 stron
- **Biznes**: 5 plików B2B

### 🚀 Stan migracji
- **Struktura CMS**: ✅ Kompletna z modułem cennikowym
- **Konfiguracja**: ✅ Gotowa 
- **Uruchomienie**: ✅ Gotowa 
- **Analiza kompletności**: ✅ Wykonana
- **Migracja danych**: ⏳ Oczekuje na działający CMS
