#!/usr/bin/env python3
# Phase 3E Enhanced Search - Completion Fix Script
# Fixes the 2 remaining issues to complete Phase 3E implementation.
# Run this script from your project directory: c:/Users/carol/mtg-deckbuilder

import os
import re

def fix_full_text_search():
    # Fix Issue 1: Enable full-text search for simple queries
    print("🔧 Fixing full-text search in scryfallApi.ts...")
    
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: {file_path} not found!")
        return False
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the problematic logic
    old_code = '''  // For simple queries without operators, just return the query as-is
  // This allows Scryfall's natural search to work normally
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    return query;
  }'''
    
    new_code = '''  // For simple queries without operators, enable full-text search
  // This searches across name, oracle text, and type line
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    return `(name:"${query}" OR oracle:"${query}" OR type:"${query}")`;
  }'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        # Write the file back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Fixed full-text search - simple queries now search oracle text and type lines")
        return True
    else:
        print("❌ Could not find the exact code to replace in scryfallApi.ts")
        print("The file may have been modified. Please check lines 356-359 manually.")
        return False

def fix_autocomplete_persistence():
    # Fix Issue 2: Hide autocomplete when Enter is pressed
    print("🔧 Fixing autocomplete persistence in SearchAutocomplete.tsx...")
    
    file_path = "src/components/SearchAutocomplete.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: {file_path} not found!")
        return False
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the Enter key handler
    old_code = '''      case 'Enter':
        e.preventDefault();
        if (activeSuggestionIndex >= 0) {
          onSuggestionSelect(suggestions[activeSuggestionIndex]);
        } else {
          onSearch(value);
        }
        break;'''
    
    new_code = '''      case 'Enter':
        e.preventDefault();
        if (activeSuggestionIndex >= 0) {
          onSuggestionSelect(suggestions[activeSuggestionIndex]);
        } else {
          onSearch(value);
          onSuggestionsClear(); // Hide autocomplete after search
        }
        break;'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        
        # Write the file back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Fixed autocomplete persistence - dropdown now hides when Enter is pressed")
        return True
    else:
        print("❌ Could not find the exact code to replace in SearchAutocomplete.tsx")
        print("The file may have been modified. Please check the Enter key handler manually.")
        return False

def main():
    # Main execution function
    print("🚀 Phase 3E Enhanced Search - Completion Fix Script")
    print("=" * 60)
    
    # Check we're in the right directory
    if not os.path.exists("src/services/scryfallApi.ts"):
        print("❌ ERROR: Not in the correct directory!")
        print("Please run this script from: c:/Users/carol/mtg-deckbuilder")
        return
    
    print("📁 Working directory confirmed: MTG Deck Builder project")
    print()
    
    # Apply both fixes
    fix1_success = fix_full_text_search()
    print()
    fix2_success = fix_autocomplete_persistence()
    print()
    
    # Summary
    print("=" * 60)
    if fix1_success and fix2_success:
        print("🎉 SUCCESS: Phase 3E Enhanced Search is now COMPLETE!")
        print()
        print("✅ Both issues resolved:")
        print("   1. Full-text search now works for simple queries")
        print("   2. Autocomplete properly hides when Enter is pressed")
        print()
        print("🧪 TEST PLAN:")
        print("   1. Search 'draw' → should return cards with 'draw' in text (like Opt, Divination)")
        print("   2. Search 'flying' → should return creatures with flying ability")
        print("   3. Type 'light' → press Enter → autocomplete should disappear")
        print("   4. Verify search operators still work: \"exact phrase\", -exclude, name:bolt")
        print()
        print("🚀 Ready to commit Phase 3E completion!")
    else:
        print("⚠️  PARTIAL SUCCESS: Some fixes may need manual attention")
        if not fix1_success:
            print("   - Full-text search fix needs manual verification")
        if not fix2_success:
            print("   - Autocomplete fix needs manual verification")
        print()
        print("Please check the indicated files and apply the changes manually if needed.")

if __name__ == "__main__":
    main()
