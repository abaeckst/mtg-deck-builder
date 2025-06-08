#!/usr/bin/env python3

import os
import sys

def fix_font_paths_proper():
    """Fix Keyrune font paths to work with React build system"""
    
    filename = "src/components/FilterPanel.css"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix font paths - use proper React public folder reference
    updates = [
        # Replace %PUBLIC_URL% with working path
        (
            '''@font-face {
  font-family: 'Keyrune';
  src: url('%PUBLIC_URL%/fonts/keyrune.woff2') format('woff2'),
       url('%PUBLIC_URL%/fonts/keyrune.woff') format('woff'),
       url('%PUBLIC_URL%/fonts/keyrune.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}''',
            '''@font-face {
  font-family: 'Keyrune';
  src: url('/fonts/keyrune.woff2') format('woff2'),
       url('/fonts/keyrune.woff') format('woff'),
       url('/fonts/keyrune.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}''',
            "Fix Keyrune font paths for React"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find font face declaration")
            # If no font face found, add it at the top
            if "@font-face" not in content:
                font_face = '''/* Keyrune Font for MTG Mana Symbols */
@font-face {
  font-family: 'Keyrune';
  src: url('/fonts/keyrune.woff2') format('woff2'),
       url('/fonts/keyrune.woff') format('woff'),
       url('/fonts/keyrune.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

'''
                content = font_face + content
                print(f"✅ Added font face declaration")
            else:
                return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_font_paths_proper()
    sys.exit(0 if success else 1)