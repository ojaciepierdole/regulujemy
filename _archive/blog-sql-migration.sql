-- 🗄️ SQL MIGRATION SCRIPT - BLOG COLLECTION
-- Directus CMS - Regulujemy.pl
-- Version: 1.0
-- Date: August 2025

-- ============================================
-- 1. CREATE MAIN BLOG TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS blog (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'scheduled', 'archived')),
    sort INTEGER,
    published_at TIMESTAMP,
    scheduled_for TIMESTAMP,
    
    -- Content fields (PL)
    title VARCHAR(120) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    excerpt TEXT,
    content TEXT,
    featured_image UUID REFERENCES directus_files(id) ON DELETE SET NULL,
    
    -- Content fields (EN)
    title_en VARCHAR(120),
    slug_en VARCHAR(255) UNIQUE,
    excerpt_en TEXT,
    content_en TEXT,
    
    -- Categorization
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(100),
    tags JSONB DEFAULT '[]'::jsonb,
    type VARCHAR(20) DEFAULT 'article',
    
    -- Author metadata
    author UUID REFERENCES directus_users(id) ON DELETE SET NULL,
    author_bio TEXT,
    reviewer UUID REFERENCES directus_users(id) ON DELETE SET NULL,
    
    -- SEO fields
    seo_title VARCHAR(60),
    seo_title_en VARCHAR(60),
    seo_description VARCHAR(160),
    seo_description_en VARCHAR(160),
    seo_keywords JSONB DEFAULT '[]'::jsonb,
    seo_keywords_en JSONB DEFAULT '[]'::jsonb,
    og_image UUID REFERENCES directus_files(id) ON DELETE SET NULL,
    canonical_url VARCHAR(500),
    noindex BOOLEAN DEFAULT FALSE,
    
    -- Article properties
    reading_time INTEGER DEFAULT 0,
    word_count INTEGER DEFAULT 0,
    difficulty_level VARCHAR(20) DEFAULT 'beginner',
    target_audience JSONB DEFAULT '[]'::jsonb,
    
    -- Dynamic components
    faq_blocks JSONB DEFAULT '[]'::jsonb,
    testimonial_blocks JSONB DEFAULT '[]'::jsonb,
    show_toc BOOLEAN DEFAULT TRUE,
    show_author BOOLEAN DEFAULT TRUE,
    show_share_buttons BOOLEAN DEFAULT TRUE,
    show_related BOOLEAN DEFAULT TRUE,
    enable_comments BOOLEAN DEFAULT FALSE,
    
    -- CTA fields
    cta_type VARCHAR(20),
    cta_title VARCHAR(255),
    cta_description TEXT,
    cta_button_text VARCHAR(50),
    cta_button_url VARCHAR(500),
    cta_service UUID REFERENCES services(id) ON DELETE SET NULL,
    
    -- Metrics
    view_count INTEGER DEFAULT 0,
    unique_visitors INTEGER DEFAULT 0,
    avg_time_on_page INTEGER DEFAULT 0,
    bounce_rate DECIMAL(5,2) DEFAULT 0,
    share_count JSONB DEFAULT '{"facebook":0,"twitter":0,"linkedin":0}'::jsonb,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_blog_status ON blog(status);
CREATE INDEX idx_blog_published_at ON blog(published_at);
CREATE INDEX idx_blog_category ON blog(category);
CREATE INDEX idx_blog_slug ON blog(slug);
CREATE INDEX idx_blog_slug_en ON blog(slug_en);
CREATE INDEX idx_blog_author ON blog(author);
CREATE INDEX idx_blog_deleted_at ON blog(deleted_at);

-- ============================================
-- 2. CREATE JUNCTION TABLES FOR M2M RELATIONS
-- ============================================

-- Blog ↔ Services
CREATE TABLE IF NOT EXISTS blog_services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blog_id UUID NOT NULL REFERENCES blog(id) ON DELETE CASCADE,
    service_id UUID NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    relevance_score INTEGER DEFAULT 5,
    sort INTEGER,
    UNIQUE(blog_id, service_id)
);

CREATE INDEX idx_blog_services_blog ON blog_services(blog_id);
CREATE INDEX idx_blog_services_service ON blog_services(service_id);

-- Blog ↔ Products
CREATE TABLE IF NOT EXISTS blog_products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blog_id UUID NOT NULL REFERENCES blog(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    is_featured BOOLEAN DEFAULT FALSE,
    sort INTEGER,
    UNIQUE(blog_id, product_id)
);

CREATE INDEX idx_blog_products_blog ON blog_products(blog_id);
CREATE INDEX idx_blog_products_product ON blog_products(product_id);

-- Blog ↔ Locations
CREATE TABLE IF NOT EXISTS blog_locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blog_id UUID NOT NULL REFERENCES blog(id) ON DELETE CASCADE,
    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    sort INTEGER,
    UNIQUE(blog_id, location_id)
);

CREATE INDEX idx_blog_locations_blog ON blog_locations(blog_id);
CREATE INDEX idx_blog_locations_location ON blog_locations(location_id);

-- Blog ↔ Blog (self-referential for related posts)
CREATE TABLE IF NOT EXISTS related_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES blog(id) ON DELETE CASCADE,
    related_post_id UUID NOT NULL REFERENCES blog(id) ON DELETE CASCADE,
    relation_type VARCHAR(50) DEFAULT 'similar', -- 'similar', 'sequel', 'prerequisite'
    sort INTEGER,
    UNIQUE(post_id, related_post_id),
    CHECK (post_id != related_post_id)
);

CREATE INDEX idx_related_posts_post ON related_posts(post_id);
CREATE INDEX idx_related_posts_related ON related_posts(related_post_id);

-- Blog ↔ FAQ (M2M for flexible FAQ assignment)
CREATE TABLE IF NOT EXISTS blog_faq (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blog_id UUID NOT NULL REFERENCES blog(id) ON DELETE CASCADE,
    faq_id UUID NOT NULL REFERENCES faq(id) ON DELETE CASCADE,
    sort INTEGER,
    UNIQUE(blog_id, faq_id)
);

CREATE INDEX idx_blog_faq_blog ON blog_faq(blog_id);
CREATE INDEX idx_blog_faq_faq ON blog_faq(faq_id);

-- Blog ↔ Testimonials (M2M)
CREATE TABLE IF NOT EXISTS blog_testimonials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blog_id UUID NOT NULL REFERENCES blog(id) ON DELETE CASCADE,
    testimonial_id UUID NOT NULL REFERENCES testimonials(id) ON DELETE CASCADE,
    sort INTEGER,
    UNIQUE(blog_id, testimonial_id)
);

CREATE INDEX idx_blog_testimonials_blog ON blog_testimonials(blog_id);
CREATE INDEX idx_blog_testimonials_testimonial ON blog_testimonials(testimonial_id);

-- Blog ↔ Gallery Images (M2M)
CREATE TABLE IF NOT EXISTS blog_gallery (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blog_id UUID NOT NULL REFERENCES blog(id) ON DELETE CASCADE,
    directus_files_id UUID NOT NULL REFERENCES directus_files(id) ON DELETE CASCADE,
    sort INTEGER,
    caption TEXT,
    alt_text VARCHAR(255)
);

CREATE INDEX idx_blog_gallery_blog ON blog_gallery(blog_id);
CREATE INDEX idx_blog_gallery_file ON blog_gallery(directus_files_id);

-- Blog ↔ Co-authors (M2M with users)
CREATE TABLE IF NOT EXISTS blog_coauthors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    blog_id UUID NOT NULL REFERENCES blog(id) ON DELETE CASCADE,
    directus_users_id UUID NOT NULL REFERENCES directus_users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'coauthor',
    sort INTEGER,
    UNIQUE(blog_id, directus_users_id)
);

CREATE INDEX idx_blog_coauthors_blog ON blog_coauthors(blog_id);
CREATE INDEX idx_blog_coauthors_user ON blog_coauthors(directus_users_id);

-- ============================================
-- 3. CREATE TRIGGERS FOR AUTOMATION
-- ============================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_blog_updated_at 
    BEFORE UPDATE ON blog 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Auto-generate slug from title
CREATE OR REPLACE FUNCTION generate_slug()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.slug IS NULL OR NEW.slug = '' THEN
        NEW.slug = lower(
            regexp_replace(
                regexp_replace(
                    regexp_replace(
                        regexp_replace(
                            NEW.title,
                            '[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]',
                            CASE 
                                WHEN substring(NEW.title from '[ąĄ]') IS NOT NULL THEN 'a'
                                WHEN substring(NEW.title from '[ćĆ]') IS NOT NULL THEN 'c'
                                WHEN substring(NEW.title from '[ęĘ]') IS NOT NULL THEN 'e'
                                WHEN substring(NEW.title from '[łŁ]') IS NOT NULL THEN 'l'
                                WHEN substring(NEW.title from '[ńŃ]') IS NOT NULL THEN 'n'
                                WHEN substring(NEW.title from '[óÓ]') IS NOT NULL THEN 'o'
                                WHEN substring(NEW.title from '[śŚ]') IS NOT NULL THEN 's'
                                WHEN substring(NEW.title from '[źŹżŻ]') IS NOT NULL THEN 'z'
                            END,
                            'g'
                        ),
                        '[^a-z0-9\s-]', '', 'g'
                    ),
                    '\s+', '-', 'g'
                ),
                '^-+|-+$', '', 'g'
            )
        );
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER generate_blog_slug 
    BEFORE INSERT ON blog 
    FOR EACH ROW 
    EXECUTE FUNCTION generate_slug();

-- Calculate reading time and word count
CREATE OR REPLACE FUNCTION calculate_reading_metrics()
RETURNS TRIGGER AS $$
DECLARE
    plain_text TEXT;
    word_count_val INTEGER;
BEGIN
    IF NEW.content IS NOT NULL THEN
        -- Remove HTML tags
        plain_text := regexp_replace(NEW.content, '<[^>]*>', '', 'g');
        -- Count words
        word_count_val := array_length(string_to_array(plain_text, ' '), 1);
        
        NEW.word_count := COALESCE(word_count_val, 0);
        NEW.reading_time := CEIL(COALESCE(word_count_val, 0) / 200.0);
        
        -- Auto-generate excerpt if missing
        IF NEW.excerpt IS NULL OR NEW.excerpt = '' THEN
            NEW.excerpt := CASE 
                WHEN length(plain_text) > 297 THEN 
                    substring(plain_text from 1 for 297) || '...'
                ELSE 
                    plain_text
            END;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER calculate_blog_metrics 
    BEFORE INSERT OR UPDATE ON blog 
    FOR EACH ROW 
    EXECUTE FUNCTION calculate_reading_metrics();

-- ============================================
-- 4. CREATE VIEWS FOR COMMON QUERIES
-- ============================================

-- Published posts view
CREATE OR REPLACE VIEW blog_published AS
SELECT * FROM blog
WHERE status = 'published' 
  AND published_at <= CURRENT_TIMESTAMP
  AND deleted_at IS NULL
ORDER BY published_at DESC;

-- Popular posts view
CREATE OR REPLACE VIEW blog_popular AS
SELECT * FROM blog
WHERE status = 'published'
  AND deleted_at IS NULL
ORDER BY view_count DESC
LIMIT 10;

-- Recent posts by category
CREATE OR REPLACE VIEW blog_by_category AS
SELECT 
    category,
    COUNT(*) as post_count,
    MAX(published_at) as latest_post,
    AVG(reading_time) as avg_reading_time,
    SUM(view_count) as total_views
FROM blog
WHERE status = 'published'
  AND deleted_at IS NULL
GROUP BY category;

-- ============================================
-- 5. INSERT SAMPLE DATA
-- ============================================

-- Sample blog posts
INSERT INTO blog (
    title, category, type, status, published_at,
    excerpt, content, seo_title, seo_description,
    difficulty_level, target_audience
) VALUES 
(
    'Jak prawidłowo wyregulować okna PCV przed zimą',
    'poradniki',
    'guide',
    'published',
    CURRENT_TIMESTAMP,
    'Dowiedz się, jak samodzielnie wyregulować okna PCV przed nadchodzącą zimą. Praktyczny poradnik krok po kroku z ilustracjami.',
    '<h2>Dlaczego regulacja okien jest ważna?</h2><p>Prawidłowa regulacja okien PCV jest kluczowa dla zachowania ich szczelności...</p>',
    'Regulacja okien PCV przed zimą - Poradnik 2025',
    'Praktyczny poradnik jak wyregulować okna PCV przed zimą. Instrukcja krok po kroku.',
    'intermediate',
    '["homeowner", "tenant"]'::jsonb
),
(
    'Dlaczego okna się pocą? Przyczyny i rozwiązania',
    'diagnostyka',
    'article',
    'published',
    CURRENT_TIMESTAMP - INTERVAL '3 days',
    'Poznaj główne przyczyny pocenia się okien i skuteczne sposoby rozwiązania tego problemu.',
    '<h2>Skąd bierze się wilgoć na oknach?</h2><p>Pocenie się okien to częsty problem...</p>',
    'Pocenie się okien - przyczyny i rozwiązania',
    'Dlaczego okna się pocą? Poznaj przyczyny i rozwiązania problemu z wilgocią.',
    'beginner',
    '["homeowner", "tenant", "property_manager"]'::jsonb
),
(
    'Modernizacja okien w kamienicy - case study',
    'realizacje',
    'case-studies',
    'published',
    CURRENT_TIMESTAMP - INTERVAL '7 days',
    'Zobacz jak przeprowadziliśmy kompleksową modernizację okien w zabytkowej kamienicy na Mokotowie.',
    '<h2>Wyzwanie</h2><p>Kamienica z 1930 roku wymagała wymiany wszystkich okien...</p>',
    'Modernizacja okien w kamienicy - Case Study',
    'Kompleksowa modernizacja okien w zabytkowej kamienicy. Zobacz efekty naszej pracy.',
    'advanced',
    '["property_manager", "business", "architect"]'::jsonb
);

-- ============================================
-- 6. GRANT PERMISSIONS
-- ============================================

-- Grant permissions for Directus roles
GRANT SELECT ON blog TO directus_reader;
GRANT SELECT, INSERT, UPDATE ON blog TO directus_editor;
GRANT ALL PRIVILEGES ON blog TO directus_admin;

GRANT SELECT ON blog_services TO directus_reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON blog_services TO directus_editor;
GRANT ALL PRIVILEGES ON blog_services TO directus_admin;

GRANT SELECT ON blog_products TO directus_reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON blog_products TO directus_editor;
GRANT ALL PRIVILEGES ON blog_products TO directus_admin;

GRANT SELECT ON blog_locations TO directus_reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON blog_locations TO directus_editor;
GRANT ALL PRIVILEGES ON blog_locations TO directus_admin;

GRANT SELECT ON related_posts TO directus_reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON related_posts TO directus_editor;
GRANT ALL PRIVILEGES ON related_posts TO directus_admin;

-- Grant permissions on views
GRANT SELECT ON blog_published TO directus_reader;
GRANT SELECT ON blog_popular TO directus_reader;
GRANT SELECT ON blog_by_category TO directus_reader;

-- ============================================
-- 7. HELPFUL QUERIES FOR ADMINISTRATORS
-- ============================================

-- Get all published posts with relations count
/*
SELECT 
    b.id,
    b.title,
    b.category,
    b.published_at,
    b.view_count,
    COUNT(DISTINCT bs.service_id) as related_services_count,
    COUNT(DISTINCT bp.product_id) as related_products_count,
    COUNT(DISTINCT bl.location_id) as related_locations_count
FROM blog b
LEFT JOIN blog_services bs ON b.id = bs.blog_id
LEFT JOIN blog_products bp ON b.id = bp.blog_id
LEFT JOIN blog_locations bl ON b.id = bl.blog_id
WHERE b.status = 'published'
GROUP BY b.id, b.title, b.category, b.published_at, b.view_count
ORDER BY b.published_at DESC;
*/

-- Get posts needing translation
/*
SELECT id, title, category, published_at
FROM blog
WHERE status = 'published'
  AND (title_en IS NULL OR content_en IS NULL)
ORDER BY view_count DESC;
*/

-- Get posts by author with metrics
/*
SELECT 
    u.first_name || ' ' || u.last_name as author_name,
    COUNT(b.id) as posts_count,
    SUM(b.view_count) as total_views,
    AVG(b.reading_time) as avg_reading_time,
    MAX(b.published_at) as last_post
FROM blog b
JOIN directus_users u ON b.author = u.id
WHERE b.status = 'published'
GROUP BY u.id, u.first_name, u.last_name
ORDER BY posts_count DESC;
*/

-- Find posts with broken relations
/*
SELECT 
    'blog_services' as table_name,
    bs.blog_id,
    bs.service_id
FROM blog_services bs
LEFT JOIN blog b ON bs.blog_id = b.id
LEFT JOIN services s ON bs.service_id = s.id
WHERE b.id IS NULL OR s.id IS NULL

UNION ALL

SELECT 
    'blog_products' as table_name,
    bp.blog_id,
    bp.product_id
FROM blog_products bp
LEFT JOIN blog b ON bp.blog_id = b.id
LEFT JOIN products p ON bp.product_id = p.id
WHERE b.id IS NULL OR p.id IS NULL;
*/

-- ============================================
-- 8. ROLLBACK SCRIPT (IF NEEDED)
-- ============================================

/*
-- TO ROLLBACK THIS MIGRATION, RUN:

DROP VIEW IF EXISTS blog_by_category CASCADE;
DROP VIEW IF EXISTS blog_popular CASCADE;
DROP VIEW IF EXISTS blog_published CASCADE;

DROP TRIGGER IF EXISTS calculate_blog_metrics ON blog;
DROP TRIGGER IF EXISTS generate_blog_slug ON blog;
DROP TRIGGER IF EXISTS update_blog_updated_at ON blog;

DROP FUNCTION IF EXISTS calculate_reading_metrics() CASCADE;
DROP FUNCTION IF EXISTS generate_slug() CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

DROP TABLE IF EXISTS blog_coauthors CASCADE;
DROP TABLE IF EXISTS blog_gallery CASCADE;
DROP TABLE IF EXISTS blog_testimonials CASCADE;
DROP TABLE IF EXISTS blog_faq CASCADE;
DROP TABLE IF EXISTS related_posts CASCADE;
DROP TABLE IF EXISTS blog_locations CASCADE;
DROP TABLE IF EXISTS blog_products CASCADE;
DROP TABLE IF EXISTS blog_services CASCADE;
DROP TABLE IF EXISTS blog CASCADE;
*/

-- ============================================
-- END OF MIGRATION SCRIPT
-- ============================================

-- Migration completed successfully!
-- Remember to:
-- 1. Configure Directus permissions through admin panel
-- 2. Set up webhook automation for scheduled posts
-- 3. Test all triggers and functions
-- 4. Create backup before running in production
-- 5. Monitor performance with EXPLAIN ANALYZE on complex queries