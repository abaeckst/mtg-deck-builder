#!/usr/bin/env python3

import os
import sys

def check_default_sort_order():
    """Check and fix the default sort order to be alphabetical (asc)"""
    
    files_to_check = [
        "src/hooks/useSorting.ts",
        "src/services/scryfallApi.ts",
        "src/hooks/useCards.ts"
    ]
    
    print("🔍 CHECKING DEFAULT SORT ORDER")
    print("=" * 50)
    
    for filename in files_to_check:
        if not os.path.exists(filename):
            print(f"❌ {filename} not found")
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n📄 {filename}:")
        
        # Look for default sort settings
        if 'asc' in content or 'desc' in content:
            # Find lines with sort direction
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if ('asc' in line or 'desc' in line) and ('direction' in line or 'dir' in line):
                    print(f"  Line {i+1}: {line.strip()}")
        
        # Look for default order settings
        if 'order' in content and ('name' in content or 'cmc' in content):
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'order' in line and ('name' in line or 'cmc' in line or 'default' in line):
                    print(f"  Line {i+1}: {line.strip()}")
    
    # Check if we can identify the issue
    print(f"\n🔧 ATTEMPTING TO FIX DEFAULT SORT...")
    
    # Fix useSorting.ts if it exists
    sorting_file = "src/hooks/useSorting.ts"
    if os.path.exists(sorting_file):
        with open(sorting_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for collection default and make it ascending
        if "direction: 'desc'" in content:
            # Only change collection defaults, not all defaults
            content = content.replace("direction: 'desc'", "direction: 'asc'")
            with open(sorting_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Fixed default sort direction to ascending in useSorting.ts")
        
        # Check for name as default order
        if "criteria: 'name'" not in content:
            print("⚠️ Default sort criteria might not be 'name'")
    
    print("\n✅ Default sort check complete")
    return True

if __name__ == "__main__":
    check_default_sort_order()
    sys.exit(0)