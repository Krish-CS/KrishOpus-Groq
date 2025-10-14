"""
ABSOLUTE FINAL Template Analyzer - UNIVERSAL VERSION
✅ Works with ALL template formats
✅ Removes ALL bracketed content (marks notation)
✅ Handles multi-line cells
✅ Splits combined sections
"""

import os
import re
from typing import List
from docx import Document


class TemplateAnalyzer:
    """Universal template analyzer - works with all formats"""
    
    def __init__(self):
        """Initialize"""
        print("✅ TemplateAnalyzer initialized (universal marks removal)")
    
    
    def detect_sections_from_marks_table(self, file_path: str) -> List[str]:
        """
        UNIVERSAL METHOD: Find marks table and extract clean section names
        """
        if not os.path.exists(file_path):
            return self._get_defaults()
        
        try:
            doc = Document(file_path)
            sections = []
            
            print(f"\n🔍 Analyzing: {os.path.basename(file_path)}")
            
            # Find table with marks notation or keywords
            for table_idx, table in enumerate(doc.tables):
                table_text = " ".join(cell.text for row in table.rows for cell in row.cells)
                
                # Check if table has marks notation OR marks keywords
                has_marks_notation = bool(re.search(r'\([0-9]+\s*[Mm]arks?\)', table_text))
                table_lower = table_text.lower()
                has_marks_keywords = any(kw in table_lower for kw in ['marks awarded', 'marks', 'objective', 'analysis', 'solution'])
                
                if has_marks_notation or has_marks_keywords:
                    print(f"   ✓ Found marks table (Table {table_idx + 1})")
                    
                    # Extract from FIRST ROW only
                    sections = self._extract_from_first_row(table)
                    
                    if sections:
                        break
            
            if sections:
                # Split combined sections
                sections = self._split_combined_sections(sections)
                
                print(f"   ✓ Extracted {len(sections)} sections:")
                for s in sections:
                    print(f"      - {s}")
                
                return sections
            else:
                print(f"   ⚠ No sections found, using defaults")
                return self._get_defaults()
                
        except Exception as e:
            print(f"   ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return self._get_defaults()
    
    
    def _extract_from_first_row(self, table) -> List[str]:
        """
        Extract sections from FIRST ROW only
        AGGRESSIVE cleaning: Remove ALL content in parentheses/brackets
        """
        if len(table.rows) == 0:
            return []
        
        sections = []
        first_row = table.rows[0]
        
        print(f"   📊 Processing {len(first_row.cells)} columns from first row...")
        
        for cell_idx, cell in enumerate(first_row.cells):
            cell_text = cell.text.strip()
            
            if not cell_text:
                continue
            
            # Step 1: Replace newlines with spaces
            cell_text = cell_text.replace('\n', ' ').replace('\r', ' ')
            cell_text = re.sub(r'\s+', ' ', cell_text).strip()
            
            print(f"      Cell {cell_idx}: '{cell_text[:50]}...'")
            
            # Step 2: AGGRESSIVELY remove ALL parentheses content
            # Removes: (5 Marks), (2), (20), (anything)
            cleaned = re.sub(r'\([^)]*\)', '', cell_text)
            
            # Step 3: Remove ALL brackets content
            # Removes: [5], [20], [anything]
            cleaned = re.sub(r'\[[^\]]*\]', '', cleaned)
            
            # Step 4: Remove special characters
            cleaned = cleaned.replace('**', '').replace('*', '').strip()
            
            # Step 5: Remove standalone "Marks" word
            cleaned = re.sub(r'\b[Mm]arks?\b', '', cleaned).strip()
            
            # Step 6: Remove "Total" if standalone
            if cleaned.lower() == 'total':
                continue
            
            # Step 7: Clean extra whitespace
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            
            print(f"         → Cleaned: '{cleaned}'")
            
            # Skip if too short
            if len(cleaned) < 3:
                print(f"         ✗ Too short, skipping")
                continue
            
            # Skip invalid keywords
            skip_keywords = ['total', 'marks', 'awarded', 'marks awarded', 'co', 'po', 'btl', 'grand total']
            if cleaned.lower() in skip_keywords:
                print(f"         ✗ Invalid keyword, skipping")
                continue
            
            # Must start with uppercase letter
            if cleaned and cleaned[0].isupper():
                if cleaned not in sections:
                    sections.append(cleaned)
                    print(f"         ✓ Added: '{cleaned}'")
        
        return sections
    
    
    def _split_combined_sections(self, sections: List[str]) -> List[str]:
        """
        Split "Conclusion and Reference" → "Conclusion" + "References"
        Keep "Solution and Results" as-is
        
        Rule: If contains "reference", split and handle specially
        """
        split_sections = []
        
        for section in sections:
            section_lower = section.lower()
            
            # If contains "reference", split it
            if 'reference' in section_lower:
                print(f"   🔀 Splitting '{section}'")
                
                # Split on "and" or "&"
                parts = re.split(r'\s+and\s+|\s+&\s+', section, flags=re.IGNORECASE)
                
                for part in parts:
                    part = part.strip()
                    
                    # Skip reference part (we'll add it at the end)
                    if 'reference' in part.lower():
                        print(f"      ✗ Excluding: {part}")
                        continue
                    
                    # Keep non-reference part
                    if part and part not in split_sections:
                        split_sections.append(part)
                        print(f"      ✓ Keeping: {part}")
            else:
                # Keep as-is
                if section not in split_sections:
                    split_sections.append(section)
        
        # Always add References at end
        if not any('reference' in s.lower() for s in split_sections):
            split_sections.append('References')
            print(f"   ✓ Added: References")
        
        return split_sections
    
    
    def _get_defaults(self) -> List[str]:
        """Default sections when detection fails"""
        return ["Objective", "Problem Analysis", "Solution", "Conclusion", "References"]
    
    
    # === PUBLIC INTERFACE ===
    
    def analyze_template(self, file_path: str) -> List[str]:
        """Main method - analyze template and return section names"""
        return self.detect_sections_from_marks_table(file_path)
    
    
    def get_section_names(self, file_path: str) -> List[str]:
        """Alias for analyze_template"""
        return self.detect_sections_from_marks_table(file_path)
    
    
    def validate_template(self, file_path: str) -> dict:
        """Validate template and return detailed info"""
        sections = self.analyze_template(file_path)
        
        return {
            "valid": len(sections) >= 3,
            "message": "Valid" if len(sections) >= 3 else "Invalid",
            "sections_count": len(sections),
            "sections": sections
        }
