#!/usr/bin/env python3
"""
Scryfall Multi-Word Search Fix Script
Fixes the buildEnhancedSearchQuery function to use proper Scryfall oracle text syntax
"""

import os
import re

def fix_scryfall_api():
    # Path to the file
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Read the current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # REVISED: Fix the actual multi-word logic that's in the file
    old_multiword_logic = """    if (words.length > 1) {
      // Multi-word query: Use Scryfall-compatible syntax
      console.log('🔍 Multi-word query detected, using simple syntax:', query);
      return query;"""

    new_multiword_logic = """    if (words.length > 1) {
      // Multi-word query: Use oracle text search with proper Scryfall syntax
      console.log('🔍 Multi-word query detected, using oracle text syntax:', query);
      return `oracle:"${query}";"""

    # Replace the multi-word logic
    if old_multiword_logic in content:
        content = content.replace(old_multiword_logic, new_multiword_logic)
        print("✅ Fixed multi-word search logic")
    else:
        # Try alternative pattern matching
        alternative_pattern = r'if \(words\.length > 1\) \{\s*// Multi-word query.*?\n.*?return query;'
        match = re.search(alternative_pattern, content, re.DOTALL)
        if match:
            old_text = match.group(0)
            new_text = """if (words.length > 1) {
      // Multi-word query: Use oracle text search with proper Scryfall syntax
      console.log('🔍 Multi-word query detected, using oracle text syntax:', query);
      return `oracle:"${query}";"""
            content = content.replace(old_text, new_text)
            print("✅ Fixed multi-word search logic (alternative pattern)")
        else:
            print("❌ Could not find multi-word logic to replace")
            print("🔧 Manual fix needed:")
            print("   Change: return query; → return `oracle:\"${query}\";")
            return False
    
    # Also add User-Agent header to rateLimitedFetch function
    old_fetch = """  const response = await fetch(url, {
    headers: {
      'Accept': 'application/json',
    },
  });"""

    new_fetch = """  const response = await fetch(url, {
    headers: {
      'Accept': 'application/json',
      'User-Agent': 'MTGDeckBuilder/1.0',
    },
  });"""
    
    if old_fetch in content:
        content = content.replace(old_fetch, new_fetch)
        print("✅ Added User-Agent header to rateLimitedFetch")
    else:
        print("⚠️  Headers already present or pattern not found")
    
    # Write the updated content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {file_path}")
    return True

def main():
    print("🔧 Fixing Scryfall multi-word search...")
    print("📍 Current directory:", os.getcwd())
    
    if fix_scryfall_api():
        print("\n🎉 Multi-word search fix complete!")
        print("\nTest these searches after running npm start:")
        print("✅ 'deal damage' should now work")
        print("✅ 'enters battlefield' should now work") 
        print("✅ 'target creature' should now work")
        print("✅ Single words like 'lightning' should still work")
    else:
        print("\n❌ Fix failed - manual intervention required")
        print("\nManual fix needed:")
        print("1. Open src/services/scryfallApi.ts")
        print("2. Find buildEnhancedSearchQuery function")
        print("3. Change multi-word query logic to use: enhancedQuery = `o:\"${originalQuery}\"`")
        print("4. Add User-Agent header to API calls")

if __name__ == "__main__":
    main()
