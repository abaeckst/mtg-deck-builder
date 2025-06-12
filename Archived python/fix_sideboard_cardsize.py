#!/usr/bin/env python3
"""
Fix script to add cardSize prop to SideboardArea in MTGOLayout.tsx
Adds the missing unified cardSize prop for size slider synchronization
"""

import re
import os

def fix_sideboard_cardsize_prop():
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        print("Please run this script from the project root directory")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 FIXING SIDEBOARD CARDSIZE PROP")
    print("="*50)
    
    # Find SideboardArea component usage
    sideboard_pattern = r'(<SideboardArea[^>]*?)(\s*/>|\s*>)'
    
    def fix_sideboard_props(match):
        opening_tag = match.group(1)
        closing = match.group(2)
        
        # Check if cardSize is already present
        if 'cardSize=' in opening_tag:
            print("   ✅ cardSize prop already present in SideboardArea")
            return match.group(0)  # No change needed
        
        # Add cardSize prop using unified state
        # Find a good place to insert it (after other similar props)
        if 'viewMode=' in opening_tag:
            # Insert after viewMode prop
            opening_tag = re.sub(
                r'(viewMode={[^}]+})',
                r'\1\n          cardSize={layout.cardSizes.deckSideboard}',
                opening_tag
            )
        else:
            # Insert before the closing of the opening tag
            opening_tag += '\n          cardSize={layout.cardSizes.deckSideboard}'
        
        print("   ✅ Added cardSize={layout.cardSizes.deckSideboard} to SideboardArea")
        return opening_tag + closing
    
    # Apply the fix
    original_content = content
    content = re.sub(sideboard_pattern, fix_sideboard_props, content, flags=re.DOTALL)
    
    if content == original_content:
        print("   ⚠️  Could not find SideboardArea component or already fixed")
        print("   ℹ️  Manual inspection may be needed")
        return
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n🎯 FIX APPLIED SUCCESSFULLY!")
    print("   📁 Updated: src/components/MTGOLayout.tsx")
    print("   🔧 Added: cardSize={layout.cardSizes.deckSideboard} prop to SideboardArea")
    print("\n📋 NEXT STEPS:")
    print("   1. Save all files")
    print("   2. Test size slider - both deck and sideboard should resize together")
    print("   3. If still not working, check console for prop reception")

if __name__ == "__main__":
    fix_sideboard_cardsize_prop()
