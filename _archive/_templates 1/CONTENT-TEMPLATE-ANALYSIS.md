# Content Template Analysis - Regulujemy.pl

## Overview
Based on my analysis of the Regulujemy.pl project structure, I've identified distinct content types and templates that can be standardized for better consistency and CMS migration readiness.

## Content Type Taxonomy

### 1. **Homepage Template**
**File:** `index.md`
**Characteristics:**
- Hero section with main value proposition
- Navigation mega-menu structure
- Service highlights (3-4 key services)
- Trust indicators (years of experience, response time, warranty)
- Location coverage overview
- CTA sections (emergency and standard)
- Social proof (numbers, certifications)
- Footer with complete navigation

**YAML Structure:**
```yaml
layout: homepage
sections:
  hero:
    title: Main headline
    subtitle: Value proposition
    cta_primary: Emergency button
    cta_secondary: Standard contact
  services_highlights: 3-4 featured services
  trust_indicators: Array of trust points
  coverage_map: Boolean
  testimonials: Boolean
```

### 2. **Category Index Templates**

#### 2a. **Service Category Index**
**Files:** `uslugi/index.md`, subdirectory indexes
**Characteristics:**
- Category introduction with emotional hook
- Service grid/list with pricing ranges
- Decision helper content
- Category-specific trust indicators
- Related blog posts
- FAQ preview
- Contact section with category context

**YAML Structure:**
```yaml
layout: category-index
category_type: service
intro_style: storytelling # or professional
services:
  display: grid # or list
  show_pricing: true
  show_duration: true
  show_warranty: true
related_content:
  blog_posts: 3
  faqs: 5
```

#### 2b. **Product Category Index**
**Files:** `produkty/index.md`, `produkty/okna/index.md`
**Characteristics:**
- Product grid with images
- Brand showcase
- Comparison tables
- Technical specifications summary
- Installation service tie-in
- Warranty information
- Financing options

**YAML Structure:**
```yaml
layout: category-index
category_type: product
products:
  display: grid
  show_brands: true
  show_specs: summary # or detailed
  comparison_table: true
financing:
  enabled: true
  options: [cash, installments, leasing]
```

#### 2c. **Location Category Index**
**Files:** `lokalizacje/warszawa/index.md`
**Characteristics:**
- District grid/list
- Response time map
- Service availability matrix
- Team distribution info
- Local testimonials

### 3. **Detail Page Templates**

#### 3a. **Service Detail Page**
**Files:** `uslugi/*/specific-service.md`
**Characteristics:**
- Service description with benefits
- Problem-solution narrative
- Process steps (numbered list)
- Pricing table/structure
- Time estimates
- Warranty details
- Before/after scenarios
- FAQ section specific to service
- Related services
- Contact with service pre-selected

**Content Sections Pattern:**
1. Navigation breadcrumb
2. Hero/Introduction (emotional connection)
3. "What is this service?" explanation
4. "When do you need this?" (problem indicators)
5. Process/How we work
6. Pricing information
7. Warranty/Guarantees
8. FAQ (3-5 questions)
9. Related services
10. Contact section

**YAML Structure:**
```yaml
layout: service-detail
service:
  category: regulacja-okien
  subcategory: podstawowa
  price_from: 35
  price_unit: "zł/okno"
  duration: "20-30 min"
  warranty_months: 24
  emergency_available: true
sections:
  process_steps: true
  pricing_table: true
  faq: embedded # or linked
  before_after: true
  testimonials: 2-3
```

#### 3b. **Product Detail Page**
**Files:** `produkty/okna/okna-pcv.md`
**Characteristics:**
- Product description with benefits
- Technical specifications table
- Brand/model variations
- Installation requirements
- Pricing structure
- Warranty information
- Certifications
- Gallery/images
- Related products
- Installation service CTA

**YAML Structure:**
```yaml
layout: product-detail
product:
  category: okna
  type: pcv
  brands: [REHAU, VEKA, SALAMANDER]
  price_from: 295
  price_unit: "zł/m²"
  warranty_years: 10
specs_table:
  format: responsive # or static
  highlight_key_specs: true
gallery:
  enabled: true
  show_technical_drawings: true
```

#### 3c. **Location Detail Page**
**Files:** `lokalizacje/warszawa/*.md`
**Characteristics:**
- District-specific information
- Local team details
- Response time specifics
- Common building types and issues
- Local testimonials
- Parking/access information
- Coverage sub-areas
- Local partnerships
- District-specific pricing notes

**YAML Structure:**
```yaml
layout: location-detail
location:
  city: Warszawa
  district: Mokotów
  response_time: "15-25 min"
  team_size: 3
  extension: "ext. MOK"
coverage:
  areas: [Stary Mokotów, Górny Mokotów, etc.]
  building_types: [kamienice, bloki, apartamentowce]
local_features:
  parking: free
  public_transport: [metro, bus, tram]
```

### 4. **Business/B2B Templates**

#### 4a. **Business Category Index**
**Files:** `biznes/index.md`
**Characteristics:**
- B2B value proposition
- Client logos/trust indicators
- Service packages overview
- Case studies preview
- Partnership benefits
- Contact with business context

#### 4b. **Business Service Detail**
**Files:** `biznes/umowy-serwisowe.md`
**Characteristics:**
- Package comparison table
- Detailed service inclusions
- SLA information
- Pricing tiers
- Contract terms
- Client testimonials
- ROI calculator/benefits
- Business-specific FAQ

**YAML Structure:**
```yaml
layout: business-service
service:
  type: maintenance-contract
packages:
  - name: Basic
    price_from: 99
    features: [list]
  - name: Standard
    price_from: 299
    features: [list]
  - name: Premium
    price_from: 599
    features: [list]
sla:
  response_time: "4-48h"
  reporting: quarterly
```

### 5. **Static Page Templates**

#### 5a. **FAQ Page**
**File:** `strony/faq.md`
**Characteristics:**
- Conversational intro
- Categorized questions
- Anchor links navigation
- Expandable sections
- Related links to services
- Contact for unanswered questions

**YAML Structure:**
```yaml
layout: faq
faq_style: conversational # or formal
categories:
  - name: "Podstawowe sprawy"
    questions: [array]
  - name: "Regulacja okien"
    questions: [array]
show_table_of_contents: true
```

#### 5b. **Pricing Page**
**File:** `strony/cennik.md`
**Characteristics:**
- Important notes section
- Table of contents
- Categorized pricing tables
- Package deals
- Additional fees section
- Payment methods
- Warranty information per service

**YAML Structure:**
```yaml
layout: pricing
pricing:
  display: tables # or cards
  show_vat: true
  highlight_popular: true
  enable_calculator: false
payment_methods:
  accepted: [cash, card, transfer, blik]
  terms: "14-30 days for business"
```

### 6. **Blog Templates**

#### 6a. **Blog Index**
**File:** `blog/index.md`
**Characteristics:**
- Friendly introduction
- Category showcase
- Latest articles grid
- Popular articles sidebar
- Newsletter signup
- Category descriptions

#### 6b. **Blog Post**
**Files:** `blog/poradniki/*.md`
**Characteristics:**
- Detailed navigation breadcrumbs
- Related articles section
- Warning/alert boxes
- Step-by-step instructions
- Visual indicators (icons, emojis)
- Call-out boxes for important info
- Author info
- Share buttons
- Comments/feedback section

**YAML Structure:**
```yaml
layout: blog-post
post:
  category: poradniki
  read_time: "5 min"
  difficulty: easy # medium, hard
  tools_required: none
  related_services: [regulacja-podstawowa]
content_features:
  warning_boxes: true
  step_numbers: true
  images: true
  downloadable_checklist: false
```

## Common Content Patterns

### 1. **Navigation Patterns**
- Breadcrumb: `[Start] > [Category] > [Subcategory] > **Current Page**`
- Contextual navigation with related links
- "Back to top" functionality for long pages

### 2. **Trust Building Elements**
- Years of experience (15+ lat, 20 lat)
- Response time promises (60 minut)
- Warranty periods (up to 5 years)
- Certifications and partnerships
- Local presence emphasis

### 3. **Call-to-Action Patterns**
- Emergency CTAs (red, prominent)
- Standard CTAs (blue/green)
- Contextual CTAs (service-specific)
- Form CTAs (quote requests)

### 4. **Content Tone Patterns**
- Conversational, friendly tone
- Direct address to reader ("Twoje okno")
- Problem-solution narrative
- Expertise without arrogance
- Local knowledge emphasis

### 5. **Pricing Display Patterns**
- "od X zł" (from X PLN)
- Price + unit (per window, per m²)
- Package pricing with savings
- Transparent additional costs

### 6. **SEO Patterns**
- Long-tail keywords in titles
- Location-specific optimization
- Service-specific meta descriptions
- FAQ schema markup
- Local business schema

## Template Consolidation Recommendations

### 1. **Create Base Templates**
```yaml
base-page:
  meta: [title, description, keywords]
  navigation: [breadcrumb, related]
  sections: [hero, content, cta]
  
service-base:
  extends: base-page
  adds: [pricing, warranty, process]
  
product-base:
  extends: base-page
  adds: [specs, gallery, brands]
```

### 2. **Standardize Section Components**
- Hero sections (3 variants)
- Pricing tables (2 formats)
- FAQ sections (embedded/linked)
- Contact sections (as per created template)
- Trust indicators (horizontal/vertical)
- Process steps (numbered/timeline)

### 3. **Content Block Library**
- Warning/Alert boxes
- Testimonial cards
- Service cards
- Product cards
- Pricing cards
- Team member cards
- Location info boxes

## Migration Strategy

### Phase 1: Template Creation
1. Create base Obsidian templates for each type
2. Define YAML schema for each template
3. Create example implementations
4. Document usage guidelines

### Phase 2: Content Standardization
1. Audit existing content against templates
2. Identify variations and exceptions
3. Standardize YAML frontmatter
4. Update content to match templates

### Phase 3: Component Development
1. Create reusable content blocks
2. Implement dynamic sections
3. Add template inheritance
4. Create variant system

### Phase 4: Testing & Refinement
1. Test templates with real content
2. Gather feedback from content team
3. Refine based on usage patterns
4. Document best practices

## Next Steps

1. **Priority Templates to Create:**
   - Service detail template
   - Product detail template
   - Location detail template
   - Blog post template

2. **Components to Standardize:**
   - Pricing tables
   - FAQ sections
   - Process steps
   - Trust indicators

3. **Content to Migrate First:**
   - High-traffic service pages
   - Main category indexes
   - Popular blog posts
   - Business packages

This template system will provide consistency across all content types while maintaining flexibility for specific needs. Each template should be created as an Obsidian template with full YAML configuration options.
