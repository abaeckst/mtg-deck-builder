#!/usr/bin/env python3
"""
Fix Export Features Compilation Errors
Addresses specific casing and API issues identified in diagnostic
"""

import os
import re

def fix_modal_css_import():
    """Fix the Modal.css vs modal.css casing issue"""
    
    modal_file = "src/components/Modal.tsx"
    
    if not os.path.exists(modal_file):
        print(f"❌ {modal_file} not found")
        return False
    
    print("🔧 Fixing Modal.css import casing...")
    
    # Read the file
    with open(modal_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the import statement
    old_import = "import './Modal.css';"
    new_import = "import './modal.css';"
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        
        # Write back to file
        with open(modal_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Fixed import in {modal_file}")
        print(f"      Changed: {old_import}")
        print(f"      To:      {new_import}")
        return True
    else:
        print(f"  ℹ️  Import statement not found or already correct in {modal_file}")
        return True

def fix_html2canvas_options():
    """Fix html2canvas API options to remove unsupported properties"""
    
    screenshot_utils_file = "src/utils/screenshotUtils.ts"
    
    if not os.path.exists(screenshot_utils_file):
        print(f"❌ {screenshot_utils_file} not found")
        return False
    
    print("🔧 Fixing html2canvas API options...")
    
    # Read the file
    with open(screenshot_utils_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix the html2canvas options
    # Look for the problematic options object
    pattern = r'const canvas = await html2canvas\(element, \{([^}]+)\}\);'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        old_options = match.group(1)
        
        # Create corrected options - remove 'scale' and fix property names
        new_options = """
    backgroundColor: '#1a1a1a', // MTGO dark background
    useCORS: true, // Allow cross-origin images
    allowTaint: true, // Allow tainted canvas
    logging: false, // Disable logging for cleaner output
    width: element.scrollWidth,
    height: element.scrollHeight,
    scrollX: 0,
    scrollY: 0"""
        
        # Replace the entire function call
        old_call = f"const canvas = await html2canvas(element, {{{old_options}}});"
        new_call = f"const canvas = await html2canvas(element, {{{new_options}\n  }});"
        
        content = content.replace(old_call, new_call)
        
        # Write back to file
        with open(screenshot_utils_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Fixed html2canvas options in {screenshot_utils_file}")
        print("      Removed: 'scale' property (not supported)")
        print("      Fixed: 'background' → 'backgroundColor'")
        return True
    else:
        print(f"  ℹ️  html2canvas call pattern not found in {screenshot_utils_file}")
        return False

def verify_fixes():
    """Verify that the fixes were applied correctly"""
    
    print("\n🔍 VERIFYING FIXES:")
    print("-" * 20)
    
    # Check Modal.tsx import
    modal_file = "src/components/Modal.tsx"
    if os.path.exists(modal_file):
        with open(modal_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "import './modal.css';" in content:
            print("  ✅ Modal.css import fixed correctly")
        elif "import './Modal.css';" in content:
            print("  ⚠️  Modal.css import still has casing issue")
        else:
            print("  ℹ️  Modal CSS import not found (might use different pattern)")
    
    # Check screenshotUtils.ts options
    screenshot_file = "src/utils/screenshotUtils.ts"
    if os.path.exists(screenshot_file):
        with open(screenshot_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "scale:" in content:
            print("  ⚠️  'scale' property still present in screenshotUtils.ts")
        else:
            print("  ✅ 'scale' property removed from html2canvas options")
        
        if "backgroundColor:" in content:
            print("  ✅ 'backgroundColor' property used correctly")
        elif "background:" in content:
            print("  ⚠️  'background' property still present (should be 'backgroundColor')")

def main():
    """Main fix function"""
    
    print("=== EXPORT FEATURES COMPILATION FIXES ===\n")
    
    # Check if we're in the right directory
    if not os.path.exists('src'):
        print("❌ ERROR: Not in project root directory")
        print("Please run this script from: C:\\Users\\carol\\mtg-deckbuilder")
        return False
    
    success_count = 0
    
    # Fix 1: Modal.css import casing
    if fix_modal_css_import():
        success_count += 1
    
    # Fix 2: html2canvas API options
    if fix_html2canvas_options():
        success_count += 1
    
    # Verify fixes
    verify_fixes()
    
    print(f"\n📊 SUMMARY:")
    print("-" * 12)
    print(f"  Fixes applied: {success_count}/2")
    
    if success_count == 2:
        print("  🎉 All compilation errors should be resolved!")
        print("\nNext steps:")
        print("  1. Run: npm start")
        print("  2. Test that app compiles without errors")
        print("  3. Check if export buttons appear in main deck header")
        print("  4. Test export functionality")
    else:
        print("  ⚠️  Some fixes may need manual attention")
        print("  Please check the file contents and error messages")
    
    return success_count == 2

if __name__ == "__main__":
    main()