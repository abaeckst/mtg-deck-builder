#!/usr/bin/env python3

import os
import sys

def fix_sortcriteria_conflict(filename):
    """Fix SortCriteria type conflict in MTGOLayout.tsx"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements to fix the type conflict
    updates = [
        # 1. Remove the local SortCriteria type definition
        (
            """// Pile view sort state
type SortCriteria = 'name' | 'mana' | 'color' | 'rarity' | 'type';""",
            """// Pile view sort state - using SortCriteria from useSorting hook""",
            "Remove local SortCriteria type definition"
        ),
        
        # 2. Also check if there are any other local type definitions that might conflict
        (
            """type SortCriteria = 'name' | 'mana' | 'color' | 'rarity' | 'type';""",
            """// SortCriteria imported from useSorting hook""",
            "Remove any remaining local SortCriteria definition"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"⚠️  Could not find (may already be fixed): {desc}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed SortCriteria conflict in {filename}")
    return True

if __name__ == "__main__":
    success = fix_sortcriteria_conflict("src/components/MTGOLayout.tsx")
    sys.exit(0 if success else 1)