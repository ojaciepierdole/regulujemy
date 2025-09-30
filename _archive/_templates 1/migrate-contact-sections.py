        # Pattern 2: Contact info in lists
        pattern2 = r'(?:^|\n)[\*\-]\s*(?:Telefon|Tel|Zadzwoń|Email|Adres|Kontakt).*?(?=\n\n|\n#|\Z)'
        
        # Pattern 3: CTA blocks with phone numbers
        pattern3 = r'(?:ZADZWOŃ|TELEFON|KONTAKT|UMÓW).*?(?:\d{2,3}[\s\-]\d{3}[\s\-]\d{2}[\s\-]\d{2}|\+48.*?\d{2})'
        
        for pattern in [pattern1, pattern2, pattern3]:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            for match in matches:
                sections.append({
                    'start': match.start(),
                    'end': match.end(),
                    'content': match.group(0),
                    'type': self._classify_section(match.group(0))
                })
        
        # Remove duplicates and overlapping sections
        sections = self._merge_overlapping_sections(sections)
        return sections
    
    def _classify_section(self, content: str) -> str:
        """Classify the type of contact section"""
        content_lower = content.lower()
        
        if 'awari' in content_lower or '24/7' in content_lower:
            return 'emergency'
        elif 'firm' in content_lower or 'biznes' in content_lower or 'b2b' in content_lower:
            return 'business'
        elif 'godzin' in content_lower or 'otwart' in content_lower:
            return 'with_hours'
        elif 'adres' in content_lower or 'ul.' in content_lower:
            return 'with_location'
        else:
            return 'standard'
    
    def _merge_overlapping_sections(self, sections: List[Dict]) -> List[Dict]:
        """Merge overlapping contact sections"""
        if not sections:
            return []
        
        # Sort by start position
        sections.sort(key=lambda x: x['start'])
        
        merged = [sections[0]]
        for current in sections[1:]:
            last = merged[-1]
            if current['start'] <= last['end']:
                # Merge overlapping sections
                last['end'] = max(last['end'], current['end'])
                last['content'] = last['content'] + '\n' + current['content']
            else:
                merged.append(current)
        
        return merged
    
    def generate_template_config(self, section: Dict, page_meta: Dict) -> str:
        """Generate appropriate template configuration based on section type"""
        section_type = section['type']
        content = section['content']
        
        # Base configuration
        config = {
            'section_id': f"contact-{page_meta.get('page_type', 'main')}",
            'heading_enabled': 'true' if re.search(r'^#{2,3}', content, re.MULTILINE) else 'false'
        }
        
        # Extract heading if present
        heading_match = re.search(r'#{2,3}\s*(.+?)(?:\n|$)', content)
        if heading_match:
            config['heading_text'] = heading_match.group(1).strip()
        
        # Configure based on section type
        if section_type == 'emergency':
            config.update({
                'primary_enabled': 'false',
                'emergency_enabled': 'true',
                'business_enabled': 'false',
                'cards_columns': '1',
                'emergency_color': 'red'
            })
        elif section_type == 'business':
            config.update({
                'primary_enabled': 'false',
                'emergency_enabled': 'false',
                'business_enabled': 'true',
                'business_title': 'Współpraca B2B',
                'cta1_text': 'Zapytaj o ofertę'
            })
        elif section_type == 'with_location':
            config.update({
                'location_enabled': 'true',
                'show_map': 'false',
                'hq_enabled': 'true'
            })
        
        # Check for district-specific content
        district_match = re.search(r'(Mokotów|Ursynów|Wilanów|Bemowo|Bielany|Wola|Śródmieście|Ochota|Praga)', content, re.IGNORECASE)
        if district_match:
            district = district_match.group(1)
            config.update({
                'district_ext_enabled': 'true',
                'district_name': district,
                'district_ext': self._get_district_extension(district)
            })
        
        # Format as YAML frontmatter addition
        yaml_config = yaml.dump({'contact_config': config}, default_flow_style=False, allow_unicode=True)
        return yaml_config
    
    def _get_district_extension(self, district: str) -> str:
        """Get district extension from contact config"""
        district_key = district.lower().replace('ó', 'o').replace('ś', 's')
        extensions = self.contact_config.get('warsaw_districts', {})
        return extensions.get(district_key, '')
    
    def migrate_file(self, filepath: Path) -> Tuple[bool, str]:
        """Migrate a single file to use contact templates"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter and body
            frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
            if frontmatter_match:
                frontmatter = frontmatter_match.group(1)
                body = frontmatter_match.group(2)
            else:
                frontmatter = ''
                body = content
            
            # Parse existing frontmatter
            fm_data = yaml.safe_load(frontmatter) if frontmatter else {}
            
            # Detect page type from frontmatter or path
            page_meta = {
                'page_type': self._detect_page_type(filepath, fm_data),
                'title': fm_data.get('title', ''),
                'category': fm_data.get('category', '')
            }
            
            # Find contact sections
            sections = self.detect_contact_section(body)
            
            if not sections:
                return False, "No contact sections found"
            
            # Process sections in reverse order to maintain positions
            modified_body = body
            for section in reversed(sections):
                # Generate template config
                template_config = self.generate_template_config(section, page_meta)
                
                # Add config to frontmatter if not exists
                if 'contact_config' not in fm_data:
                    fm_data['contact_config'] = yaml.safe_load(template_config)['contact_config']
                
                # Replace section with template call
                template_call = '\n{{tp:insert _templates/components/contact-section.md}}\n'
                modified_body = modified_body[:section['start']] + template_call + modified_body[section['end']:]
                
                self.migration_stats['sections_replaced'] += 1
            
            # Replace standalone phone numbers
            modified_body = self._replace_phone_numbers(modified_body)
            
            # Reconstruct file
            new_frontmatter = yaml.dump(fm_data, default_flow_style=False, allow_unicode=True)
            new_content = f"---\n{new_frontmatter}---\n{modified_body}"
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.migration_stats['files_processed'] += 1
            return True, "Successfully migrated"
            
        except Exception as e:
            error_msg = f"Error processing {filepath}: {str(e)}"
            self.migration_stats['errors'].append(error_msg)
            return False, error_msg
    
    def _detect_page_type(self, filepath: Path, frontmatter: Dict) -> str:
        """Detect page type from path and frontmatter"""
        path_str = str(filepath)
        
        if 'lokalizacje' in path_str:
            return 'district'
        elif 'uslugi' in path_str:
            return 'service'
        elif 'biznes' in path_str:
            return 'business'
        elif 'index.md' in path_str and filepath.parent == self.base_path:
            return 'homepage'
        elif 'kontakt' in path_str:
            return 'contact'
        else:
            return 'standard'
    
    def _replace_phone_numbers(self, content: str) -> str:
        """Replace standalone phone numbers with template references"""
        for pattern, phone_type in self.phone_patterns:
            if phone_type == 'placeholder' or phone_type == 'local':
                replacement = '{{contact.primary.phone_display}}'
            elif phone_type == 'international':
                replacement = '{{contact.primary.phone}}'
            elif phone_type == 'emergency':
                replacement = '{{contact.emergency.phone}}'
            else:
                replacement = '{{contact.primary.phone_display}}'
            
            count = len(pattern.findall(content))
            if count > 0:
                content = pattern.sub(replacement, content)
                self.migration_stats['phones_replaced'] += count
        
        return content
    
    def run_migration(self, dry_run: bool = True):
        """Run migration on all markdown files"""
        print(f"Starting contact section migration...")
        print(f"Base path: {self.base_path}")
        print(f"Dry run: {dry_run}")
        print("-" * 50)
        
        # Find all markdown files
        md_files = list(self.base_path.rglob("*.md"))
        md_files = [f for f in md_files if '_templates' not in str(f) and '_config' not in str(f)]
        
        print(f"Found {len(md_files)} markdown files to process")
        
        for filepath in md_files:
            if dry_run:
                # Just detect and report
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                sections = self.detect_contact_section(content)
                if sections:
                    print(f"\n{filepath.relative_to(self.base_path)}:")
                    print(f"  - Found {len(sections)} contact section(s)")
                    for i, section in enumerate(sections):
                        print(f"    Section {i+1}: {section['type']}")
            else:
                # Actually migrate
                success, message = self.migrate_file(filepath)
                if success:
                    print(f"✓ {filepath.relative_to(self.base_path)}")
                else:
                    print(f"✗ {filepath.relative_to(self.base_path)}: {message}")
        
        # Print summary
        print("\n" + "=" * 50)
        print("Migration Summary:")
        print(f"Files processed: {self.migration_stats['files_processed']}")
        print(f"Sections replaced: {self.migration_stats['sections_replaced']}")
        print(f"Phone numbers replaced: {self.migration_stats['phones_replaced']}")
        print(f"Errors: {len(self.migration_stats['errors'])}")
        
        if self.migration_stats['errors']:
            print("\nErrors:")
            for error in self.migration_stats['errors']:
                print(f"  - {error}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate contact sections to template system")
    parser.add_argument('--path', default='/Users/tomek/Documents/Kamyki/Regulujemy.pl', 
                        help='Base path of the project')
    parser.add_argument('--dry-run', action='store_true', 
                        help='Run in dry-run mode (no changes)')
    parser.add_argument('--file', help='Migrate single file only')
    
    args = parser.parse_args()
    
    migrator = ContactMigrator(args.path)
    
    if args.file:
        # Single file migration
        filepath = Path(args.file)
        if filepath.exists():
            success, message = migrator.migrate_file(filepath)
            print(f"Result: {message}")
        else:
            print(f"File not found: {filepath}")
    else:
        # Full migration
        migrator.run_migration(dry_run=args.dry_run)
