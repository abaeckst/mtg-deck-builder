#!/usr/bin/env python3
"""
Fix 3: Custom Standard Enhancement
Updates the custom-standard format to include Final Fantasy (FIN) set cards
Changes query from 'legal:standard' to '(legal:standard OR set:FIN)'
"""

import re
import os

def fix_custom_standard():
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        print("Make sure you're running this script from the project root directory (c:\\Users\\carol\\mtg-deckbuilder)")
        return False
    
    print(f"🔧 Reading {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print("📝 Original content length:", len(content))
        
        # Find and replace the custom-standard logic
        old_custom_standard = """  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Use standard legality as base
      // In future phases, this will be extended to include unreleased sets
      searchQuery += ` legal:standard`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }"""
        
        new_custom_standard = """  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Standard-legal cards + Final Fantasy set
      searchQuery += ` (legal:standard OR set:FIN)`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }"""
        
        if old_custom_standard in content:
            content = content.replace(old_custom_standard, new_custom_standard)
            print("✅ Updated custom-standard format logic")
            print("   - BEFORE: legal:standard only")
            print("   - AFTER: (legal:standard OR set:FIN)")
        else:
            print("⚠️  Could not find exact custom-standard pattern. Trying alternative approach...")
            
            # Try alternative pattern matching
            pattern = re.compile(
                r'if \(filters\.format === \'custom-standard\'\) \{.*?searchQuery \+= ` legal:standard`;',
                re.DOTALL
            )
            
            replacement = """if (filters.format === 'custom-standard') {
      // Custom Standard: Standard-legal cards + Final Fantasy set
      searchQuery += ` (legal:standard OR set:FIN)`;"""
            
            new_content = pattern.sub(replacement, content)
            
            if new_content != content:
                content = new_content
                print("✅ Updated custom-standard format logic (alternative pattern)")
            else:
                print("❌ Could not find custom-standard pattern to update")
                return False
        
        print(f"📝 Updated content length: {len(content)}")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ SUCCESS: Custom Standard enhancement applied to {file_path}")
        print("🧪 TEST REQUIRED:")
        print("   1. Select 'Custom Standard (Standard + Unreleased)' format")
        print("   2. Search should now return standard-legal cards + Final Fantasy cards")
        print("   3. Verify other formats still work correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to process {file_path}: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 MTG Deck Builder - Fix 3: Custom Standard Enhancement")
    print("=" * 60)
    print("This script enhances Custom Standard to include Final Fantasy (FIN) set cards")
    print("in addition to standard-legal cards.\n")
    
    success = fix_custom_standard()
    
    if success:
        print("\n🎉 Custom Standard enhancement completed successfully!")
        print("📋 Next steps:")
        print("   1. Test Custom Standard format filter")
        print("   2. Verify Final Fantasy cards appear in results")
        print("   3. Verify other formats still work correctly")
        print("   4. Run npm start to test the complete application")
        print("\n🏆 ALL THREE FIXES COMPLETED!")
        print("   ✅ Fix 1: Color Identity correction")
        print("   ✅ Fix 2: Set Filter addition")  
        print("   ✅ Fix 3: Custom Standard enhancement")
    else:
        print("\n❌ Custom Standard enhancement failed. Please check the error messages above.")
