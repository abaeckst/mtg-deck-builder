#!/usr/bin/env python3

import os
import sys

def fix_usecards_clearfilters_mode():
    """Fix the clearAllFilters colorIdentity default in useCards.ts"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for clearAllFilters function and fix colorIdentity
    updates = [
        # Find clearAllFilters and fix the colorIdentity setting
        (
            '      activeFilters: {\n        format: \'\',\n        colors: [],\n        colorIdentity: \'exact\',',
            '      activeFilters: {\n        format: \'\',\n        colors: [],\n        colorIdentity: \'subset\',',
            "Fix clearAllFilters colorIdentity default"
        ),
        
        # Also check clearCards function
        (
            '        colorIdentity: \'exact\',\n        types: [],\n        rarity: [],\n        sets: [],\n        cmc: { min: null, max: null },\n        power: { min: null, max: null },\n        toughness: { min: null, max: null },\n        // Phase 4B: Enhanced filter reset\n        subtypes: [],\n        isGoldMode: false,',
            '        colorIdentity: \'subset\',\n        types: [],\n        rarity: [],\n        sets: [],\n        cmc: { min: null, max: null },\n        power: { min: null, max: null },\n        toughness: { min: null, max: null },\n        // Phase 4B: Enhanced filter reset\n        subtypes: [],\n        isGoldMode: false,',
            "Fix clearCards colorIdentity default"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"ℹ️ Pattern not found: {desc}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_usecards_clearfilters_mode()
    sys.exit(0 if success else 1)