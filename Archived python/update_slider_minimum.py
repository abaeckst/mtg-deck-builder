#!/usr/bin/env python3

import os
import sys

def update_slider_minimum():
    """Update slider minimum values from 0.7 to 1.3 to remove bottom third of range"""
    
    success = True
    
    # Update MTGOLayout.tsx - slider min values
    mtgo_layout_file = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(mtgo_layout_file):
        print(f"❌ Error: {mtgo_layout_file} not found")
        return False
    
    print(f"📝 Updating {mtgo_layout_file}...")
    
    with open(mtgo_layout_file, 'r', encoding='utf-8') as f:
        mtgo_content = f.read()
    
    # Replace slider min values
    original_mtgo = mtgo_content
    mtgo_content = mtgo_content.replace('min="0.7"', 'min="1.3"')
    
    if mtgo_content != original_mtgo:
        with open(mtgo_layout_file, 'w', encoding='utf-8') as f:
            f.write(mtgo_content)
        print(f"✅ Updated slider min values in {mtgo_layout_file}")
    else:
        print(f"⚠️ No slider min values found to update in {mtgo_layout_file}")
        success = False
    
    # Update useCardSizing.ts - clamp min values
    card_sizing_file = "src/hooks/useCardSizing.ts"
    
    if not os.path.exists(card_sizing_file):
        print(f"❌ Error: {card_sizing_file} not found")
        return False
    
    print(f"📝 Updating {card_sizing_file}...")
    
    with open(card_sizing_file, 'r', encoding='utf-8') as f:
        sizing_content = f.read()
    
    # Replace Math.max clamp values
    original_sizing = sizing_content
    sizing_content = sizing_content.replace('Math.max(0.7,', 'Math.max(1.3,')
    
    if sizing_content != original_sizing:
        with open(card_sizing_file, 'w', encoding='utf-8') as f:
            f.write(sizing_content)
        print(f"✅ Updated clamp min values in {card_sizing_file}")
    else:
        print(f"⚠️ No clamp min values found to update in {card_sizing_file}")
        success = False
    
    if success:
        print("\n🎉 Successfully updated minimum slider values!")
        print("📊 Changes made:")
        print("   • Slider minimum: 0.7 → 1.3")
        print("   • Hook clamps: Math.max(0.7, ...) → Math.max(1.3, ...)")
        print("   • Effective range: Removed bottom ~33% of slider")
        print("\n💡 This should improve text readability by preventing very small card sizes")
        print("   Users can now only scale from 130% to 250% instead of 70% to 250%")
    else:
        print("\n❌ Some updates failed - please check the files manually")
    
    return success

if __name__ == "__main__":
    success = update_slider_minimum()
    sys.exit(0 if success else 1)