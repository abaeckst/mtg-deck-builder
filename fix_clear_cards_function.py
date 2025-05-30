#!/usr/bin/env python3
"""
Fix clearCards Function TypeScript Error
Removes remaining set filter state properties from clearCards function
"""

import re
import os

def fix_clear_cards_function():
    file_path = "src/hooks/useCards.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        return False
    
    print(f"🔧 Fixing clearCards function in useCards.ts...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find and fix the clearCards function - remove set filter properties
        old_clear_cards = """  // Clear all cards and reset state
  const clearCards = useCallback(() => {
    setState({
      cards: [],
      loading: false,
      error: null,
      hasMore: false,
      selectedCards: new Set(),
      searchQuery: '',
      totalCards: 0,
      // Enhanced search state
      searchSuggestions: [],
      showSuggestions: false,
      recentSearches: [],
      // Set filter state
      availableSets: [],
      setSearchText: '',
      filteredSets: [],
      // Enhanced filtering state
      activeFilters: {
        format: 'custom-standard',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
      isFiltersCollapsed: false,
    });
  }, []);"""
        
        new_clear_cards = """  // Clear all cards and reset state
  const clearCards = useCallback(() => {
    setState({
      cards: [],
      loading: false,
      error: null,
      hasMore: false,
      selectedCards: new Set(),
      searchQuery: '',
      totalCards: 0,
      // Enhanced search state
      searchSuggestions: [],
      showSuggestions: false,
      recentSearches: [],
      // Enhanced filtering state
      activeFilters: {
        format: 'custom-standard',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
      isFiltersCollapsed: false,
    });
  }, []);"""
        
        if old_clear_cards in content:
            content = content.replace(old_clear_cards, new_clear_cards)
            print("✅ Fixed clearCards function - removed set filter state properties")
        else:
            print("⚠️  Could not find exact clearCards pattern, trying alternative approach...")
            
            # Alternative approach - just remove the problematic lines
            content = content.replace("      // Set filter state\n", "")
            content = content.replace("      availableSets: [],\n", "")
            content = content.replace("      setSearchText: '',\n", "")
            content = content.replace("      filteredSets: [],\n", "")
            
            print("✅ Applied alternative fix - removed individual set filter lines")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ SUCCESS: Fixed clearCards function in {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to update {file_path}: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 MTG Deck Builder - Fix clearCards Function")
    print("=" * 50)
    print("This script fixes the TypeScript error in clearCards function.\n")
    
    success = fix_clear_cards_function()
    
    if success:
        print("\n🎉 clearCards function fixed successfully!")
        print("📋 Next steps:")
        print("   1. Run 'npm start' to verify compilation")
        print("   2. Test the application functionality")
    else:
        print("\n❌ Fix failed. Please check the error messages above.")
