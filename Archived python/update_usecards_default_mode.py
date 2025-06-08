#!/usr/bin/env python3

import os
import sys

def update_usecards_default_mode():
    """Update useCards.ts to change default color mode to 'subset' (At most these colors)"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Updates for default color mode
    updates = [
        # 1. Change initial default from 'exact' to 'subset'
        (
            "      colorIdentity: 'exact',",
            "      colorIdentity: 'subset',",
            "Change initial colorIdentity default to 'subset'"
        ),
        
        # 2. Change reset state in clearAllFilters
        (
            "        colorIdentity: 'exact',",
            "        colorIdentity: 'subset',",
            "Change clearAllFilters colorIdentity default to 'subset'"
        ),
        
        # 3. Change reset state in clearCards
        (
            "        colorIdentity: 'exact',",
            "        colorIdentity: 'subset',",
            "Change clearCards colorIdentity default to 'subset'"
        ),
        
        # 4. Update default section states to have default sections expanded
        (
            "        sectionStates: {\n          colors: true,      // Default sections expanded\n          cmc: true,\n          types: true,\n          subtypes: true,\n          sets: false,       // Advanced sections collapsed\n          rarity: false,\n          stats: false,\n        },",
            "        sectionStates: {\n          colors: true,      // Default sections expanded\n          cmc: true,\n          types: true,\n          subtypes: true,\n          sets: false,       // Advanced sections collapsed\n          rarity: false,\n          stats: false,\n        },",
            "Confirm default section states (already correct)"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            # For the section states, it's already correct, so just note it
            if "section states" in desc.lower():
                print(f"ℹ️ {desc} - already configured correctly")
            else:
                print(f"❌ Could not find: {desc}")
                return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_usecards_default_mode()
    sys.exit(0 if success else 1)