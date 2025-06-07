#!/usr/bin/env python3

import os
import sys

def fix_keyrune_font_loading():
    """Fix Keyrune font loading in FilterPanel.css for Create React App"""
    
    css_file = "src/components/FilterPanel.css"
    
    if not os.path.exists(css_file):
        print(f"Error: {css_file} not found")
        return False
    
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the @font-face declaration to use %PUBLIC_URL% for CRA
    old_font_face = """@font-face {
  font-family: 'Keyrune';
  src: url('/fonts/keyrune.woff2') format('woff2'),
       url('/fonts/keyrune.woff') format('woff'),
       url('/fonts/keyrune.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}"""

    new_font_face = """@font-face {
  font-family: 'Keyrune';
  src: url('%PUBLIC_URL%/fonts/keyrune.woff2') format('woff2'),
       url('%PUBLIC_URL%/fonts/keyrune.woff') format('woff'),
       url('%PUBLIC_URL%/fonts/keyrune.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}"""
    
    if old_font_face in content:
        content = content.replace(old_font_face, new_font_face)
        print("✅ Fixed @font-face declaration to use %PUBLIC_URL%")
    else:
        print("❌ Could not find exact @font-face declaration to replace")
        return False
    
    # Write the updated content back
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {css_file}")
    print("✅ Keyrune fonts should now load properly with MTG mana symbols")
    return True

if __name__ == "__main__":
    success = fix_keyrune_font_loading()
    if success:
        print("\n🎮 Font fix complete! Run 'npm start' to see authentic MTG mana symbols!")
    sys.exit(0 if success else 1)