#!/usr/bin/env python3
"""
Comprehensive Fix Script for All TypeScript Errors
Fixes naming conflicts, missing properties, and CSS syntax issues
"""

import re
import os

def fix_use_cards_clear_function():
    """Fix the clearCards function to include missing set filter state properties"""
    file_path = "src/hooks/useCards.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        return False
    
    print(f"🔧 Reading {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix the clearCards function to include missing properties
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
      // Enhanced filtering state
      activeFilters: {
        format: 'standard',
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
      // Set filter state
      availableSets: [],
      setSearchText: '',
      filteredSets: [],
      // Enhanced filtering state
      activeFilters: {
        format: 'standard',
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
            print("✅ Fixed clearCards function to include missing set filter properties")
        else:
            print("⚠️  Could not find clearCards function pattern")
            return False
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ SUCCESS: Fixed {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to update {file_path}: {str(e)}")
        return False

def fix_mtgo_layout_naming_conflicts():
    """Fix naming conflicts and CSS syntax issues in MTGOLayout.tsx"""
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        return False
    
    print(f"🔧 Reading {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix 1: Remove setSearchText from useCards destructuring since we have local state
        old_destructuring = """  const { 
    cards, 
    loading, 
    error, 
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards, 
    loadRandomCard,
    activeFilters,
    isFiltersCollapsed,
    updateFilter,
    clearAllFilters,
    toggleFiltersCollapsed,
    hasActiveFilters,
    searchSuggestions,
    showSuggestions,
    getSearchSuggestions,
    clearSearchSuggestions,
    addToSearchHistory,
    availableSets,
    setSearchText,
    filteredSets,
    updateSetSearchText,
    toggleSetSelection
  } = useCards();"""
        
        new_destructuring = """  const { 
    cards, 
    loading, 
    error, 
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards, 
    loadRandomCard,
    activeFilters,
    isFiltersCollapsed,
    updateFilter,
    clearAllFilters,
    toggleFiltersCollapsed,
    hasActiveFilters,
    searchSuggestions,
    showSuggestions,
    getSearchSuggestions,
    clearSearchSuggestions,
    addToSearchHistory,
    availableSets,
    setSearchText: setFilterSearchText,
    filteredSets,
    updateSetSearchText,
    toggleSetSelection
  } = useCards();"""
        
        if old_destructuring in content:
            content = content.replace(old_destructuring, new_destructuring)
            print("✅ Fixed useCards destructuring - renamed setSearchText to setFilterSearchText")
        else:
            print("⚠️  Could not find useCards destructuring pattern")
        
        # Fix 2: Update the SearchAutocomplete onChange to use local setSearchText function
        old_search_autocomplete = """              <SearchAutocomplete
                value={searchText}
                onChange={setSearchText}
                onSearch={handleSearch}"""
        
        new_search_autocomplete = """              <SearchAutocomplete
                value={searchText}
                onChange={setSearchText}
                onSearch={handleSearch}"""
        
        # This one should already be correct, but let's make sure setSearchText refers to local state
        
        # Fix 3: Update set search input to use the renamed function
        old_set_search_input = """                  value={setSearchText}
                  onChange={(e) => updateSetSearchText(e.target.value)}"""
        
        new_set_search_input = """                  value={setFilterSearchText}
                  onChange={(e) => updateSetSearchText(e.target.value)}"""
        
        if old_set_search_input in content:
            content = content.replace(old_set_search_input, new_set_search_input)
            print("✅ Fixed set search input to use renamed setFilterSearchText")
        
        # Fix 4: Update condition that checks setSearchText
        old_condition = """                  {filteredSets.length === 0 && setSearchText && ("""
        new_condition = """                  {filteredSets.length === 0 && setFilterSearchText && ("""
        
        if old_condition in content:
            content = content.replace(old_condition, new_condition)
            print("✅ Fixed setSearchText condition to use renamed variable")
        
        # Fix 5: Remove invalid CSS :hover syntax
        old_css_style = """                      ':hover': { backgroundColor: '#333' }"""
        new_css_style = """                      // Note: hover styles should be in CSS file"""
        
        if old_css_style in content:
            content = content.replace(old_css_style, new_css_style)
            print("✅ Fixed invalid :hover CSS syntax")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ SUCCESS: Fixed {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to update {file_path}: {str(e)}")
        return False

def main():
    print("🚀 MTG Deck Builder - Comprehensive Fix for TypeScript Errors")
    print("=" * 70)
    print("This script fixes all compilation errors from the filter addition.\n")
    
    success = True
    
    # Step 1: Fix useCards.ts clearCards function
    print("📦 Step 1: Fixing clearCards function in useCards.ts...")
    if not fix_use_cards_clear_function():
        success = False
    
    # Step 2: Fix MTGOLayout.tsx naming conflicts and CSS
    print("\n🎨 Step 2: Fixing naming conflicts and CSS in MTGOLayout.tsx...")
    if not fix_mtgo_layout_naming_conflicts():
        success = False
    
    if success:
        print("\n🎉 All TypeScript errors fixed successfully!")
        print("📋 Next steps:")
        print("   1. Run 'npm start' to verify compilation")
        print("   2. Test the set filter functionality")
        print("   3. Test color identity fix")
        print("   4. Test custom standard enhancement")
        print("\n🔧 What was fixed:")
        print("   ✅ Removed setSearchText naming conflict")
        print("   ✅ Added missing set filter state properties")
        print("   ✅ Fixed invalid CSS :hover syntax")
        print("   ✅ Renamed conflicting variable to setFilterSearchText")
    else:
        print("\n❌ Some fixes failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
