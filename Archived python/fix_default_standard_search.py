#!/usr/bin/env python3

# Fix the default search to simply show standard cards sorted by mana value
# Remove the creatures-only restriction to show diverse card types

import re

def fix_default_standard_search():
    print("🔧 Fixing default search to show all standard cards sorted by mana value...")
    
    # Read current useSearch.ts file
    try:
        with open('src/hooks/useSearch.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ useSearch.ts not found")
        return False
    
    print("📝 Updating POPULAR_CARDS_QUERY to simple standard search...")
    
    # Replace the creatures-only query with a simple standard search
    old_query_pattern = r"const POPULAR_CARDS_QUERY = '[^']*';"
    new_query = "const POPULAR_CARDS_QUERY = 'legal:standard';"
    
    if re.search(old_query_pattern, content):
        content = re.sub(old_query_pattern, new_query, content)
        print("✅ Updated POPULAR_CARDS_QUERY to 'legal:standard'")
    else:
        print("❌ Could not find POPULAR_CARDS_QUERY pattern")
        return False
    
    # Write updated file
    try:
        with open('src/hooks/useSearch.ts', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Updated useSearch.ts successfully")
    except Exception as e:
        print(f"❌ Failed to write useSearch.ts: {e}")
        return False
    
    print("\n🎯 NEW DEFAULT SEARCH:")
    print("- Query: 'legal:standard'")
    print("- Shows: All standard-legal cards")
    print("- Sorted: By mana value (0, 1, 2, 3, 4, 5...)")
    print("- Mix: Lands, artifacts, creatures, spells, etc.")
    
    print("\n✨ Expected result:")
    print("- App loads showing 0-cost artifacts and lands first")
    print("- Then 1-cost cards (creatures, instants, etc.)")
    print("- Then 2-cost cards, 3-cost cards, etc.")
    print("- Clear mana value progression instead of creature-only")
    
    print("\n🧪 Test: Refresh the app and you should see:")
    print("- More diverse card types in initial results")
    print("- Clear mana cost progression from 0 upward")
    print("- Console logs still showing 'order=cmc&dir=asc'")
    
    return True

if __name__ == "__main__":
    success = fix_default_standard_search()
    if success:
        print("\n🚀 Default search fix complete! Refresh the app to test.")
    else:
        print("\n❌ Default search fix failed. Check error messages above.")
