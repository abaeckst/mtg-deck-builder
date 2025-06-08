#!/usr/bin/env python3

import os
import sys

def update_color_button_selection_outlines():
    """Fix color button selection outlines to be more prominent and increase button size by 50%"""
    
    # Update GoldButton.tsx to use proper CSS classes instead of inline styles
    gold_button_file = "src/components/GoldButton.tsx"
    if not os.path.exists(gold_button_file):
        print(f"Error: {gold_button_file} not found")
        return False
    
    with open(gold_button_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the entire button element to use CSS classes instead of inline styles
    old_button_style = '''      style={{
        backgroundColor: isSelected ? '#FFD700' : 'transparent',
        border: '2px solid #FFD700',
        color: isSelected ? '#000000' : '#FFD700',
        fontWeight: 'bold',
        transition: 'all 0.2s ease',
        opacity: disabled ? 0.5 : 1,
        cursor: disabled ? 'not-allowed' : 'pointer',
        boxShadow: isSelected ? '0 0 8px rgba(255, 215, 0, 0.6)' : 'none',
      }}'''
    
    if old_button_style in content:
        content = content.replace(old_button_style, '')
        print("✅ Removed inline styles from GoldButton component")
    else:
        print("ℹ️ Inline styles not found in GoldButton (may already be removed)")
    
    # Write the updated content
    with open(gold_button_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Update FilterPanel.css to enhance selection outlines and increase button size
    css_file = "src/components/FilterPanel.css"
    if not os.path.exists(css_file):
        print(f"Error: {css_file} not found")
        return False
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Replace existing color button styling with enhanced version
    old_color_button_css = '''.color-button {
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 11px;
  font-weight: bold;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  text-shadow: none;
}

.color-button:hover:not(.disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.color-button.selected {
  border: 2px solid #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}'''

    new_color_button_css = '''.color-button {
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 14px;
  font-weight: bold;
  width: 36px;  /* Increased from 24px (50% larger) */
  height: 36px; /* Increased from 24px (50% larger) */
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.1s ease; /* Faster for responsiveness */
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  text-shadow: none;
}

.color-button:hover:not(.disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.color-button.selected {
  border: 4px solid #3b82f6 !important; /* Much thicker and more prominent */
  box-shadow: 0 0 0 2px #3b82f6, 0 0 12px rgba(59, 130, 246, 0.5) !important; /* Enhanced glow */
  transform: scale(1.05); /* Slight scale increase when selected */
}'''

    if old_color_button_css in css_content:
        css_content = css_content.replace(old_color_button_css, new_color_button_css)
        print("✅ Updated color button base styling with larger size and enhanced selection")
    else:
        print("❌ Could not find existing color button CSS to replace")
        return False
    
    # Update the gold button specific styling to match the new size and selection style
    old_gold_css = '''.color-gold {
  background: #FFD700 !important;
  border: 1px solid #B8860B !important;
  color: #000000 !important;
  font-weight: 900 !important;
  font-size: 9px !important;
  text-shadow: none !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
  transition: all 0.2s ease;
}

.color-gold:hover:not(.disabled) {
  background: linear-gradient(135deg, #FFED4A 0%, #FFB84D 100%);
  box-shadow: 0 4px 8px rgba(255, 215, 0, 0.4);
  transform: translateY(-1px);
}

.color-gold.selected {
  background: #FFD700;
  box-shadow: 0 0 0 1px #3b82f6;
  border-color: #3b82f6;
  color: #000000;
}

.color-gold.disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: #666666;
  border-color: #888888 !important;
  color: #cccccc;
  box-shadow: none;
}'''

    new_gold_css = '''.color-gold {
  background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%) !important;
  border: 2px solid #B8860B !important;
  color: #000000 !important;
  font-weight: 900 !important;
  font-size: 12px !important; /* Increased font size for larger button */
  text-shadow: none !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
  transition: all 0.1s ease; /* Faster for responsiveness */
}

.color-gold:hover:not(.disabled) {
  background: linear-gradient(135deg, #FFED4A 0%, #FFB84D 100%) !important;
  box-shadow: 0 4px 8px rgba(255, 215, 0, 0.4) !important;
  transform: translateY(-1px);
}

.color-gold.selected {
  background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%) !important;
  border: 4px solid #3b82f6 !important; /* Same prominent selection as other buttons */
  box-shadow: 0 0 0 2px #3b82f6, 0 0 12px rgba(59, 130, 246, 0.5) !important; /* Enhanced glow */
  color: #000000 !important;
  transform: scale(1.05); /* Same scale increase as other buttons */
}

.color-gold.disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: #666666 !important;
  border: 2px solid #888888 !important;
  color: #cccccc !important;
  box-shadow: none !important;
  transform: none !important;
}'''

    if old_gold_css in css_content:
        css_content = css_content.replace(old_gold_css, new_gold_css)
        print("✅ Updated gold button styling with larger size and prominent selection")
    else:
        print("❌ Could not find existing gold button CSS to replace")
        return False
    
    # Write the updated CSS
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print("✅ Successfully updated color button selection outlines and size")
    print("🎯 Changes made:")
    print("   - Color buttons are now 50% larger (36px instead of 24px)")
    print("   - Selection border is 4px thick (much more prominent)")
    print("   - Enhanced blue glow effect around selected buttons")
    print("   - Slight scale increase (1.05) when selected for extra emphasis")
    print("   - Gold button gets the same prominent selection treatment")
    print("   - Faster transitions (0.1s) for immediate responsiveness")
    return True

if __name__ == "__main__":
    success = update_color_button_selection_outlines()
    sys.exit(0 if success else 1)