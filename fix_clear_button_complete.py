#!/usr/bin/env python3
"""
Complete fix for clear button - align MTGOLayout and FilterPanel properly.
Fix the compilation error by making MTGOLayout pass function reference.
"""

import re

def fix_mtgo_layout_props():
    """Fix MTGOLayout to pass function reference instead of boolean result."""
    
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the hasActiveFilters prop to pass function reference
        pattern = r'hasActiveFilters=\{hasActiveFilters\(\)\}'
        replacement = r'hasActiveFilters={hasActiveFilters}'
        
        updated_content = re.sub(pattern, replacement, content)
        
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("✅ Fixed MTGOLayout.tsx compilation error")
            print("   Changed: hasActiveFilters={hasActiveFilters()} → hasActiveFilters={hasActiveFilters}")
            print("   Now passes function reference to match FilterPanel interface")
        else:
            print("❌ Pattern not found in MTGOLayout.tsx")
            print("   Looking for: hasActiveFilters={hasActiveFilters()}")
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error processing file: {e}")

if __name__ == "__main__":
    print("🔧 Fixing Clear Button Compilation Error...")
    print()
    
    # Fix MTGOLayout to pass function reference
    fix_mtgo_layout_props()
    
    print()
    print("🎯 Fix Summary:")
    print("   - MTGOLayout now passes function reference instead of boolean result")
    print("   - Matches FilterPanel interface expecting () => boolean")
    print("   - Clear button should now appear when filters are active")
    print()
    print("🧪 Test: Compile with npm start, then apply filters to see Clear button")
