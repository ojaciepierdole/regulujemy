#!/usr/bin/env python3
"""
Skrypt do analizy osieroconych plików i brakujących linków
"""

import os
import re
from collections import defaultdict

PROJECT_PATH = "/Users/tomek/Documents/Kamyki/Regulujemy.pl"

def extract_links_from_file(filepath):
    """Wyciąga wszystkie linki z pliku markdown"""
    links = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Wzorzec dla linków markdown [text](path)
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        matches = re.findall(link_pattern, content)
        
        for text, path in matches:
            # Normalizujemy ścieżkę
            if not path.startswith('http') and not path.startswith('#'):
                # Usuwamy .md z końca dla porównania
                normalized_path = path.replace('.md', '')
                links.append(normalized_path)
        
    except Exception as e:
        print(f"Błąd czytania {filepath}: {e}")
    
    return links

def get_all_files():
    """Zwraca listę wszystkich plików .md w projekcie"""
    files = []
    for root, dirs, filenames in os.walk(PROJECT_PATH):
        # Pomijamy katalogi systemowe
        if any(skip in root for skip in ['konwersja-linkow', '.git', '_archive', '_templates']):
            continue
            
        for filename in filenames:
            if filename.endswith('.md') and not filename.startswith('_'):
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, PROJECT_PATH)
                files.append(rel_path)
    
    return files

def analyze_orphaned_files():
    """Analizuje które pliki nie są linkowane z innych plików"""
    all_files = get_all_files()
    linked_files = set()
    link_map = defaultdict(list)
    
    # Dla każdego pliku sprawdzamy jakie ma linki
    for file in all_files:
        filepath = os.path.join(PROJECT_PATH, file)
        links = extract_links_from_file(filepath)
        
        for link in links:
            # Konwertujemy względną ścieżkę na absolutną względem projektu
            if link.startswith('../'):
                base_dir = os.path.dirname(file)
                resolved_path = os.path.normpath(os.path.join(base_dir, link))
            elif link.startswith('./'):
                base_dir = os.path.dirname(file)
                resolved_path = os.path.normpath(os.path.join(base_dir, link[2:]))
            else:
                base_dir = os.path.dirname(file)
                resolved_path = os.path.normpath(os.path.join(base_dir, link))
            
            resolved_path = resolved_path.replace('.md', '')
            linked_files.add(resolved_path)
            link_map[resolved_path].append(file)
    
    # Znajdujemy osierocone pliki
    orphaned = []
    for file in all_files:
        normalized_file = file.replace('.md', '')
        if normalized_file not in linked_files:
            # Sprawdzamy czy to nie jest plik główny lub specjalny
            if file not in ['index.md', 'README.md', 'MASTER-TRACKER.md', 'GEMINI.md', 'System Prompt.md']:
                orphaned.append(file)
    
    return orphaned, link_map, all_files

def check_missing_navigation(filepath):
    """Sprawdza brakujące elementy nawigacyjne w pliku"""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdzamy breadcrumbs
        if '## NAWIGACJA' not in content and not filepath.endswith('index.md'):
            issues.append("Brak sekcji nawigacyjnej (breadcrumbs)")
        
        # Sprawdzamy powiązane strony
        if 'Powiązane' not in content and 'Zobacz także' not in content and 'Powiązane strony' not in content:
            if not any(skip in filepath for skip in ['index.md', 'README.md', 'MASTER']):
                issues.append("Brak sekcji 'Powiązane strony'")
        
        # Sprawdzamy CTA
        if not any(cta in content for cta in ['[ZADZWOŃ', '[ZAMÓW', '[FORMULARZ', 'Kontakt]']):
            if 'strony/' not in filepath:
                issues.append("Brak wyraźnego CTA (call-to-action)")
        
    except Exception as e:
        issues.append(f"Błąd analizy: {e}")
    
    return issues

def main():
    """Główna funkcja analizy"""
    print("🔍 Analiza osieroconych plików i brakujących elementów nawigacyjnych\n")
    
    # Analiza osieroconych plików
    orphaned, link_map, all_files = analyze_orphaned_files()
    
    print("📁 OSIEROCONE PLIKI (nie są linkowane z innych dokumentów):\n")
    
    if orphaned:
        for file in sorted(orphaned):
            print(f"  ❌ {file}")
            # Sugerujemy gdzie powinien być link
            if 'uslugi/' in file:
                print(f"     → Powinien być linkowany z: uslugi/index.md")
            elif 'produkty/' in file:
                print(f"     → Powinien być linkowany z: produkty/index.md")
            elif 'blog/' in file:
                print(f"     → Powinien być linkowany z: blog/index.md")
            elif 'lokalizacje/' in file:
                print(f"     → Powinien być linkowany z: lokalizacje/index.md")
            print()
    else:
        print("  ✅ Wszystkie pliki są prawidłowo podlinkowane!\n")
    
    # Analiza brakujących elementów nawigacyjnych
    print("\n🔗 BRAKUJĄCE ELEMENTY NAWIGACYJNE:\n")
    
    nav_issues = defaultdict(list)
    
    for file in all_files:
        if any(skip in file for skip in ['README.md', 'MASTER-TRACKER.md', 'GEMINI.md', '_']):
            continue
            
        filepath = os.path.join(PROJECT_PATH, file)
        issues = check_missing_navigation(filepath)
        
        if issues:
            nav_issues[file] = issues
    
    if nav_issues:
        for file, issues in sorted(nav_issues.items()):
            print(f"  📄 {file}:")
            for issue in issues:
                print(f"     ⚠️  {issue}")
            print()
    else:
        print("  ✅ Wszystkie pliki mają kompletną nawigację!\n")
    
    # Podsumowanie
    print("\n📊 PODSUMOWANIE:")
    print(f"  - Wszystkich plików: {len(all_files)}")
    print(f"  - Osieroconych plików: {len(orphaned)}")
    print(f"  - Plików z brakującą nawigacją: {len(nav_issues)}")
    
    # Rekomendacje
    if orphaned or nav_issues:
        print("\n💡 REKOMENDACJE:")
        if orphaned:
            print("  1. Dodaj linki do osieroconych plików w odpowiednich indeksach kategorii")
        if nav_issues:
            print("  2. Uzupełnij brakujące elementy nawigacyjne (breadcrumbs, powiązane strony)")
            print("  3. Dodaj CTA w plikach usługowych")

if __name__ == "__main__":
    main()