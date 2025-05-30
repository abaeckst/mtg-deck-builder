#!/usr/bin/env python3
"""
Fix 1: Color Identity Filter Correction
Replaces all 'color' queries with 'id' queries in scryfallApi.ts
This fixes the critical issue where color identity filter was using casting cost instead of actual color identity
"""

import re
import os

def fix_color_identity_api():
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
        
        # Track all replacements for verification
        replacements_made = []
        original_content = content
        
        # Fix 1: Replace color=C with id=C (colorless handling)
        old_pattern1 = 'searchQuery += ` color=C`;'
        new_pattern1 = 'searchQuery += ` id=C`;'
        if old_pattern1 in content:
            content = content.replace(old_pattern1, new_pattern1)
            replacements_made.append(f"✅ Fixed colorless: {old_pattern1} → {new_pattern1}")
        
        # Fix 2: Replace color=${colorQuery} with id=${colorQuery} (exact match)
        old_pattern2 = 'searchQuery += ` color=${colorQuery}`;'
        new_pattern2 = 'searchQuery += ` id=${colorQuery}`;'
        if old_pattern2 in content:
            content = content.replace(old_pattern2, new_pattern2)
            replacements_made.append(f"✅ Fixed exact match: {old_pattern2} → {new_pattern2}")
        
        # Fix 3: Replace color<=${colorQuery} with id<=${colorQuery} (subset match)
        old_pattern3 = 'searchQuery += ` color<=${colorQuery}`;'
        new_pattern3 = 'searchQuery += ` id<=${colorQuery}`;'
        if old_pattern3 in content:
            content = content.replace(old_pattern3, new_pattern3)
            replacements_made.append(f"✅ Fixed subset match: {old_pattern3} → {new_pattern3}")
        
        # Fix 4: Replace color:${colorQuery} with id:${colorQuery} (include match)
        old_pattern4 = 'searchQuery += ` color:${colorQuery}`;'
        new_pattern4 = 'searchQuery += ` id:${colorQuery}`;'
        if old_pattern4 in content:
            content = content.replace(old_pattern4, new_pattern4)
            replacements_made.append(f"✅ Fixed include match: {old_pattern4} → {new_pattern4}")
        
        # Fix 5: Handle complex colorless combinations
        old_pattern5 = '(color=C OR color=${otherColors})'
        new_pattern5 = '(id=C OR id=${otherColors})'
        if old_pattern5 in content:
            content = content.replace(old_pattern5, new_pattern5)
            replacements_made.append(f"✅ Fixed colorless combination: {old_pattern5} → {new_pattern5}")
        
        # Fix 6: Handle subset with colorless
        old_pattern6 = 'color<=${otherColors}C'
        new_pattern6 = 'id<=${otherColors}C'
        if old_pattern6 in content:
            content = content.replace(old_pattern6, new_pattern6)
            replacements_made.append(f"✅ Fixed subset colorless: {old_pattern6} → {new_pattern6}")
        
        # Fix 7: Handle include with colorless  
        old_pattern7 = '(color:C OR color:${otherColors})'
        new_pattern7 = '(id:C OR id:${otherColors})'
        if old_pattern7 in content:
            content = content.replace(old_pattern7, new_pattern7)
            replacements_made.append(f"✅ Fixed include colorless: {old_pattern7} → {new_pattern7}")
        
        if not replacements_made:
            print("⚠️  No color identity patterns found to replace. File may already be updated or patterns may have changed.")
            return False
        
        print(f"\n🔧 REPLACEMENTS MADE:")
        for replacement in replacements_made:
            print(f"   {replacement}")
        
        print(f"\n📝 Updated content length: {len(content)}")
        print(f"📝 Content changed: {'Yes' if content != original_content else 'No'}")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"\n✅ SUCCESS: Color identity fix applied to {file_path}")
        print("🧪 TEST REQUIRED: Search for 'Alesha, Who Smiles at Death' with W/B/R color identity filter")
        print("   - Should now appear in results (was missing before)")
        print("   - Verify other color identity searches work correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to process {file_path}: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 MTG Deck Builder - Fix 1: Color Identity API Correction")
    print("=" * 60)
    print("This script fixes the color identity filter to use actual color identity")
    print("instead of casting cost only.\n")
    
    success = fix_color_identity_api()
    
    if success:
        print("\n🎉 Color identity fix completed successfully!")
        print("📋 Next steps:")
        print("   1. Test the color identity filter with various cards")
        print("   2. Run npm start to verify the application still works")
        print("   3. Proceed with Fix 2 (Set Filter Addition)")
    else:
        print("\n❌ Color identity fix failed. Please check the error messages above.")
