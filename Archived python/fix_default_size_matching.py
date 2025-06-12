#!/usr/bin/env python3
"""
Fix default card size mismatch between collection and deck/sideboard areas.
Collection default (1 on 0-2 scale) should visually match deck/sideboard default.
"""

import re

def fix_default_size_matching():
    uselayout_path = "src/hooks/useLayout.ts"
    
    try:
        with open(uselayout_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing default card size mismatch...")
        
        # Find the current deckSideboard default value (1.6)
        current_default_match = re.search(r'deckSideboard:\s*([0-9.]+),\s*//.*UNIFIED', content)
        if current_default_match:
            current_default = current_default_match.group(1)
            print(f"📊 Current deck/sideboard default: {current_default}")
        
        # Change deckSideboard default from 1.6 to 1.3 to match collection visual size
        # Collection uses scale 0-2 with default 1, which should match deck/sideboard 1.3 (minimum of 1.3-2.5 scale)
        print("🔧 Updating deck/sideboard default size to match collection...")
        
        content = re.sub(
            r'(deckSideboard:\s*)([0-9.]+)(,\s*//.*UNIFIED.*)',
            r'\g<1>1.3\g<3>',
            content
        )
        
        # Verify the change was made
        if 'deckSideboard: 1.3,' not in content:
            print("❌ Failed to update deckSideboard default")
            return False
        
        # Save the file
        with open(uselayout_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Default card sizes now match visually!")
        print("   • Collection default: 1 (on 0-2 scale)")
        print("   • Deck/Sideboard default: 1.3 (on 1.3-2.5 scale)")
        print("   • Both should now appear the same visual size by default")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = fix_default_size_matching()
    if success:
        print("\n🎯 Default sizes fixed! All areas should now have matching visual card sizes by default.")
        print("📝 Note: You may need to refresh or reset size sliders to see the new default.")
    else:
        print("\n❌ Fix failed. Manual correction needed.")
