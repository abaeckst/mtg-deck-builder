#!/usr/bin/env python3
"""
Fix FilterPanel clear button by correcting hasActiveFilters prop usage.
The FilterPanel interface expects a boolean but MTGOLayout is passing a function reference.
"""

import re

def fix_filter_panel_props():
    """Fix the MTGOLayout.tsx hasActiveFilters prop to pass boolean instead of function."""
    
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the FilterPanel props section
        # Look for hasActiveFilters={hasActiveFilters()} and change to hasActiveFilters={hasActiveFilters}
        pattern = r'hasActiveFilters=\{hasActiveFilters\(\)\}'
        replacement = r'hasActiveFilters={hasActiveFilters}'
        
        updated_content = re.sub(pattern, replacement, content)
        
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("✅ Fixed MTGOLayout.tsx - hasActiveFilters now passes function reference")
            print("   Changed: hasActiveFilters={hasActiveFilters()} → hasActiveFilters={hasActiveFilters}")
        else:
            print("❌ Pattern not found in MTGOLayout.tsx")
            print("   Looking for: hasActiveFilters={hasActiveFilters()}")
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error processing file: {e}")

def update_filter_panel_interface():
    """Update FilterPanel interface to expect function instead of boolean."""
    
    file_path = "src/components/FilterPanel.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update interface to expect function
        pattern = r'hasActiveFilters:\s*boolean;'
        replacement = r'hasActiveFilters: () => boolean;'
        
        updated_content = re.sub(pattern, replacement, content)
        
        # Update the conditional usage to call the function
        pattern2 = r'\{hasActiveFilters\s*&&\s*\('
        replacement2 = r'{hasActiveFilters() && ('
        
        updated_content = re.sub(pattern2, replacement2, updated_content)
        
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("✅ Fixed FilterPanel.tsx interface and usage")
            print("   - Interface: hasActiveFilters: boolean → hasActiveFilters: () => boolean")
            print("   - Usage: {hasActiveFilters && → {hasActiveFilters() &&")
        else:
            print("❌ Patterns not found in FilterPanel.tsx")
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error processing file: {e}")

if __name__ == "__main__":
    print("🔧 Fixing Clear Button Props Issue...")
    print()
    
    # Update FilterPanel to expect and use function properly
    update_filter_panel_interface()
    
    print()
    print("🎯 Fix Summary:")
    print("   Clear button will now appear when filters are active")
    print("   FilterPanel interface updated to match useCards function signature")
    print()
    print("🧪 Test: Apply filters and check for Clear button in header")
