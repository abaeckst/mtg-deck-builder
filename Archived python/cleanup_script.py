#!/usr/bin/env python3
"""
Script to fix filename casing issues and clean up duplicate files
"""

import os
import shutil

def fix_filename_casing():
    """Fix filename casing issues"""
    
    # Define the files that need to be properly named
    files_to_check = [
        ('src/components/modal.tsx', 'src/components/Modal.tsx'),
        ('src/components/Modal.css', 'src/components/Modal.css'),  # Should be correct
        ('src/utils/deckformatting.ts', 'src/utils/deckFormatting.ts'),
        ('src/utils/screenshotutils.ts', 'src/utils/screenshotUtils.ts'),
        ('src/utils/ScreenshotUtils.ts', 'src/utils/screenshotUtils.ts'),  # Remove duplicate
    ]
    
    print("🔧 Fixing filename casing issues...")
    
    # First, remove any duplicate files with wrong casing
    duplicates_to_remove = [
        'src/utils/ScreenshotUtils.ts',
        'src/components/screenshot_utils.tsx'  # This seems to be a corrupted file
    ]
    
    for duplicate in duplicates_to_remove:
        if os.path.exists(duplicate):
            os.remove(duplicate)
            print(f"✅ Removed duplicate file: {duplicate}")
    
    # Now fix the casing by renaming files
    for old_name, new_name in files_to_check:
        if os.path.exists(old_name) and old_name != new_name:
            # Create a temporary name to avoid case-sensitivity issues on Windows
            temp_name = old_name + '.temp'
            os.rename(old_name, temp_name)
            os.rename(temp_name, new_name)
            print(f"✅ Renamed {old_name} to {new_name}")
        elif os.path.exists(new_name):
            print(f"✅ {new_name} already exists with correct casing")
        else:
            print(f"⚠️  Neither {old_name} nor {new_name} found")

def main():
    """Main function"""
    print("🚀 Fixing filename casing and cleaning up duplicates...")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('src'):
        print("❌ Error: This script should be run from the project root directory")
        print("   Expected to find 'src' folder")
        return
    
    fix_filename_casing()
    
    print()
    print("🎉 Cleanup completed!")
    print()
    print("Next steps:")
    print("1. Make sure all the new component files are saved with correct names")
    print("2. Run: npm start")
    print("3. Check for any remaining compilation errors")

if __name__ == '__main__':
    main()