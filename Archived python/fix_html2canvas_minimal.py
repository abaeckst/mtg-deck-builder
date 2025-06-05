#!/usr/bin/env python3
"""
Fix html2canvas - Use only supported API properties
"""

import os
import re

def fix_html2canvas_to_minimal():
    """Fix html2canvas to use only supported properties"""
    
    screenshot_utils_file = "src/utils/screenshotUtils.ts"
    
    if not os.path.exists(screenshot_utils_file):
        print(f"❌ {screenshot_utils_file} not found")
        return False
    
    print("🔧 Fixing html2canvas to use only supported properties...")
    
    # Read the file
    with open(screenshot_utils_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the html2canvas call and replace with minimal supported options
    pattern = r'const canvas = await html2canvas\(element, \{[^}]+\}\);'
    
    # Simple minimal configuration that should work
    new_call = """const canvas = await html2canvas(element, {
    background: '#1a1a1a',
    useCORS: true,
    allowTaint: true,
    logging: false
  });"""
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_call, content, flags=re.DOTALL)
        
        # Write back to file
        with open(screenshot_utils_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Simplified html2canvas options in {screenshot_utils_file}")
        print("      Removed: width, height, scrollX, scrollY (not supported)")
        print("      Kept: background, useCORS, allowTaint, logging")
        return True
    else:
        print(f"  ℹ️  html2canvas call pattern not found")
        return False

def main():
    """Main fix function"""
    
    print("=== HTML2CANVAS MINIMAL OPTIONS FIX ===\n")
    
    if not os.path.exists('src'):
        print("❌ ERROR: Not in project root directory")
        return False
    
    if fix_html2canvas_to_minimal():
        print("\n🎉 html2canvas options simplified!")
        print("\nNext steps:")
        print("  1. Run: npm start")
        print("  2. Check if compilation succeeds")
        print("  3. Test screenshot functionality")
    else:
        print("\n⚠️  Fix not applied - check file content manually")
    
    return True

if __name__ == "__main__":
    main()