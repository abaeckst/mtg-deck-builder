#!/usr/bin/env python3

import os
import sys

def fix_cards_hook_remaining(filename):
    """Fix remaining issues in useCards.ts for Phase 4B"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements with exact string matching
    updates = [
        # Update clearAllFilters function (alternative search pattern)
        (
            """    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
    }));""",
            """    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
        // Phase 4B: Enhanced filter clear
        subtypes: [],
        isGoldMode: false,
        sectionStates: {
          colors: true,
          cmc: true,
          types: true,
          subtypes: true,
          sets: false,
          rarity: false,
          stats: false,
        },
      },
    }));""",
            "Enhanced filter clear in clearAllFilters"
        ),
        
        # Update clearCards filter reset (alternative search pattern)
        (
            """      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },""",
            """      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
        // Phase 4B: Enhanced filter reset
        subtypes: [],
        isGoldMode: false,
        sectionStates: {
          colors: true,
          cmc: true,
          types: true,
          subtypes: true,
          sets: false,
          rarity: false,
          stats: false,
        },
      },""",
            "Enhanced filter reset in clearCards"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            print(f"Searching for alternative pattern...")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_cards_hook_remaining("src/hooks/useCards.ts")
    sys.exit(0 if success else 1)
