#!/usr/bin/env python3
"""
Fix Load More in Card view by adding a trigger to force re-render
without resetting scroll position
"""

import re

def fix_load_more_rendering():
    """Apply minimal fix to force Card view re-render for Load More"""
    
    try:
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ MTGOLayout.tsx not found")
        return False
    
    # Find the collection-grid div and add a data attribute that changes with cards.length
    # This forces React to re-render without affecting scroll position
    pattern = r'(<div\s+className="collection-grid")'
    
    replacement = r'<div\n                className="collection-grid"\n                data-card-count={cards.length}'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print("✅ Added data-card-count attribute to collection-grid")
    else:
        print("❌ Could not find collection-grid pattern")
        return False
    
    # Write the fixed content back
    try:
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully applied Load More fix")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def main():
    """Main execution"""
    print("🚀 Applying Load More Card view fix")
    print("=" * 50)
    
    success = fix_load_more_rendering()
    
    if success:
        print("\n🎯 SUCCESS! Fix applied:")
        print("✅ Added data-card-count attribute to collection-grid")
        print("✅ This forces React to re-render when cards.length changes")
        print("✅ No scroll position reset (better than key prop solution)")
        print("\nThe collection-grid will now re-render whenever new cards")
        print("are loaded, making Load More work in Card view!")
        print("\nYou can now test the Load More functionality in Card view.")
    else:
        print("\n❌ Fix failed - please check the file manually")
    
    return success

if __name__ == "__main__":
    main()
