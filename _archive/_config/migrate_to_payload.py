#!/usr/bin/env python3
"""
Migration script to implement new Payload CMS structure
Processes existing content and adds new required fields
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime

class PayloadMigration:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "_config"
        self.migration_log = []
        
    def load_config(self, config_file):
        """Load YAML configuration file"""
        config_path = self.config_dir / config_file
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return None
        
    def migrate_globals(self):
        """Create global settings from existing configurations"""
        print("🔄 Migrating global settings...")
        
        # Load existing contact configuration
        contact_config = self.load_config('contact.yml')
        
        if contact_config:
            # Transform to new global structure
            globals_data = {
                'site-settings': {
                    'siteName': 'Regulujemy.pl',
                    'tagline': contact_config.get('company', {}).get('tagline', '')
                }
            }
            self.migration_log.append("✅ Migrated contact.yml to globals")
            return globals_data
        return None
    def create_block_templates(self):
        """Generate TypeScript templates for blocks"""
        print("🔄 Creating block templates...")
        
        blocks_config = self.load_config('blocks.yml')
        if not blocks_config:
            print("❌ blocks.yml not found")
            return
            
        output_dir = self.project_root / "_config" / "payload" / "blocks"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for block_key, block_data in blocks_config.get('blocks', {}).items():
            if isinstance(block_data, dict) and 'name' in block_data:
                template = self.generate_block_template(block_key, block_data)
                
                # Save template
                output_file = output_dir / f"{block_key}.ts"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(template)
                    
                self.migration_log.append(f"✅ Created block template: {block_key}")
                
    def generate_block_template(self, block_key, block_data):
        """Generate TypeScript template for a block"""
        template = f"""// {block_data.get('name', block_key)}
import {{ Block }} from 'payload/types';

export const {self.to_camel_case(block_key)}: Block = {{
  slug: '{block_data.get('slug', block_key)}',
  labels: {{
    singular: '{block_data.get('name', block_key)}',
    plural: '{block_data.get('name', block_key)}s',
  }},
  fields: [
"""
        
        # Add fields
        for field in block_data.get('fields', []):
            field_def = self.generate_field_definition(field)
            template += field_def
            
        template += """  ],
};
"""
        return template
    def generate_field_definition(self, field):
        """Generate TypeScript field definition"""
        if isinstance(field, dict):
            field_name = field.get('name', 'unnamed')
            field_type = field.get('type', 'text')
            required = field.get('required', False)
            
            field_def = f"""    {{
      name: '{field_name}',
      type: '{field_type}',"""
            
            if required:
                field_def += f"""
      required: true,"""
                
            if 'defaultValue' in field:
                default_val = field['defaultValue']
                if isinstance(default_val, str):
                    field_def += f"""
      defaultValue: '{default_val}',"""
                else:
                    field_def += f"""
      defaultValue: {json.dumps(default_val)},"""
                    
            field_def += """
    },
"""
            return field_def
        return ""
        
    def to_camel_case(self, snake_str):
        """Convert snake_case to CamelCase"""
        components = snake_str.split('_')
        return ''.join(x.title() for x in components)
        
    def create_api_routes(self):
        """Generate custom API route handlers"""
        print("🔄 Creating API route handlers...")
        
        api_config = self.load_config('api-enhancements.yml')
        if not api_config:
            print("❌ api-enhancements.yml not found")
            return
            
        output_dir = self.project_root / "_config" / "payload" / "endpoints"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for endpoint_key, endpoint_data in api_config.get('custom_endpoints', {}).items():
            template = self.generate_endpoint_template(endpoint_key, endpoint_data)
            
            output_file = output_dir / f"{endpoint_key}.ts"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(template)
                
            self.migration_log.append(f"✅ Created API endpoint: {endpoint_key}")
    def generate_endpoint_template(self, endpoint_key, endpoint_data):
        """Generate TypeScript template for API endpoint"""
        handler_name = endpoint_data.get('handler', endpoint_key)
        method = endpoint_data.get('method', 'GET')
        path = endpoint_data.get('path', f'/api/{endpoint_key}')
        
        template = f"""// {endpoint_key} API Endpoint
import {{ Request, Response }} from 'express';
import {{ Payload }} from 'payload';

export const {handler_name} = async (
  req: Request,
  res: Response,
  payload: Payload
) => {{
  try {{
    const {{ {', '.join(endpoint_data.get('params', {}).keys())} }} = req.{('body' if method == 'POST' else 'query')};
    
    // TODO: Implement {endpoint_key} logic
    
    res.status(200).json({{
      success: true,
      // Add response data based on endpoint specification
    }});
  }} catch (error) {{
    console.error('Error in {handler_name}:', error);
    res.status(500).json({{
      success: false,
      error: 'Internal server error'
    }});
  }}
}};
"""
        return template
        
    def run_migration(self):
        """Run all migration tasks"""
        print("🚀 Starting Payload CMS migration...")
        print("=" * 50)
        
        # Run migration tasks
        self.migrate_globals()
        self.create_block_templates()
        self.create_api_routes()
        
        # Save migration log
        log_file = self.config_dir / "migration_log.txt"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"Migration completed at {datetime.now()}\n")
            f.write("=" * 50 + "\n")
            for log_entry in self.migration_log:
                f.write(log_entry + "\n")
                
        print("\n✅ Migration completed!")
        print(f"📝 Log saved to: {log_file}")
        
if __name__ == "__main__":
    project_root = "/Users/tomek/Documents/Kamyki/01_ACTIVE/Projects/regulujemy-pl"
    migration = PayloadMigration(project_root)
    migration.run_migration()