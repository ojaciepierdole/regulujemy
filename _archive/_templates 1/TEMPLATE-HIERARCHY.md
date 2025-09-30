# Content Template Hierarchy - Regulujemy.pl

## Template Structure Overview

```
📁 Base Templates
│
├── 🏠 Homepage Template
│   ├── Hero Section
│   ├── Service Highlights (3-4)
│   ├── Trust Indicators
│   ├── Coverage Map
│   └── Emergency CTA
│
├── 📑 Category Index Templates
│   ├── Service Category Index
│   │   ├── Emotional Introduction
│   │   ├── Service Grid/List
│   │   ├── Pricing Overview
│   │   └── Category FAQ
│   │
│   ├── Product Category Index
│   │   ├── Product Grid
│   │   ├── Brand Showcase
│   │   ├── Comparison Table
│   │   └── Financing Options
│   │
│   └── Location Category Index
│       ├── District List/Map
│       ├── Response Times
│       └── Local Teams
│
├── 📄 Detail Page Templates
│   ├── Service Detail Page
│   │   ├── Problem-Solution Narrative
│   │   ├── Process Steps (5-7)
│   │   ├── Pricing Table
│   │   ├── Service-Specific FAQ
│   │   └── Related Services
│   │
│   ├── Product Detail Page
│   │   ├── Technical Specifications
│   │   ├── Brand Variations
│   │   ├── Installation Guide
│   │   └── Product Gallery
│   │
│   └── Location Detail Page
│       ├── District Info
│       ├── Local Issues
│       ├── Team & Response
│       └── Local Testimonials
│
├── 💼 Business Templates
│   ├── B2B Landing Page
│   │   ├── Corporate Benefits
│   │   ├── Client Logos
│   │   └── Case Studies
│   │
│   └── Service Package Page
│       ├── Package Comparison
│       ├── SLA Details
│       └── Contract Terms
│
├── 📋 Static Page Templates
│   ├── FAQ Page
│   │   ├── Categorized Questions
│   │   ├── Anchor Navigation
│   │   └── Unanswered Question CTA
│   │
│   ├── Pricing Page
│   │   ├── Service Categories
│   │   ├── Pricing Tables
│   │   └── Payment Methods
│   │
│   └── About/Contact Pages
│       ├── Company Story
│       ├── Team Section
│       └── Contact Forms
│
└── 📝 Blog Templates
    ├── Blog Index
    │   ├── Category Cards
    │   ├── Latest Posts
    │   └── Popular Articles
    │
    └── Blog Post
        ├── Tutorial Format
        ├── Step Instructions
        ├── Warning Boxes
        └── Related Articles
```

## Content Section Components

### 🧩 Reusable Components

#### Navigation Components
- **Breadcrumb**: `[Start] > [Category] > [Current]`
- **Related Links**: Contextual navigation
- **Table of Contents**: For long pages

#### Content Blocks
- **Hero Section** (3 variants)
  - Homepage hero (full-width)
  - Category hero (with intro)
  - Service hero (with pricing)

- **Pricing Display** (4 formats)
  - Simple price tag: "od 35 zł"
  - Table format (for comparisons)
  - Card format (for packages)
  - Calculator format (for estimates)

- **Trust Indicators**
  - Icon + Text horizontal bar
  - Vertical list with details
  - Statistics counter
  - Certification badges

- **Process Steps**
  - Numbered list (1,2,3)
  - Timeline visual
  - Icon + description cards

- **FAQ Sections**
  - Accordion (collapsible)
  - Simple Q&A list
  - Categorized with anchors

- **CTA Sections**
  - Emergency (red, phone-focused)
  - Standard (blue, multi-option)
  - Contextual (service-specific)
  - Form-based (quote request)

#### Content Patterns
- **Problem Indicators** ("When you need this")
  - Bullet list with bold keywords
  - Icon grid showing issues
  - Checklist format

- **Testimonials**
  - Quote block with attribution
  - Card with photo
  - Inline text testimonial

- **Alert/Warning Boxes**
  - Red alert (urgent issues)
  - Yellow warning (caution)
  - Blue info (helpful tips)
  - Green success (benefits)

## Template Variables & Configuration

### Base YAML Structure
```yaml
# Meta Information
title: Page title
description: SEO description
keywords: [array of keywords]
author: Content author
created: YYYY-MM-DD
modified: YYYY-MM-DD

# Template Configuration
layout: template-name
template_version: 1.0

# Page-Specific Variables
page:
  type: service|product|location|blog
  category: main-category
  subcategory: sub-category
  
# Content Sections Control
sections:
  hero: 
    enabled: true
    variant: default|minimal|full
  pricing:
    enabled: true
    format: table|cards|inline
  faq:
    enabled: true
    style: embedded|linked
  testimonials:
    enabled: true
    count: 3
    
# Business Logic
pricing:
  from: 35
  unit: "zł/okno"
  show_vat: true
  
warranty:
  months: 24
  type: "standard|extended"
  
response_time:
  minutes: 60
  district_specific: true
```

## Content Flow Patterns

### Service Page Flow
1. **Hook** - Problem statement
2. **Solution** - What we offer
3. **Process** - How we work
4. **Proof** - Results/testimonials
5. **Pricing** - Transparent costs
6. **FAQ** - Address concerns
7. **CTA** - Book service

### Product Page Flow
1. **Overview** - What it is
2. **Benefits** - Why choose this
3. **Options** - Variations available
4. **Specs** - Technical details
5. **Installation** - How it works
6. **Warranty** - Peace of mind
7. **CTA** - Order/Quote

### Location Page Flow
1. **Local Identity** - We know your area
2. **Specifics** - Local issues we solve
3. **Logistics** - How fast we arrive
4. **Team** - Who serves you
5. **Proof** - Local testimonials
6. **CTA** - Call local team

## Template Inheritance Model

```
BaseTemplate
├── MetaTemplate (SEO, navigation)
│   ├── ContentTemplate (sections, layout)
│   │   ├── ServiceTemplate
│   │   │   ├── BasicService
│   │   │   ├── AdvancedService
│   │   │   └── EmergencyService
│   │   ├── ProductTemplate
│   │   │   ├── WindowProduct
│   │   │   ├── DoorProduct
│   │   │   └── AccessoryProduct
│   │   └── LocationTemplate
│   │       ├── CityTemplate
│   │       └── DistrictTemplate
│   └── StaticTemplate
│       ├── InfoTemplate
│       ├── LegalTemplate
│       └── MarketingTemplate
└── BlogTemplate
    ├── TutorialTemplate
    ├── DiagnosticTemplate
    └── NewsTemplate
```

## Implementation Priority

### Phase 1 - Core Templates (Week 1-2)
1. Service Detail Template
2. Product Detail Template
3. Location Detail Template
4. Category Index Template

### Phase 2 - Supporting Templates (Week 3-4)
1. FAQ Template
2. Pricing Template
3. Blog Post Template
4. Business Service Template

### Phase 3 - Components (Week 5-6)
1. Pricing Tables Component
2. FAQ Component
3. Process Steps Component
4. Trust Indicators Component

### Phase 4 - Integration (Week 7-8)
1. Template Inheritance System
2. Variable Management
3. Content Migration Scripts
4. Documentation & Training

This comprehensive template system will ensure consistency across all 100+ pages while maintaining the flexibility needed for different content types and business requirements.
