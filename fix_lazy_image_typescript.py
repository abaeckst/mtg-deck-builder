#!/usr/bin/env python3
"""
Fix TypeScript error in LazyImage component
Remove WebkitImageRendering property that's causing compilation error
"""

import os
import re

def fix_lazy_image_typescript():
    """Fix the TypeScript error in LazyImage.tsx"""
    lazy_image_path = "src/components/LazyImage.tsx"
    
    print(f"🔧 Fixing TypeScript error in {lazy_image_path}...")
    
    with open(lazy_image_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the problematic WebkitImageRendering line
    updated_content = re.sub(
        r'            // PERFORMANCE: Optimize rendering for small images scaled up\s*\n\s*imageRendering: \'auto\',\s*\n\s*WebkitImageRendering: \'auto\',',
        '''            // PERFORMANCE: Optimize rendering for images
            imageRendering: 'auto',''',
        content,
        flags=re.MULTILINE
    )
    
    with open(lazy_image_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Fixed TypeScript error - removed WebkitImageRendering property")

def main():
    """Main execution function"""
    print("🔧 Fixing LazyImage TypeScript compilation error...")
    print()
    
    try:
        fix_lazy_image_typescript()
        print()
        print("✅ TYPESCRIPT ERROR FIXED!")
        print()
        print("🧪 Next Steps:")
        print("   1. The compilation error should now be resolved")
        print("   2. Run npm start to verify the fix")
        print("   3. Test lazy loading functionality")
        
    except Exception as e:
        print(f"❌ Error during fix: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
