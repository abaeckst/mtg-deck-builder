#!/usr/bin/env python3
"""
Fix html2canvas API - Use correct property names
"""

import os

def fix_html2canvas_properties():
    """Fix html2canvas to use correct API properties"""
    
    screenshot_utils_file = "src/utils/screenshotUtils.ts"
    
    if not os.path.exists(screenshot_utils_file):
        print(f"❌ {screenshot_utils_file} not found")
        return False
    
    print("🔧 Fixing html2canvas API properties...")
    
    # Read the file
    with open(screenshot_utils_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix backgroundColor -> background
    old_property = "backgroundColor: '#1a1a1a', // MTGO dark background"
    new_property = "background: '#1a1a1a', // MTGO dark background"
    
    if old_property in content:
        content = content.replace(old_property, new_property)
        
        # Write back to file
        with open(screenshot_utils_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Fixed property in {screenshot_utils_file}")
        print(f"      Changed: backgroundColor → background")
        return True
    else:
        print(f"  ℹ️  Property already correct or not found")
        return False

def main():
    """Main fix function"""
    
    print("=== HTML2CANVAS API PROPERTY FIX ===\n")
    
    if not os.path.exists('src'):
        print("❌ ERROR: Not in project root directory")
        return False
    
    if fix_html2canvas_properties():
        print("\n🎉 html2canvas API fix applied!")
        print("\nNext steps:")
        print("  1. Run: npm start")
        print("  2. Check if compilation succeeds")
    else:
        print("\n⚠️  Fix not applied - check file content manually")
    
    return True

if __name__ == "__main__":
    main()