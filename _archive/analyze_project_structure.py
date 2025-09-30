#!/usr/bin/env python3
"""
Analiza kompletności frontmatter i struktury treści
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict, Counter
import json

class ProjectAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.files_analyzed = 0
        self.frontmatter_stats = defaultdict(Counter)
        self.content_patterns = defaultdict(list)
        self.category_structures = defaultdict(list)
        self.issues = []
        
    def analyze_all_files(self):
        """Analizuje wszystkie pliki markdown w projekcie"""
        md_files = []
        for root, dirs, files in os.walk(self.base_path):
            # Pomijamy _archive i _templates
            if '_archive' in root or '_templates' in root:
                continue
            for file in files:
                if file.endswith('.md'):
                    md_files.append(Path(root) / file)
        
        print(f"Znaleziono {len(md_files)} plików markdown do analizy\n")
        
        for file_path in md_files:
            self.analyze_file(file_path)
            
        return self.generate_report()
    
    def analyze_file(self, file_path):
        """Analizuje pojedynczy plik"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.files_analyzed += 1
            relative_path = file_path.relative_to(self.base_path)
            category = self._get_category(relative_path)
            
            # Analiza frontmatter
            frontmatter = self._extract_frontmatter(content)
            if frontmatter:
                self._analyze_frontmatter(frontmatter, category, relative_path)
            else:
                self.issues.append(f"BRAK FRONTMATTER: {relative_path}")
            
            # Analiza struktury treści
            self._analyze_content_structure(content, category, relative_path)
            
        except Exception as e:
            self.issues.append(f"BŁĄD ANALIZY {file_path}: {str(e)}")
    
    def _get_category(self, relative_path):
        """Określa kategorię pliku na podstawie ścieżki"""
        parts = relative_path.parts
        if len(parts) > 1:
            return parts[0]
        return 'root'
    
    def _extract_frontmatter(self, content):
        """Wyciąga frontmatter z pliku"""
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except:
                return None
        return None
    
    def _analyze_frontmatter(self, frontmatter, category, file_path):
        """Analizuje pola frontmatter"""
        for key in frontmatter.keys():
            self.frontmatter_stats[category][key] += 1
        
        # Sprawdzamy wymagane pola
        required_fields = ['title', 'description', 'keywords']
        missing = [f for f in required_fields if f not in frontmatter]
        if missing:
            self.issues.append(f"BRAKUJĄCE POLA ({file_path}): {', '.join(missing)}")
            
        # Zapisujemy strukturę dla kategorii
        self.category_structures[category].append(set(frontmatter.keys()))
    
    def _analyze_content_structure(self, content, category, file_path):
        """Analizuje strukturę treści"""
        # Usuwamy frontmatter
        content_body = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Znajdujemy nagłówki
        headers = re.findall(r'^(#{1,6})\s+(.+)$', content_body, re.MULTILINE)
        header_structure = [(len(h[0]), h[1]) for h in headers]
        
        # Znajdujemy sekcje specjalne
        has_pricing = 'Cena:' in content_body or 'Cennik' in content_body
        has_process = 'Proces' in content_body or 'Jak pracujemy' in content_body
        has_faq = 'FAQ' in content_body or 'Pytania' in content_body
        has_cta = 'Zadzwoń' in content_body or 'Umów' in content_body
        
        self.content_patterns[category].append({
            'file': str(file_path),
            'headers': header_structure,
            'has_pricing': has_pricing,
            'has_process': has_process,
            'has_faq': has_faq,
            'has_cta': has_cta
        })
    
    def generate_report(self):
        """Generuje raport z analizy"""
        report = []
        report.append("="*80)
        report.append("ANALIZA KOMPLETNOŚCI PROJEKTU REGULUJEMY.PL")
        report.append("="*80)
        report.append(f"\nPrzeanalizowano plików: {self.files_analyzed}")
        
        # Analiza frontmatter po kategoriach
        report.append("\n\n## ANALIZA FRONTMATTER\n")
        
        for category, fields in sorted(self.frontmatter_stats.items()):
            report.append(f"\n### Kategoria: {category}")
            report.append(f"Plików w kategorii: {len(self.category_structures[category])}")
            
            # Pola występujące we wszystkich plikach kategorii
            if self.category_structures[category]:
                common_fields = set.intersection(*self.category_structures[category])
                report.append(f"Pola wspólne: {', '.join(sorted(common_fields))}")
            
            # Statystyki pól
            report.append("\nWystępowanie pól:")
            total_files = len(self.category_structures[category])
            for field, count in sorted(fields.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_files * 100) if total_files > 0 else 0
                report.append(f"  - {field}: {count}/{total_files} ({percentage:.1f}%)")
        
        # Analiza struktury treści
        report.append("\n\n## ANALIZA STRUKTURY TREŚCI\n")
        
        for category, patterns in self.content_patterns.items():
            if not patterns:
                continue
                
            report.append(f"\n### Kategoria: {category}")
            
            # Statystyki elementów
            total = len(patterns)
            with_pricing = sum(1 for p in patterns if p['has_pricing'])
            with_process = sum(1 for p in patterns if p['has_process'])
            with_faq = sum(1 for p in patterns if p['has_faq'])
            with_cta = sum(1 for p in patterns if p['has_cta'])
            
            report.append(f"Sekcje cenowe: {with_pricing}/{total} ({with_pricing/total*100:.1f}%)")
            report.append(f"Sekcje procesu: {with_process}/{total} ({with_process/total*100:.1f}%)")
            report.append(f"Sekcje FAQ: {with_faq}/{total} ({with_faq/total*100:.1f}%)")
            report.append(f"Sekcje CTA: {with_cta}/{total} ({with_cta/total*100:.1f}%)")
        
        # Problemy znalezione
        if self.issues:
            report.append("\n\n## ZNALEZIONE PROBLEMY\n")
            for issue in sorted(set(self.issues)):
                report.append(f"- {issue}")
        
        # Rekomendacje dla CMS
        report.append("\n\n## REKOMENDACJE DLA STRUKTURY CMS\n")
        report.append(self._generate_cms_recommendations())
        
        return "\n".join(report)
    
    def _generate_cms_recommendations(self):
        """Generuje rekomendacje dla struktury CMS"""
        recommendations = []
        
        # Analiza spójności frontmatter
        recommendations.append("### Wymagane pola frontmatter (dla wszystkich typów):")
        recommendations.append("- title (string, required)")
        recommendations.append("- description (textarea, required, max 300)")
        recommendations.append("- keywords (array of strings)")
        recommendations.append("- author (string, default: 'Tomasz Jakubowski')")
        recommendations.append("- created (date)")
        recommendations.append("- modified (date)")
        
        # Pola specyficzne dla kategorii
        recommendations.append("\n### Pola specyficzne dla kategorii:")
        
        if 'uslugi' in self.frontmatter_stats:
            recommendations.append("\n**USŁUGI:**")
            recommendations.append("- price_from (number)")
            recommendations.append("- price_to (number)")
            recommendations.append("- duration (string)")
            recommendations.append("- warranty (string)")
            recommendations.append("- category (select)")
            recommendations.append("- emergency_available (boolean)")
        
        if 'produkty' in self.frontmatter_stats:
            recommendations.append("\n**PRODUKTY:**")
            recommendations.append("- price_from (number)")
            recommendations.append("- price_unit (string)")
            recommendations.append("- brands (array)")
            recommendations.append("- warranty_years (number)")
            recommendations.append("- category (select)")
        
        if 'lokalizacje' in self.frontmatter_stats:
            recommendations.append("\n**LOKALIZACJE:**")
            recommendations.append("- district (string)")
            recommendations.append("- response_time (string)")
            recommendations.append("- team_size (number)")
            recommendations.append("- coverage_areas (array)")
        
        return "\n".join(recommendations)

if __name__ == "__main__":
    analyzer = ProjectAnalyzer("/Users/tomek/Documents/Kamyki/Regulujemy.pl")
    report = analyzer.analyze_all_files()
    
    # Zapisz raport
    with open("/Users/tomek/Documents/Kamyki/Regulujemy.pl/FRONTMATTER_ANALYSIS.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(report)
