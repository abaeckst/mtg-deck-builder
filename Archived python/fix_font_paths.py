#!/usr/bin/env python3

import os
import sys

def fix_font_paths():
    """Fix Keyrune font paths in FilterPanel.css"""
    
    filename = "src/components/FilterPanel.css"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix font paths - use proper relative paths for public folder
    updates = [
        # Fix font path declarations
        (
            '''@font-face {
  font-family: 'Keyrune';
  src: url('/fonts/keyrune.woff2') format('woff2'),
       url('/fonts/keyrune.woff') format('woff'),
       url('/fonts/keyrune.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}''',
            '''@font-face {
  font-family: 'Keyrune';
  src: url('%PUBLIC_URL%/fonts/keyrune.woff2') format('woff2'),
       url('%PUBLIC_URL%/fonts/keyrune.woff') format('woff'),
       url('%PUBLIC_URL%/fonts/keyrune.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}''',
            "Fix Keyrune font paths to use %PUBLIC_URL%"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            # Check if fonts exist in public folder
            font_files = ['keyrune.woff2', 'keyrune.woff', 'keyrune.ttf']
            missing_fonts = []
            for font in font_files:
                if not os.path.exists(f'public/fonts/{font}'):
                    missing_fonts.append(font)
            
            if missing_fonts:
                print(f"⚠️ Missing font files in public/fonts/: {missing_fonts}")
                print("Please ensure Keyrune font files are in public/fonts/ directory")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_font_paths()
    sys.exit(0 if success else 1)