#!/usr/bin/env python3
"""
Fix page calculation in useSearch.ts
The issue is using 75 as page size when Scryfall returns 175 cards per page
"""

import re

def fix_page_calculation():
    """Fix the page calculation in loadMoreCards function"""
    
    print("🔧 Fixing page calculation in useSearch.ts...")
    
    try:
        with open('src/hooks/useSearch.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ useSearch.ts not found")
        return False
    
    # Find and fix the page calculation
    old_calculation = r'''currentPage: Math\.floor\(actualLoadedCards / 75\) \+ 1, // ✅ Calculate from actual cards'''
    
    new_calculation = '''currentPage: Math.floor(actualLoadedCards / 175) + 1, // ✅ Fixed: 175 cards per page, not 75'''
    
    if re.search(old_calculation, content):
        content = re.sub(old_calculation, new_calculation, content)
        print("✅ Fixed page calculation (75 → 175)")
    else:
        # Try alternative pattern
        alt_pattern = r'''currentPage: Math\.floor\(actualLoadedCards / 75\) \+ 1,'''
        alt_replacement = '''currentPage: Math.floor(actualLoadedCards / 175) + 1, // ✅ Fixed: Scryfall returns 175 cards per page'''
        
        if re.search(alt_pattern, content):
            content = re.sub(alt_pattern, alt_replacement, content)
            print("✅ Fixed page calculation using alternative pattern")
        else:
            print("❌ Could not find page calculation pattern")
            return False
    
    # Also fix the other calculation that might be using 75
    other_calc_pattern = r'''currentPage: Math\.floor\(\(state\.cards\.length \+ newCards\.length\) / 75\) \+ 1,'''
    other_calc_replacement = '''currentPage: Math.floor((state.cards.length + newCards.length) / 175) + 1,'''
    
    if re.search(other_calc_pattern, content):
        content = re.sub(other_calc_pattern, other_calc_replacement, content)
        print("✅ Also fixed pagination update calculation")
    
    # Write the fixed content back
    try:
        with open('src/hooks/useSearch.ts', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ useSearch.ts updated successfully")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def main():
    """Main execution"""
    print("🚀 Fixing page calculation")
    print("=" * 30)
    
    if fix_page_calculation():
        print("\n🎯 SUCCESS! Page calculation fixed:")
        print("1. ✅ Changed from 75 cards per page to 175 cards per page")
        print("2. ✅ Load More should now request page 2 instead of page 3")
        print("3. ✅ Should get B cards instead of jumping to C cards")
        print("\nThe issue was:")
        print("- Scryfall returns 175 cards per page")
        print("- Code was calculating based on 75 cards per page")
        print("- Math.floor(175 / 75) + 1 = 3 (wrong)")
        print("- Math.floor(175 / 175) + 1 = 2 (correct)")
        print("\nTest: Search and click Load More - should now get B cards!")
    else:
        print("\n❌ Fix failed - manual action required")
        print("Please manually change '/ 75' to '/ 175' in the page calculations")

if __name__ == "__main__":
    main()
