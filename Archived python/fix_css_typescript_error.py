#!/usr/bin/env python3

import os
import sys

def fix_css_typescript_error():
    """Fix TypeScript error by using correct imageRendering values"""
    
    filename = "src/components/MagicCard.tsx"
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the problematic CSS with TypeScript-compatible values
    old_style = '''            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              display: imageLoaded ? 'block' : 'none',
              // Crisp image rendering for sharp text at small sizes
              imageRendering: scaleFactor < 0.8 ? 'crisp-edges' : 'high-quality',
              WebkitImageRendering: scaleFactor < 0.8 ? '-webkit-optimize-contrast' : 'auto',
            }}'''

    new_style = '''            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              display: imageLoaded ? 'block' : 'none',
              // Crisp image rendering for sharp text at small sizes
              imageRendering: scaleFactor < 0.8 ? 'crisp-edges' : 'auto',
              WebkitImageRendering: scaleFactor < 0.8 ? '-webkit-optimize-contrast' : 'auto',
            } as React.CSSProperties}'''

    if old_style in content:
        content = content.replace(old_style, new_style)
        print("✅ Fixed TypeScript error with correct CSS values")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {filename}")
        return True
    else:
        print("❌ Could not find the exact problematic style pattern")
        print("💡 Manual fix needed - replace the imageRendering line with:")
        print("imageRendering: scaleFactor < 0.8 ? 'crisp-edges' : 'auto',")
        print("And add: } as React.CSSProperties")
        return False

if __name__ == "__main__":
    print("🔧 Fixing TypeScript Error in Image Rendering CSS...")
    print("=" * 60)
    
    success = fix_css_typescript_error()
    
    if success:
        print("\n✅ TypeScript Error Fixed!")
        print("\n🎯 Changes Made:")
        print("• Changed 'high-quality' to 'auto' (TypeScript compatible)")
        print("• Added 'as React.CSSProperties' type assertion")
        print("• Kept 'crisp-edges' for small cards (this is the important one)")
        print("• Maintained Safari optimization")
        
        print("\n🚀 Next Steps:")
        print("1. Test the application: npm start")
        print("2. TypeScript compilation should now succeed")
        print("3. Set size slider to smallest - text should be much sharper!")
        
        print("\n📊 Expected Results:")
        print("✅ No TypeScript errors")
        print("✅ Sharp text rendering at small card sizes")
        print("✅ 'crisp-edges' prevents blur when cards are small")
        print("✅ PNG (745×1040) + crisp CSS = optimal quality")
        
    else:
        print("\n⚠️ Automatic fix failed - manual edit needed")
        print("\nIn MagicCard.tsx, change the imageRendering line to:")
        print("imageRendering: scaleFactor < 0.8 ? 'crisp-edges' : 'auto',")
        print("And change the closing }} to:")
        print("} as React.CSSProperties")
    
    sys.exit(0 if success else 1)
