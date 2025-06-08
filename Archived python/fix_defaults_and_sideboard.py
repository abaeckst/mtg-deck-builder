#!/usr/bin/env python3

import os
import sys

def fix_defaults_and_sideboard():
    """Fix default card sizes and remove sideboard elements from main deck area"""
    
    success = True
    
    # Update useCardSizing.ts - increase default sizes
    card_sizing_file = "src/hooks/useCardSizing.ts"
    
    if not os.path.exists(card_sizing_file):
        print(f"❌ Error: {card_sizing_file} not found")
        return False
    
    print(f"📝 Updating default card sizes in {card_sizing_file}...")
    
    with open(card_sizing_file, 'r', encoding='utf-8') as f:
        sizing_content = f.read()
    
    # Update default sizes from 1.4 to 1.6 (160% instead of 140%)
    updates = [
        ('collection: 1.4,  // 140% (1.4) default', 'collection: 1.6,  // 160% (1.6) default'),
        ('deck: 1.4,        // 140% (1.4) default', 'deck: 1.6,        // 160% (1.6) default'),
        ('sideboard: 1.4    // 140% (1.4) default', 'sideboard: 1.6    // 160% (1.6) default'),
        ('// Always start with clean defaults (140% for all areas)', '// Always start with clean defaults (160% for all areas)'),
        ('console.log(\'Initializing card sizes with 140% defaults:\', DEFAULT_SIZES);', 'console.log(\'Initializing card sizes with 160% defaults:\', DEFAULT_SIZES);'),
        ('collection: 1.4,', 'collection: 1.6,'),
        ('deck: 1.4,', 'deck: 1.6,'),
        ('sideboard: 1.4', 'sideboard: 1.6')
    ]
    
    original_sizing = sizing_content
    for old_str, new_str in updates:
        if old_str in sizing_content:
            sizing_content = sizing_content.replace(old_str, new_str)
            print(f"✅ Updated: {old_str[:50]}...")
        else:
            print(f"⚠️ Could not find: {old_str[:50]}...")
    
    if sizing_content != original_sizing:
        with open(card_sizing_file, 'w', encoding='utf-8') as f:
            f.write(sizing_content)
        print(f"✅ Updated default sizes in {card_sizing_file}")
    else:
        print(f"❌ No changes made to {card_sizing_file}")
        success = False
    
    # Update MTGOLayout.tsx - remove sideboard elements from main deck area
    mtgo_layout_file = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(mtgo_layout_file):
        print(f"❌ Error: {mtgo_layout_file} not found")
        return False
    
    print(f"📝 Fixing sideboard elements in main deck area in {mtgo_layout_file}...")
    
    with open(mtgo_layout_file, 'r', encoding='utf-8') as f:
        mtgo_content = f.read()
    
    # Remove the erroneous sideboard message in main deck area
    sideboard_message_block = '''                  
                  {sideboard.length === 0 && (
                    <div className="empty-sideboard-message">
                      Drag cards here for your sideboard
                    </div>
                  )}'''
    
    # Alternative format that might exist
    alt_sideboard_message = '''                  {sideboard.length === 0 && (
                    <div className="empty-sideboard-message">
                      Drag cards here for your sideboard
                    </div>
                  )}'''
    
    # Another possible format
    simple_sideboard_message = '''                {sideboard.length === 0 && (
                  <div className="empty-sideboard-message">
                    Drag cards here for your sideboard
                  </div>
                )}'''
    
    original_mtgo = mtgo_content
    
    # Try to find and remove the sideboard message in deck area
    if sideboard_message_block in mtgo_content:
        mtgo_content = mtgo_content.replace(sideboard_message_block, '')
        print("✅ Removed sideboard message from main deck area (format 1)")
    elif alt_sideboard_message in mtgo_content:
        mtgo_content = mtgo_content.replace(alt_sideboard_message, '')
        print("✅ Removed sideboard message from main deck area (format 2)")
    elif simple_sideboard_message in mtgo_content:
        mtgo_content = mtgo_content.replace(simple_sideboard_message, '')
        print("✅ Removed sideboard message from main deck area (format 3)")
    else:
        # Look for the pattern more flexibly
        import re
        pattern = r'\s*\{sideboard\.length === 0 && \(\s*<div className="empty-sideboard-message">\s*Drag cards here for your sideboard\s*</div>\s*\)\}'
        
        if re.search(pattern, mtgo_content):
            mtgo_content = re.sub(pattern, '', mtgo_content)
            print("✅ Removed sideboard message from main deck area (regex pattern)")
        else:
            print("⚠️ Could not find sideboard message in main deck area to remove")
    
    if mtgo_content != original_mtgo:
        with open(mtgo_layout_file, 'w', encoding='utf-8') as f:
            f.write(mtgo_content)
        print(f"✅ Updated {mtgo_layout_file}")
    else:
        print(f"⚠️ No changes made to {mtgo_layout_file}")
    
    if success:
        print("\n🎉 Successfully updated card sizing and cleaned up layout!")
        print("📊 Changes made:")
        print("   • Default card size: 140% → 160%")
        print("   • Removed sideboard elements from main deck area")
        print("\n💡 Cards should now appear larger by default")
        print("   Users will start with 160% sizing instead of 140%")
    else:
        print("\n⚠️ Some updates may have failed - please check the results")
    
    return success

if __name__ == "__main__":
    success = fix_defaults_and_sideboard()
    sys.exit(0 if success else 1)