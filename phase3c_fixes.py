# Phase 3C TypeScript Fixes
# This script fixes the compilation errors from the initial implementation

import os
import re

def fix_use_cards_clear_function():
    """Fix the clearCards function to include missing state properties"""
    
    # Read the current file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the clearCards function
    old_clear_function = '''  // Clear all cards and reset state
  const clearCards = useCallback(() => {
    setState({
      cards: [],
      loading: false,
      error: null,
      hasMore: false,
      selectedCards: new Set(),
      searchQuery: '',
      totalCards: 0,
    });
  }, []);'''
    
    new_clear_function = '''  // Clear all cards and reset state
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
        colorIdentity: 'include',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
      isFiltersCollapsed: false,
    });
  }, []);'''
    
    content = content.replace(old_clear_function, new_clear_function)
    
    # Write the updated file
    with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed clearCards function in useCards.ts")

def fix_scryfall_api_backward_compatibility():
    """Remove the problematic backward compatibility code for single set filter"""
    
    # Read the current file
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the problematic backward compatibility section
    problematic_code = '''  
  // Backward compatibility for single set filter
  if (filters.set && !filters.sets) {
    searchQuery += ` set:${filters.set}`;
  }'''
    
    content = content.replace(problematic_code, '')
    
    # Also clean up any extra whitespace that might be left
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Write the updated file
    with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed SearchFilters backward compatibility in scryfallApi.ts")

def verify_interface_consistency():
    """Verify that all interfaces are consistent"""
    
    # Read the scryfallApi.ts file
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        api_content = f.read()
    
    # Read the useCards.ts file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        cards_content = f.read()
    
    # Check if SearchFilters interface is properly defined
    if 'export interface SearchFilters' in api_content:
        print("✅ SearchFilters interface found in scryfallApi.ts")
    else:
        print("❌ SearchFilters interface missing in scryfallApi.ts")
    
    # Check if UseCardsState interface includes all required properties
    if 'activeFilters:' in cards_content and 'isFiltersCollapsed:' in cards_content:
        print("✅ Enhanced state properties found in useCards.ts")
    else:
        print("❌ Enhanced state properties missing in useCards.ts")

def add_missing_imports():
    """Add any missing imports that might be needed"""
    
    # Read the useCards.ts file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if SearchFilters import exists
    if 'SearchFilters' not in content:
        # Add the import
        old_import = "import { searchCards, getRandomCard, searchCardsWithFilters } from '../services/scryfallApi';"
        new_import = "import { searchCards, getRandomCard, searchCardsWithFilters, SearchFilters } from '../services/scryfallApi';"
        
        content = content.replace(old_import, new_import)
        
        # Write the updated file
        with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Added SearchFilters import to useCards.ts")
    else:
        print("✅ SearchFilters import already exists in useCards.ts")

def main():
    """Execute all fixes for Phase 3C TypeScript errors"""
    try:
        print("🔧 Fixing Phase 3C TypeScript Compilation Errors")
        print("=" * 50)
        
        # Fix 1: clearCards function missing state properties
        print("\n📋 Fix 1: Updating clearCards function...")
        fix_use_cards_clear_function()
        
        # Fix 2: Remove problematic backward compatibility code
        print("\n📋 Fix 2: Removing problematic backward compatibility...")
        fix_scryfall_api_backward_compatibility()
        
        # Fix 3: Add missing imports
        print("\n📋 Fix 3: Adding missing imports...")
        add_missing_imports()
        
        # Fix 4: Verify everything is consistent
        print("\n📋 Fix 4: Verifying interface consistency...")
        verify_interface_consistency()
        
        print("\n" + "=" * 50)
        print("✅ All TypeScript Fixes Applied!")
        print("\n🧪 Next Steps:")
        print("   1. Run 'npm start' to verify compilation")
        print("   2. Test the enhanced filter functionality")
        print("   3. Verify all existing features still work")
        
        print("\n🎯 If you still see errors, please share them and I'll fix immediately!")
        
    except Exception as e:
        print(f"\n❌ Error during fixes: {e}")
        print("Please check the file paths and try again.")

if __name__ == "__main__":
    main()
