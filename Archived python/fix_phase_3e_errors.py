#!/usr/bin/env python3
"""
Fix Phase 3E implementation errors
Fixes specific compilation and TypeScript errors
"""

import os

def fix_mtgo_layout_placeholder():
    """Fix the placeholder string escaping issue in MTGOLayout.tsx"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the placeholder string with proper escaping
        find_text = '''                placeholder="Search cards... (try: flying, \"exact phrase\", -exclude, name:lightning)"'''
        replace_text = '''                placeholder="Search cards... (try: flying, &quot;exact phrase&quot;, -exclude, name:lightning)"'''
        
        if find_text in content:
            content = content.replace(find_text, replace_text)
            print("✅ Fixed placeholder string escaping in MTGOLayout.tsx")
        else:
            print("❌ Could not find placeholder string to fix")
            return False
        
        # Fix the dependency issue - remove searchWithAllFilters from handleFilterChange
        find_dependency = """  }, [updateFilter, searchWithAllFilters, searchText, activeFilters]);"""
        replace_dependency = """  }, [updateFilter, enhancedSearch, searchText, activeFilters]);"""
        
        if find_dependency in content:
            content = content.replace(find_dependency, replace_dependency)
            print("✅ Fixed handleFilterChange dependency array")
        else:
            print("❌ Could not find dependency array to fix")
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
        
    except Exception as e:
        print(f"❌ Error fixing MTGOLayout.tsx: {e}")
        return False

def fix_use_cards_clear_cards():
    """Fix the clearCards function in useCards.ts to include missing properties"""
    file_path = "src/hooks/useCards.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the clearCards function to include all required properties
        find_clear_cards = """  // Clear all cards and reset state
  const clearCards = useCallback(() => {
    setState({
      cards: [],
      loading: false,
      error: null,
      hasMore: false,
      selectedCards: new Set(),
      searchQuery: '',
      totalCards: 0,
      // Enhanced filtering state
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
      isFiltersCollapsed: false,
    });
  }, []);"""
        
        replace_clear_cards = """  // Clear all cards and reset state
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
      isFiltersCollapsed: false,
    });
  }, []);"""
        
        if find_clear_cards in content:
            content = content.replace(find_clear_cards, replace_clear_cards)
            print("✅ Fixed clearCards function to include search state properties")
        else:
            print("❌ Could not find clearCards function to fix")
            return False
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
        
    except Exception as e:
        print(f"❌ Error fixing useCards.ts: {e}")
        return False

def fix_scryfall_api_set_iteration():
    """Fix the Set iteration issue in scryfallApi.ts"""
    file_path = "src/services/scryfallApi.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the Set spread operator issue
        find_set_spread = """    // Remove duplicates and limit results
    return [...new Set(suggestions)].slice(0, 10);"""
        
        replace_set_spread = """    // Remove duplicates and limit results
    const uniqueSuggestions = Array.from(new Set(suggestions));
    return uniqueSuggestions.slice(0, 10);"""
        
        if find_set_spread in content:
            content = content.replace(find_set_spread, replace_set_spread)
            print("✅ Fixed Set iteration compatibility in scryfallApi.ts")
        else:
            print("❌ Could not find Set spread operator to fix")
            return False
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
        
    except Exception as e:
        print(f"❌ Error fixing scryfallApi.ts: {e}")
        return False

def main():
    """Run all error fixes"""
    print("🔧 Fixing Phase 3E compilation errors")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src/services/scryfallApi.ts"):
        print("❌ Error: Please run this script from your project root directory")
        print("   Expected location: C:\\Users\\carol\\mtg-deckbuilder")
        return False
    
    success_count = 0
    total_fixes = 3
    
    # Fix MTGOLayout placeholder issue
    print("🔧 Fixing MTGOLayout placeholder string...")
    if fix_mtgo_layout_placeholder():
        success_count += 1
    
    # Fix useCards clearCards function
    print("🔧 Fixing useCards clearCards function...")
    if fix_use_cards_clear_cards():
        success_count += 1
    
    # Fix scryfallApi Set iteration
    print("🔧 Fixing scryfallApi Set iteration...")
    if fix_scryfall_api_set_iteration():
        success_count += 1
    
    print("=" * 50)
    print(f"✅ Error fixes complete: {success_count}/{total_fixes} fixes successful")
    
    if success_count == total_fixes:
        print("🎉 All errors should now be resolved!")
        print("\\n🔧 Next Steps:")
        print("1. Run 'npm start' to verify compilation")
        print("2. Test the enhanced search functionality")
        print("3. Verify all existing features still work")
        print("\\n📋 Expected working features:")
        print("• Enhanced search with autocomplete suggestions")
        print("• Search operators: quotes, exclusion (-), field-specific")
        print("• Full-text search across names, text, and types")
        print("• Seamless integration with existing filters")
    else:
        print(f"❌ Some fixes failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    main()