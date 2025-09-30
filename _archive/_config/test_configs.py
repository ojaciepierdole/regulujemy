#!/usr/bin/env python3
"""
Test script to verify new Payload CMS configurations
"""

import os
import yaml
from pathlib import Path

def check_configurations():
    """Check if all new configuration files exist and are valid"""
    
    config_dir = Path("/Users/tomek/Documents/Kamyki/01_ACTIVE/Projects/regulujemy-pl/_config")
    
    required_files = [
        "globals.yml",
        "blocks.yml", 
        "components.yml",
        "media.yml",
        "templates.yml",
        "navigation.yml",
        "api-enhancements.yml"
    ]
    
    print("🔍 Checking Payload CMS Configuration Files")
    print("=" * 50)
    
    all_valid = True
    
    for config_file in required_files:
        config_path = config_dir / config_file
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                # Check if file has content
                if data:
                    print(f"✅ {config_file}: Valid")
                    
                    # Show summary
                    if isinstance(data, dict):
                        keys = list(data.keys())
                        print(f"   → Keys: {', '.join(keys[:3])}")
                else:
                    print(f"⚠️  {config_file}: Empty")
                    all_valid = False
                    
            except Exception as e:
                print(f"❌ {config_file}: Invalid YAML - {str(e)}")
                all_valid = False
        else:
            print(f"❌ {config_file}: Not found")
            all_valid = False
            
    print("=" * 50)
    
    if all_valid:
        print("✅ All configuration files are valid!")
    else:
        print("⚠️  Some configuration files need attention")
        
    return all_valid

if __name__ == "__main__":
    check_configurations()