#!/usr/bin/env python3

import os
import sys
from datetime import datetime

def merge_load_more_css():
    """Merge load_more_styles.css into MTGOLayout.css with backup and organization"""
    
    # File paths
    load_more_file = "load_more_styles.css"
    mtgo_css_file = "src/components/MTGOLayout.css"
    backup_file = f"src/components/MTGOLayout.css.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Check if files exist
    if not os.path.exists(load_more_file):
        print(f"❌ Error: {load_more_file} not found in project root")
        print("Make sure the previous script created this file successfully")
        return False
    
    if not os.path.exists(mtgo_css_file):
        print(f"❌ Error: {mtgo_css_file} not found")
        print("Make sure you're running this from the project root directory")
        return False
    
    # Read the Load More CSS content
    try:
        with open(load_more_file, 'r', encoding='utf-8') as f:
            load_more_content = f.read().strip()
        print(f"✅ Read Load More styles from {load_more_file}")
    except Exception as e:
        print(f"❌ Error reading {load_more_file}: {e}")
        return False
    
    # Read the existing MTGOLayout.css content
    try:
        with open(mtgo_css_file, 'r', encoding='utf-8') as f:
            mtgo_content = f.read()
        print(f"✅ Read existing MTGOLayout.css ({len(mtgo_content)} characters)")
    except Exception as e:
        print(f"❌ Error reading {mtgo_css_file}: {e}")
        return False
    
    # Create backup
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(mtgo_content)
        print(f"✅ Created backup: {backup_file}")
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False
    
    # Check if Load More styles already exist (avoid duplicates)
    if ".load-more-section" in mtgo_content or ".load-more-results-btn" in mtgo_content:
        print("⚠️  Load More styles appear to already exist in MTGOLayout.css")
        print("Skipping merge to avoid duplicates")
        print("If you need to update the styles, manually remove the existing Load More section first")
        return True
    
    # Find the best insertion point - at the end of the file
    # Add Load More styles with proper section header
    load_more_section = f"""

/* ===== LOAD MORE RESULTS FUNCTIONALITY ===== */

{load_more_content}

/* ===== END LOAD MORE RESULTS STYLES ===== */"""
    
    # Merge the content
    merged_content = mtgo_content + load_more_section
    
    # Write the merged content
    try:
        with open(mtgo_css_file, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        print(f"✅ Successfully merged Load More styles into {mtgo_css_file}")
        print(f"📊 New file size: {len(merged_content)} characters")
    except Exception as e:
        print(f"❌ Error writing merged file: {e}")
        return False
    
    # Clean up the temporary load_more_styles.css file
    try:
        os.remove(load_more_file)
        print(f"✅ Cleaned up temporary file: {load_more_file}")
    except Exception as e:
        print(f"⚠️  Warning: Could not remove {load_more_file}: {e}")
    
    print("\n🎉 CSS Merge Complete!")
    print("\nNext steps:")
    print("1. Test your application: npm start")
    print("2. Verify Load More button appears with proper styling")
    print("3. Test progress indicators during loading")
    print("4. If any issues occur, restore from backup:")
    print(f"   cp {backup_file} {mtgo_css_file}")
    
    return True

if __name__ == "__main__":
    print("🔧 MTG Deck Builder - CSS Merge Script")
    print("=" * 50)
    
    # Verify we're in the right directory
    if not os.path.exists("package.json"):
        print("❌ Error: This doesn't appear to be the project root directory")
        print("Please run this script from C:/Users/carol/mtg-deck-builder/")
        sys.exit(1)
    
    success = merge_load_more_css()
    sys.exit(0 if success else 1)