#!/usr/bin/env python3
# Add Default Standard Format Filter
# Sets the default format filter to Standard when the app loads

import os
import re

def update_use_cards_default_format():
    """Update useCards.ts to default to Standard format"""
    print("🔧 Setting default format to Standard in useCards.ts...")
    
    file_path = "src/hooks/useCards.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: {file_path} not found!")
        return False
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the activeFilters initialization
    old_code = '''    // Enhanced filtering state
    activeFilters: {
      format: '',
      colors: [],'''
    
    new_code = '''    // Enhanced filtering state
    activeFilters: {
      format: 'standard',
      colors: [],'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        # Write the file back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Default format set to 'standard' in useCards.ts")
        return True
    else:
        print("❌ Could not find the exact activeFilters initialization code")
        print("Please check the activeFilters object in useCards.ts manually")
        return False

def update_clear_filters_default():
    """Update clearAllFilters to reset to Standard instead of empty"""
    print("🔧 Updating clearAllFilters to reset to Standard...")
    
    file_path = "src/hooks/useCards.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: {file_path} not found!")
        return False
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the clearAllFilters function
    old_code = '''      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },'''
    
    new_code = '''      activeFilters: {
        format: 'standard',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        # Write the file back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ clearAllFilters now resets to Standard format")
        return True
    else:
        print("❌ Could not find the exact clearAllFilters reset code")
        print("Please check the clearAllFilters function manually")
        return False

def update_popular_cards_query():
    """Update the popular cards query to include Standard format"""
    print("🔧 Updating popular cards to be Standard-legal...")
    
    file_path = "src/hooks/useCards.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: {file_path} not found!")
        return False
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the POPULAR_CARDS_QUERY
    old_code = '''const POPULAR_CARDS_QUERY = 'is:commander OR name:"Lightning Bolt" OR name:"Counterspell" OR name:"Sol Ring" OR name:"Path to Exile" OR name:"Swords to Plowshares" OR name:"Birds of Paradise" OR name:"Dark Ritual" OR name:"Giant Growth" OR name:"Ancestral Recall"';'''
    
    new_code = '''const POPULAR_CARDS_QUERY = 'legal:standard (type:creature OR type:instant OR type:sorcery OR type:planeswalker OR type:enchantment OR type:artifact)';'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        # Write the file back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Popular cards now shows Standard-legal cards")
        return True
    else:
        print("❌ Could not find the POPULAR_CARDS_QUERY constant")
        print("Please check the popular cards query manually")
        return False

def main():
    """Main execution function"""
    print("🚀 Setting Default Standard Format Filter")
    print("=" * 50)
    
    # Check we're in the right directory
    if not os.path.exists("src/hooks/useCards.ts"):
        print("❌ ERROR: Not in the correct directory!")
        print("Please run this script from: c:/Users/carol/mtg-deckbuilder")
        return
    
    print("📁 Working directory confirmed: MTG Deck Builder project")
    print()
    
    # Apply all updates
    fix1_success = update_use_cards_default_format()
    print()
    fix2_success = update_clear_filters_default()
    print()
    fix3_success = update_popular_cards_query()
    print()
    
    # Summary
    print("=" * 50)
    if fix1_success and fix2_success and fix3_success:
        print("🎉 SUCCESS: Default Standard format filter is now active!")
        print()
        print("✅ Changes applied:")
        print("   1. App now loads with Standard format selected by default")
        print("   2. Clear filters button resets to Standard (not empty)")
        print("   3. Popular cards now shows Standard-legal cards")
        print()
        print("🧪 TEST:")
        print("   1. Reload the app → Standard should be pre-selected")
        print("   2. Search should only show Standard-legal cards")
        print("   3. Click 'Clear' filters → should reset to Standard")
        print()
        print("🚀 Ready to test the Standard-focused experience!")
    else:
        print("⚠️  PARTIAL SUCCESS: Some changes may need manual attention")
        print("Please check the useCards.ts file for any needed manual updates")

if __name__ == "__main__":
    main()
