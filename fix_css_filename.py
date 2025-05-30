#!/usr/bin/env python3
"""
Fix the CSS filename case sensitivity issue
"""

import os
import shutil

def fix_css_filename():
    """Fix the SearchAutocomplete CSS filename"""
    wrong_name = "src/components/SearchAutoComplete.css"
    correct_name = "src/components/SearchAutocomplete.css"
    
    try:
        if os.path.exists(wrong_name):
            # Rename the file to correct case
            shutil.move(wrong_name, correct_name)
            print(f"✅ Renamed {wrong_name} to {correct_name}")
            return True
        elif os.path.exists(correct_name):
            print(f"✅ File already exists with correct name: {correct_name}")
            return True
        else:
            print(f"❌ Neither {wrong_name} nor {correct_name} found")
            print("   Please create the SearchAutocomplete.css file manually")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing CSS filename: {e}")
        return False

def main():
    """Run the CSS filename fix"""
    print("🔧 Fixing SearchAutocomplete CSS filename")
    print("=" * 45)
    
    if not os.path.exists("src/components"):
        print("❌ Error: components directory not found")
        return False
    
    if fix_css_filename():
        print("=" * 45)
        print("🎉 CSS filename should now be correct!")
        print("\n🔧 Next Steps:")
        print("1. Run 'npm start' to verify compilation")
    else:
        print("❌ Fix failed. You may need to create the CSS file manually.")
    
    return True

if __name__ == "__main__":
    main()