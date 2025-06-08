#!/usr/bin/env python3

import os
import sys

def fix_gold_button_size_and_selection():
    """Fix gold button size to match other buttons, remove weird blue circles, and tone down selection border"""
    
    # Update FilterPanel.css to fix all the issues
    css_file = "src/components/FilterPanel.css"
    if not os.path.exists(css_file):
        print(f"Error: {css_file} not found")
        return False
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Remove any weird blue circle ::after pseudo-elements that might exist
    blue_circle_patterns = [
        '''.color-button.selected::after {
  content: '';
  position: absolute;
  top: -6px;
  right: -6px;
  width: 16px;
  height: 16px;
  background: #3b82f6;
  border: 3px solid #ffffff;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.6);
  z-index: 10;
  animation: blueCircleAppear 0.2s ease;
}''',
        '''.color-button.color-gold.selected::after {
  content: '';
  position: absolute;
  top: -6px;
  right: -6px;
  width: 16px;
  height: 16px;
  background: #3b82f6;
  border: 3px solid #ffffff;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.6);
  z-index: 10;
  animation: blueCircleAppear 0.2s ease;
}''',
        '''@keyframes blueCircleAppear {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}'''
    ]
    
    for pattern in blue_circle_patterns:
        if pattern in css_content:
            css_content = css_content.replace(pattern, '')
            print("✅ Removed weird blue circle styling")
    
    # Fix the color button base styling - tone down the selection border
    old_selection_css = '''.color-button.selected {
  border: 4px solid #3b82f6 !important; /* Much thicker and more prominent */
  box-shadow: 0 0 0 2px #3b82f6, 0 0 12px rgba(59, 130, 246, 0.5) !important; /* Enhanced glow */
  transform: scale(1.05); /* Slight scale increase when selected */
}'''

    new_selection_css = '''.color-button.selected {
  border: 3px solid #3b82f6 !important; /* Prominent but not overwhelming */
  box-shadow: 0 0 0 1px #3b82f6 !important; /* Cleaner, less aggressive glow */
}'''

    if old_selection_css in css_content:
        css_content = css_content.replace(old_selection_css, new_selection_css)
        print("✅ Toned down selection border styling")
    
    # Most importantly: Fix the gold button to be the same size as other color buttons
    old_gold_css = '''.color-gold {
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

    new_gold_css = '''.color-gold {
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
}'''

    if old_gold_css in css_content:
        css_content = css_content.replace(old_gold_css, new_gold_css)
        print("✅ Fixed gold button to be same size as other color buttons")
    else:
        print("ℹ️ Gold button CSS not found in expected format, searching for alternative...")
        
        # Look for any existing gold button styling and replace it
        if '.color-gold {' in css_content:
            import re
            # Find the gold button CSS block and replace it
            gold_pattern = r'\.color-gold \{[^}]*\}(?:\s*\.color-gold[^}]*\{[^}]*\})*'
            css_content = re.sub(gold_pattern, new_gold_css.split('\n\n')[0], css_content, flags=re.DOTALL)
            print("✅ Updated existing gold button styling")
    
    # Write the updated CSS
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print("✅ Successfully fixed gold button size and selection styling")
    print("🎯 Changes made:")
    print("   - Removed weird blue circles (::after pseudo-elements)")
    print("   - Gold button now same size as other color buttons (36px)")
    print("   - Toned down selection border to 3px (less aggressive)")
    print("   - Cleaner selection glow effect")
    print("   - Gold button inherits size from base .color-button class")
    return True

if __name__ == "__main__":
    success = fix_gold_button_size_and_selection()
    sys.exit(0 if success else 1)