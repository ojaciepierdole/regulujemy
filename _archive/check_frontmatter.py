
import os
import yaml

def find_markdown_files(root_dir):
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        # Exclude the _archive directory
        if '_archive' in dirpath.split(os.sep):
            continue
        for filename in filenames:
            if filename.endswith(".md"):
                markdown_files.append(os.path.join(dirpath, filename))
    return markdown_files

def check_frontmatter(file_path):
    missing_fields = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for frontmatter fences
            if content.startswith("---"):
                parts = content.split('---')
                if len(parts) > 2:
                    frontmatter = yaml.safe_load(parts[1])
                    if not isinstance(frontmatter, dict):
                        return ['no frontmatter'] # Not a valid frontmatter

                    if 'keywords' not in frontmatter or not frontmatter['keywords']:                        missing_fields.append('keywords')
                    if 'description' not in frontmatter or not frontmatter['description']:
                        missing_fields.append('description')
                else:
                    missing_fields.append('no frontmatter') # No closing fence
            else:
                missing_fields.append('no frontmatter') # No opening fence
    except Exception as e:
        # Could be a parsing error or file not found
        return [f"error: {e}"]
        
    return missing_fields

if __name__ == "__main__":
    project_root = "/Users/tomek/Documents/Kamyki/Regulujemy.pl"
    all_markdown_files = find_markdown_files(project_root)
    
    files_to_fix = {}
    for md_file in all_markdown_files:
        missing = check_frontmatter(md_file)
        if missing:
            files_to_fix[md_file] = missing
            
    if files_to_fix:
        print("Files with missing frontmatter fields:")
        for file, fields in files_to_fix.items():
            print(f"  - {file}: {', '.join(fields)}")
    else:
        print("All markdown files have complete frontmatter.")
