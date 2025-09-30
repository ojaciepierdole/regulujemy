#!/usr/bin/env python3
"""
Test script for Contact Section Templates
Validates template syntax and data integration
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

class TemplateValidator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.errors = []
        self.warnings = []
        self.successes = []
    
    def validate_all(self):
        """Run all validation checks"""
        print("🔍 Starting Contact Template Validation...\n")
        
        # Check 1: Config files exist
        self.check_config_files()
        
        # Check 2: Template files exist
        self.check_template_files()
        
        # Check 3: YAML syntax in templates
        self.check_yaml_syntax()
        
        # Check 4: Template variable references
        self.check_template_variables()
        
        # Check 5: Contact data consistency
        self.check_contact_data()
        
        # Check 6: Example implementations
        self.check_examples()
        
        # Report results
        self.print_report()
    
    def check_config_files(self):
        """Verify all required config files exist"""
        required_configs = [
            '_config/contact.yml',
            '_config/content-structure.yml',
            '_config/assets.yml',
            '_config/content-relationships.yml'
        ]
        
        for config in required_configs:
            path = self.base_path / config
            if path.exists():
                self.successes.append(f"✅ Config found: {config}")
            else:
                self.errors.append(f"❌ Missing config: {config}")
    
    def check_template_files(self):
        """Verify template files exist"""
        template_files = [
            '_templates/components/contact-section.md',
            '_templates/components/contact-variants.md',
            '_templates/components/contact-usage-guide.md'
        ]
        
        for template in template_files:
            path = self.base_path / template
            if path.exists():
                self.successes.append(f"✅ Template found: {template}")
                # Check file size
                size = path.stat().st_size
                if size < 100:
                    self.warnings.append(f"⚠️  Template seems too small: {template} ({size} bytes)")
            else:
                self.errors.append(f"❌ Missing template: {template}")
    
    def check_yaml_syntax(self):
        """Validate YAML syntax in templates"""
        template_path = self.base_path / '_templates/components/contact-section.md'
        
        if not template_path.exists():
            return
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract YAML frontmatter
        yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            try:
                data = yaml.safe_load(yaml_content)
                self.successes.append("✅ Template YAML syntax is valid")
                
                # Check for required sections
                required_sections = ['component', 'section', 'heading', 'contact_cards']
                for section in required_sections:
                    if section in data:
                        self.successes.append(f"✅ Found required section: {section}")
                    else:
                        self.errors.append(f"❌ Missing required section: {section}")
                        
            except yaml.YAMLError as e:
                self.errors.append(f"❌ YAML syntax error in template: {str(e)}")
        else:
            self.errors.append("❌ No YAML frontmatter found in template")
    
    def check_template_variables(self):
        """Check for proper template variable usage"""
        template_path = self.base_path / '_templates/components/contact-section.md'
        
        if not template_path.exists():
            return
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Obsidian Templater syntax
        templater_vars = re.findall(r'{{(\w+(?:\.\w+)*?)}}', content)
        if templater_vars:
            self.successes.append(f"✅ Found {len(templater_vars)} template variables")
            
            # Check for common variables
            expected_vars = ['section.id', 'heading.text', 'contact_cards.primary.title']
            for var in expected_vars:
                if var in content:
                    self.successes.append(f"✅ Found expected variable: {var}")
                else:
                    self.warnings.append(f"⚠️  Missing expected variable: {var}")
        
        # Check for contact.yml references
        contact_refs = re.findall(r'<%.*?contact\.yml.*?%>', content, re.DOTALL)
        if contact_refs:
            self.successes.append(f"✅ Found {len(contact_refs)} contact.yml references")
        else:
            self.warnings.append("⚠️  No contact.yml references found")
    
    def check_contact_data(self):
        """Validate contact.yml data structure"""
        contact_path = self.base_path / '_config/contact.yml'
        
        if not contact_path.exists():
            return
        
        with open(contact_path, 'r', encoding='utf-8') as f:
            contact_data = yaml.safe_load(f)
        
        # Check required fields
        required_fields = {
            'company': ['name', 'tagline'],
            'primary': ['phone', 'phone_display', 'email'],
            'departments': ['main', 'emergency', 'business'],
            'warsaw_districts': ['mokotow', 'ursynow', 'wilanow']
        }
        
        for section, fields in required_fields.items():
            if section in contact_data:
                self.successes.append(f"✅ Found section: {section}")
                for field in fields:
                    if field in contact_data[section]:
                        self.successes.append(f"✅ Found field: {section}.{field}")
                    else:
                        self.errors.append(f"❌ Missing field: {section}.{field}")
            else:
                self.errors.append(f"❌ Missing section: {section}")
        
        # Check phone number formats
        phone_pattern = re.compile(r'^\+?48?\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}$')
        phones_to_check = [
            contact_data.get('primary', {}).get('phone', ''),
            contact_data.get('primary', {}).get('phone_emergency', '')
        ]
        
        for phone in phones_to_check:
            if phone and phone_pattern.match(phone):
                self.successes.append(f"✅ Valid phone format: {phone}")
            elif phone:
                self.warnings.append(f"⚠️  Questionable phone format: {phone}")
    
    def check_examples(self):
        """Validate example implementations"""
        examples_dir = self.base_path / '_templates/examples'
        
        if not examples_dir.exists():
            self.warnings.append("⚠️  No examples directory found")
            return
        
        example_files = list(examples_dir.glob('*.md'))
        if example_files:
            self.successes.append(f"✅ Found {len(example_files)} example files")
            
            for example in example_files:
                with open(example, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for template insertion
                if '{{tp:insert _templates/components/contact-section.md}}' in content:
                    self.successes.append(f"✅ Example uses template: {example.name}")
                else:
                    self.warnings.append(f"⚠️  Example doesn't use template: {example.name}")
                
                # Check for contact_config
                if 'contact_config:' in content:
                    self.successes.append(f"✅ Example has contact_config: {example.name}")
        else:
            self.warnings.append("⚠️  No example files found")
    
    def print_report(self):
        """Print validation report"""
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)
        
        print(f"\n✅ Successes: {len(self.successes)}")
        if len(self.successes) <= 20:
            for success in self.successes:
                print(f"   {success}")
        else:
            print(f"   (showing first 10 of {len(self.successes)})")
            for success in self.successes[:10]:
                print(f"   {success}")
        
        print(f"\n⚠️  Warnings: {len(self.warnings)}")
        for warning in self.warnings:
            print(f"   {warning}")
        
        print(f"\n❌ Errors: {len(self.errors)}")
        for error in self.errors:
            print(f"   {error}")
        
        # Overall status
        print("\n" + "="*60)
        if not self.errors:
            print("✅ VALIDATION PASSED - Templates are ready to use!")
        elif len(self.errors) < 3:
            print("⚠️  VALIDATION PASSED WITH WARNINGS - Minor issues to fix")
        else:
            print("❌ VALIDATION FAILED - Please fix errors before using templates")
        print("="*60)
        
        # Usage instructions
        if not self.errors:
            print("\n📝 NEXT STEPS:")
            print("1. Run migration script to update existing files:")
            print("   python _templates/migrate-contact-sections.py --dry-run")
            print("\n2. Test on a single file first:")
            print("   python _templates/migrate-contact-sections.py --file index.md")
            print("\n3. Review the examples in _templates/examples/")
            print("\n4. When ready, run full migration:")
            print("   python _templates/migrate-contact-sections.py")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate contact section templates")
    parser.add_argument('--path', default='/Users/tomek/Documents/Kamyki/Regulujemy.pl',
                        help='Base path of the project')
    
    args = parser.parse_args()
    
    validator = TemplateValidator(args.path)
    validator.validate_all()
