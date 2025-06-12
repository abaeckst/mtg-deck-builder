#!/usr/bin/env python3
"""
Fix duplicate cardSize attributes in MTGOLayout.tsx
Removes the old cardSize={cardSizes.sideboard} and keeps the unified one
"""

import os
import re

def fix_duplicate_cardsize():
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 FIXING DUPLICATE CARDSIZE ATTRIBUTES")
    print("="*40)
    
    # Remove the old cardSize={cardSizes.sideboard} line
    # Keep the new cardSize={layout.cardSizes.deckSideboard} line
    
    # Pattern to find and remove the old cardSize line
    old_cardsize_pattern = r'\s*cardSize=\{cardSizes\.sideboard\}\s*\n'
    
    original_content = content
    content = re.sub(old_cardsize_pattern, '', content)
    
    if content != original_content:
        print("✅ Removed old cardSize={cardSizes.sideboard} attribute")
    else:
        # Try alternative patterns
        alt_patterns = [
            r'\s*cardSize=\{cardSizes\.sideboard\}',
            r'cardSize=\{cardSizes\.sideboard\}\s*',
            r'cardSize=\{cardSizes\.sideboard\}'
        ]
        
        for pattern in alt_patterns:
            new_content = re.sub(pattern, '', content)
            if new_content != content:
                content = new_content
                print(f"✅ Removed old cardSize attribute using pattern: {pattern}")
                break
        else:
            print("❌ Could not find the duplicate cardSize={cardSizes.sideboard} to remove")
            print("📝 Manual fix needed:")
            print("   1. Find line ~700: cardSize={cardSizes.sideboard}")
            print("   2. Delete that entire line")
            print("   3. Keep the line: cardSize={layout.cardSizes.deckSideboard}")
            return
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ DUPLICATE ATTRIBUTE FIXED!")
    print("   📁 Updated: src/components/MTGOLayout.tsx")
    print("   ❌ Removed: cardSize={cardSizes.sideboard}")
    print("   ✅ Kept: cardSize={layout.cardSizes.deckSideboard}")
    print("\n📋 NEXT STEPS:")
    print("   1. App should now compile successfully")
    print("   2. Test size slider - deck and sideboard should resize together")

if __name__ == "__main__":
    fix_duplicate_cardsize()
