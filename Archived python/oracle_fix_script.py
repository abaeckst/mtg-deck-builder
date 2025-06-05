#!/usr/bin/env python3
"""
Fix Oracle Text Search Syntax in scryfallApi.ts
Changes 'oracle:' to 'o:' for proper Scryfall API compatibility
"""

import os

def fix_oracle_syntax():
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Read the current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Fixing oracle syntax...")
    
    # Track changes made
    changes_made = 0
    
    # Fix 1: Multi-word query template literal (line ~366)
    old_multiword = 'return `oracle:"${query}"`;'
    new_multiword = 'return `o:"${query}"`;'
    
    if old_multiword in content:
        content = content.replace(old_multiword, new_multiword)
        print("✅ Fixed multi-word oracle syntax: oracle: → o:")
        changes_made += 1
    else:
        print("⚠️  Multi-word oracle syntax not found (may already be fixed)")
    
    # Fix 2: Single-word query template literal (line ~369)
    old_singleword = '`(name:${query} OR oracle:${query} OR type:${query})`'
    new_singleword = '`(name:${query} OR o:${query} OR type:${query})`'
    
    if old_singleword in content:
        content = content.replace(old_singleword, new_singleword)
        print("✅ Fixed single-word oracle syntax: oracle: → o:")
        changes_made += 1
    else:
        print("⚠️  Single-word oracle syntax not found (may already be fixed)")
    
    # Fix 3: Any other instances of 'oracle:' in template literals
    # Look for other oracle: references in the buildEnhancedSearchQuery function
    old_parts_oracle = 'parts.push(`oracle:${processedValue}`);'
    new_parts_oracle = 'parts.push(`o:${processedValue}`);'
    
    if old_parts_oracle in content:
        content = content.replace(old_parts_oracle, new_parts_oracle)
        print("✅ Fixed parts.push oracle syntax: oracle: → o:")
        changes_made += 1
    else:
        print("⚠️  parts.push oracle syntax not found (may already be fixed)")
    
    # Verify the changes look correct
    if changes_made > 0:
        print(f"\n📋 Made {changes_made} syntax fixes")
        
        # Write the updated content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
    else:
        print("❌ No changes were needed - syntax may already be correct")
        
        # Check if 'o:"' syntax is already present
        if 'o:"' in content:
            print("✅ Found existing 'o:' syntax - file appears to already be correct")
        
        return False

def main():
    print("🔧 Fixing Scryfall oracle text search syntax")
    print("📍 Current directory:", os.getcwd())
    print()
    
    success = fix_oracle_syntax()
    
    print("\n" + "="*50)
    
    if success:
        print("🎉 Oracle syntax fix complete!")
        print("\nNext steps:")
        print("1. Run 'npm start' to test compilation")
        print("2. Test multi-word searches:")
        print("   ✅ 'deal damage' should find Lightning Bolt, etc.")
        print("   ✅ 'enters battlefield' should find ETB cards")
        print("   ✅ 'lightning' (single word) should still work")
        print("\nExpected API calls:")
        print("   - 'deal damage' → o:\"deal damage\"")
        print("   - 'lightning' → (name:lightning OR o:lightning OR type:lightning)")
    else:
        print("ℹ️  No changes made")
        print("\nIf searches still don't work:")
        print("1. Check that npm start compiles without errors")
        print("2. Look at browser console for actual API calls being made")
        print("3. Verify the API calls use 'o:' syntax instead of 'oracle:'")
        
        print("\nManual fix if needed:")
        print("1. Open src/services/scryfallApi.ts")
        print("2. Find buildEnhancedSearchQuery function")
        print("3. Change any 'oracle:' to 'o:' in template literals")

if __name__ == "__main__":
    main()
