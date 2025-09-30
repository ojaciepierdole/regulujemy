// types/payload-types.ts
// Auto-generated types for Payload CMS collections and globals

export interface Service {
  id: string;
  title: string;
  slug: string;
  description: string;
  content: any; // Lexical content
  category: string;
  priceFrom: number;
  priceUnit: string;
  duration: string;
  emergencyAvailable: boolean;
  availability: {
    weekdays: string;
    saturday: string;
    sunday: string;
    emergency247: boolean;
  };
  responseTime: number;
  meta: {
    description: string;
    keywords: string;
  };
  isActive: boolean;
  isFeatured: boolean;
  publishedAt: string;
  faq: FAQ[];
  createdAt: string;
  updatedAt: string;
}

export interface Product {
  id: string;
  name: string;
  slug: string;
  description: string;
  fullDescription: any; // Lexical content
  category: string;
  sku: string;
  priceFrom?: number;
  priceUnit: string;
  inStock: boolean;
  stockQuantity: number;
  meta: {
    description: string;
    keywords: string;
  };
  isActive: boolean;
  isFeatured: boolean;
  publishedAt: string;
  createdAt: string;
  updatedAt: string;
}

export interface FAQ {
  id: string;
  question: string;
  answer: any; // Lexical content
  category: 'service' | 'product' | 'general';
  priority: number;
  isActive: boolean;
  relatedContent: {
    services: Service[];
    products: Product[];
    packages: Package[];
    locations: Location[];
  };
  searchKeywords: Array<{
    keyword: string;
    id: string;
  }>;
  metadata: {
    source: string;
    originalMarkdownPath: string;
    lastUpdated: string;
  };
  seo: {
    metaTitle: string;
    metaDescription: string;
  };
  slug: string;
  createdAt: string;
  updatedAt: string;
}

export interface Location {
  id: string;
  name: string;
  slug: string;
  city: string;
  district: string;
  description: any; // Lexical content
  coordinates: {
    latitude: number;
    longitude: number;
  };
  phone: string;
  email: string;
  responseTime: {
    min: number;
    max: number;
    emergency: number;
  };
  serviceAreas: Array<{
    area: string;
    additionalFee: number;
    id: string;
  }>;
  specialties: Array<{
    specialty: string;
    id: string;
  }>;
  teamMembers: any[];
  workingHours: {
    standard: string;
    emergency: string;
    notes: string;
  };
  isMain: boolean;
  isActive: boolean;
  priority: number;
  createdAt: string;
  updatedAt: string;
}

export interface Package {
  id: string;
  name: string;
  slug: string;
  description: string;
  content: any; // Lexical content
  packageType: string;
  duration: string;
  totalPrice: number;
  paymentTerms: {
    paymentMethod: string;
    validityPeriod: number;
  };
  pricingItems: any[];
  markdownContent: {
    detailedDescription: any;
    processSteps: any;
    guaranteeInfo: any;
  };
  ctaBlocks: any;
  isPromoted: boolean;
  promotionDetails: any;
  meta: {
    title: string;
    description: string;
    keywords: string;
  };
  isActive: boolean;
  isFeatured: boolean;
  popularityScore: number;
  publishedAt: string;
  createdAt: string;
  updatedAt: string;
}
