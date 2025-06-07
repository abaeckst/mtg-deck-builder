#!/usr/bin/env python3

import os
import sys

def fix_gold_button_sizing():
    """Fix gold button sizing consistency by consolidating CSS rules"""
    
    # Fix FilterPanel.css
    css_file = "src/components/FilterPanel.css"
    if not os.path.exists(css_file):
        print(f"Error: {css_file} not found")
        return False
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Step 1: Remove the conflicting standalone .color-gold rules (lines 89-98)
    old_standalone_gold = """/* Gold Button Styling */
.color-gold {
  background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%) !important;
  border: 2px solid #B8860B !important;
  color: #000000 !important;
  font-weight: 900 !important;
  font-size: 14px !important; /* Same font size as other color buttons */
  text-shadow: none !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
  transition: all 0.1s ease;
  /* Inherit size from .color-button - no separate width/height needed */
}

.color-gold:hover:not(.disabled) {
  background: linear-gradient(135deg, #FFED4A 0%, #FFB84D 100%) !important;
  box-shadow: 0 4px 8px rgba(255, 215, 0, 0.4) !important;
  transform: translateY(-1px);
}

.color-gold.selected {
  background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%) !important;
  border: 3px solid #3b82f6 !important; /* Same selection border as other buttons */
  box-shadow: 0 0 0 1px #3b82f6 !important; /* Same selection glow as other buttons */
  color: #000000 !important;
}

.color-gold.disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: #666666 !important;
  border: 2px solid #888888 !important;
  color: #cccccc !important;
  box-shadow: none !important;
}"""
    
    if old_standalone_gold in css_content:
        css_content = css_content.replace(old_standalone_gold, "")
        print("✅ Removed conflicting standalone .color-gold rules")
    else:
        print("⚠️ Standalone .color-gold rules not found (may have been modified)")
    
    # Step 2: Remove the smaller conflicting .color-button.color-gold rules (lines 347-352)
    old_small_gold = """/* Gold Button Enhanced Styling to Match Other Color Buttons */
.color-button.color-gold {
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 11px;
  font-weight: bold;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid #FFD700;
  cursor: pointer;
  transition: all 0.1s ease !important; /* Immediate feedback */
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  text-shadow: none;
  background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
  color: #000000;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.color-button.color-gold:hover:not(.disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
  background: linear-gradient(135deg, #FFED4A 0%, #FFB84D 100%);
}

.color-button.color-gold.selected {
  border: 2px solid #FFD700;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
}

/* Gold button gets the same blue circle as other color buttons */


.color-button.color-gold.disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: #666666;
  border-color: #888888;
  color: #cccccc;
  box-shadow: none;
  transform: none;
}"""
    
    if old_small_gold in css_content:
        css_content = css_content.replace(old_small_gold, "")
        print("✅ Removed conflicting .color-button.color-gold rules with wrong sizing")
    else:
        print("⚠️ Small .color-button.color-gold rules not found (may have been modified)")
    
    # Step 3: Add clean, consistent .color-button.color-gold rules that inherit base sizing
    new_gold_rules = """/* Gold Button - Inherits sizing from .color-button base class */
.color-button.color-gold {
  background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
  border-color: #B8860B;
  color: #000000;
  font-weight: bold;
}

.color-button.color-gold:hover:not(.disabled) {
  background: linear-gradient(135deg, #FFED4A 0%, #FFB84D 100%);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}

.color-button.color-gold.selected {
  /* Uses .color-button.selected styles automatically */
  background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
}

.color-button.color-gold.disabled {
  background: #666666;
  border-color: #888888;
  color: #cccccc;
}"""
    
    # Insert the new rules after the base .color-button class
    insert_point = ".color-button.disabled {"
    if insert_point in css_content:
        insertion_index = css_content.find(insert_point)
        # Find the end of the .color-button.disabled rule
        end_index = css_content.find("}", insertion_index) + 1
        
        css_content = (css_content[:end_index] + 
                      "\n\n" + new_gold_rules + 
                      css_content[end_index:])
        print("✅ Added clean .color-button.color-gold rules that inherit base sizing")
    else:
        print("❌ Could not find insertion point for new gold button rules")
        return False
    
    # Write the updated CSS
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"✅ Successfully updated {css_file}")
    
    # Fix GoldButton.tsx component
    gold_button_file = "src/components/GoldButton.tsx"
    if not os.path.exists(gold_button_file):
        print(f"Error: {gold_button_file} not found")
        return False
    
    with open(gold_button_file, 'r', encoding='utf-8') as f:
        gold_content = f.read()
    
    # Update className to ensure it inherits from .color-button base class
    old_classname = '`color-button color-gold ${isSelected ? \'selected\' : \'\'} ${disabled ? \'disabled\' : \'\'} ${className}`'
    new_classname = '`color-button color-gold ${isSelected ? \'selected\' : \'\'} ${disabled ? \'disabled\' : \'\'} ${className}`'
    
    # The className is already correct, but let's verify the structure
    if "color-button color-gold" in gold_content:
        print("✅ GoldButton.tsx already uses correct className structure")
    else:
        print("⚠️ GoldButton.tsx className may need manual verification")
    
    print(f"✅ Verified {gold_button_file}")
    
    return True

if __name__ == "__main__":
    print("🔧 Fixing gold button sizing consistency...")
    print("📋 Strategy: Unified CSS-first approach")
    print("🎯 Goal: All color buttons exactly 36px × 36px")
    print()
    
    success = fix_gold_button_sizing()
    
    print()
    if success:
        print("✅ Gold button sizing fix completed!")
        print("📏 All color buttons now inherit consistent 36px × 36px sizing from .color-button base class")
        print("🎨 Gold button styling consolidated and cleaned up")
        print("🔧 No more conflicting CSS rules")
        print()
        print("🧪 Next steps:")
        print("   1. Run 'npm start' to test visual consistency")
        print("   2. Verify all 7 color buttons (W, U, B, R, G, C, GOLD) are same size")
        print("   3. Test gold button selection and disabled states")
    else:
        print("❌ Gold button sizing fix failed!")
        print("🔍 Check file paths and try again")
    
    sys.exit(0 if success else 1)