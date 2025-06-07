#!/usr/bin/env python3

import os
import sys
import shutil

def fix_keyrune_fonts_src_approach():
    """Fix Keyrune font loading by moving fonts to src/assets and using proper imports"""
    
    # Step 1: Create src/assets/fonts directory
    assets_dir = "src/assets"
    fonts_dir = "src/assets/fonts"
    
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"✅ Created {assets_dir} directory")
    
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
        print(f"✅ Created {fonts_dir} directory")
    
    # Step 2: Copy font files from public/fonts to src/assets/fonts
    public_fonts = [
        "public/fonts/keyrune.woff2",
        "public/fonts/keyrune.woff", 
        "public/fonts/keyrune.ttf"
    ]
    
    for font_file in public_fonts:
        if os.path.exists(font_file):
            filename = os.path.basename(font_file)
            dest_path = os.path.join(fonts_dir, filename)
            shutil.copy2(font_file, dest_path)
            print(f"✅ Copied {font_file} to {dest_path}")
        else:
            print(f"❌ Font file not found: {font_file}")
            return False
    
    # Step 3: Update FilterPanel.css with proper imports
    css_file = "src/components/FilterPanel.css"
    
    if not os.path.exists(css_file):
        print(f"Error: {css_file} not found")
        return False
    
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the old broken @font-face declaration
    old_font_face = """@font-face {
  font-family: 'Keyrune';
  src: url('%PUBLIC_URL%/fonts/keyrune.woff2') format('woff2'),
       url('%PUBLIC_URL%/fonts/keyrune.woff') format('woff'),
       url('%PUBLIC_URL%/fonts/keyrune.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}"""

    # New @font-face with relative imports from src/assets/fonts
    new_font_face = """@font-face {
  font-family: 'Keyrune';
  src: url('../assets/fonts/keyrune.woff2') format('woff2'),
       url('../assets/fonts/keyrune.woff') format('woff'),
       url('../assets/fonts/keyrune.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}"""
    
    if old_font_face in content:
        content = content.replace(old_font_face, new_font_face)
        print("✅ Updated @font-face declaration with relative paths")
    else:
        # Try to find any @font-face with Keyrune and replace it
        import re
        font_face_pattern = r'@font-face\s*\{[^}]*font-family:\s*[\'"]Keyrune[\'"][^}]*\}'
        if re.search(font_face_pattern, content, re.DOTALL):
            content = re.sub(font_face_pattern, new_font_face, content, flags=re.DOTALL)
            print("✅ Found and replaced existing Keyrune @font-face declaration")
        else:
            # Insert new font-face at the top
            content = new_font_face + "\n\n" + content
            print("✅ Added new @font-face declaration at top of file")
    
    # Write the updated content back
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {css_file}")
    return True

if __name__ == "__main__":
    success = fix_keyrune_fonts_src_approach()
    if success:
        print("\n🎮 Font fix complete! Fonts moved to src/assets/fonts/ with proper relative imports.")
        print("✅ Run 'npm start' to see authentic MTG mana symbols!")
    else:
        print("\n❌ Font fix failed. Check the error messages above.")
    sys.exit(0 if success else 1)