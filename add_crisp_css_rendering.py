#!/usr/bin/env python3

import os
import sys

def add_crisp_css_rendering():
    """Add CSS image-rendering properties for crisp scaling at small sizes"""
    
    filename = "src/components/MagicCard.tsx"
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the image style to include crisp rendering properties
    old_img_style = '''            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              display: imageLoaded ? 'block' : 'none',
            }}'''

    new_img_style = '''            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              display: imageLoaded ? 'block' : 'none',
              // Crisp image rendering for sharp text at small sizes
              imageRendering: scaleFactor < 0.8 ? 'crisp-edges' : 'high-quality',
              WebkitImageRendering: scaleFactor < 0.8 ? '-webkit-optimize-contrast' : 'auto',
            }}'''

    if old_img_style in content:
        content = content.replace(old_img_style, new_img_style)
        print("✅ Added crisp image rendering CSS properties")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {filename}")
        return True
    else:
        print("❌ Could not find the exact image style pattern to update")
        print("💡 The image style may have been modified. Here's what to add manually:")
        print("\nAdd these lines to the img style object:")
        print("imageRendering: scaleFactor < 0.8 ? 'crisp-edges' : 'high-quality',")
        print("WebkitImageRendering: scaleFactor < 0.8 ? '-webkit-optimize-contrast' : 'auto',")
        return False

if __name__ == "__main__":
    print("🎨 Adding Crisp CSS Rendering for Sharp Image Scaling...")
    print("=" * 60)
    
    success = add_crisp_css_rendering()
    
    if success:
        print("\n✅ CSS Rendering Update Complete!")
        print("\n🎯 What Was Added:")
        print("• crisp-edges rendering for small card sizes (scaleFactor < 0.8)")
        print("• high-quality rendering for larger card sizes")
        print("• Safari optimization with -webkit-optimize-contrast")
        print("• Smart scaling based on your card size slider")
        
        print("\n🚀 Next Steps:")
        print("1. Test the application: npm start")
        print("2. Set size slider to smallest setting")
        print("3. Card text should now be much sharper and more readable!")
        print("4. Try different sizes - should see crisp rendering throughout")
        
        print("\n📊 Expected Results:")
        print("✅ Sharp, readable card names at smallest sizes")
        print("✅ Crisp mana symbols and set symbols")
        print("✅ Clear artwork details instead of blur")
        print("✅ Professional quality text rendering")
        
        print("\n🔧 Technical Details:")
        print("• PNG source (745×1040) + crisp CSS = optimal quality")
        print("• Browser uses pixel-perfect scaling for small cards")
        print("• Automatic switch to smooth scaling for larger cards")
        
    else:
        print("\n⚠️ Automatic update failed - manual edit needed")
        print("\nPlease add these CSS properties to the img element in MagicCard.tsx:")
        print("imageRendering: scaleFactor < 0.8 ? 'crisp-edges' : 'high-quality',")
        print("WebkitImageRendering: scaleFactor < 0.8 ? '-webkit-optimize-contrast' : 'auto',")
    
    sys.exit(0 if success else 1)
