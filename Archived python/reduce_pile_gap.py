#!/usr/bin/env python3
"""
Reduce pile view gap from 8px to 4px
Simple targeted fix for the final gap size
"""

def reduce_pile_gap():
    """Reduce the gap between pile columns from 8px to 4px"""
    
    # Read the current CSS file
    try:
        with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
            print("✅ Successfully read MTGOLayout.css")
    except Exception as e:
        print(f"❌ Error reading CSS file: {e}")
        return False

    # Find and replace the gap value in pile-columns-container
    # Look for gap: 8px and change it to gap: 4px
    old_gap = "gap: 8px"
    new_gap = "gap: 4px"
    
    if old_gap in css_content:
        # Replace all instances of gap: 8px with gap: 4px in the pile view section
        css_content = css_content.replace(old_gap, new_gap)
        print(f"✅ Updated gap from 8px to 4px")
        
        # Count how many replacements were made
        count = css_content.count(new_gap)
        print(f"📊 Found {count} gap declarations set to 4px")
    else:
        print("⚠️ Could not find 'gap: 8px' in CSS file")
        # Look for other gap variations
        if "gap: 8px !important" in css_content:
            css_content = css_content.replace("gap: 8px !important", "gap: 4px !important")
            print("✅ Updated gap: 8px !important to gap: 4px !important")
        else:
            print("❌ Could not find gap setting to modify")
            return False

    # Write the updated CSS back
    try:
        with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
            f.write(css_content)
        print("✅ Successfully updated MTGOLayout.css")
        return True
    except Exception as e:
        print(f"❌ Error writing CSS file: {e}")
        return False

def main():
    """Main execution"""
    print("🔧 Reducing Pile View Gap Size")
    print("=" * 40)
    print("🎯 Change: 8px gap → 4px gap")
    print("")
    
    if reduce_pile_gap():
        print("=" * 40)
        print("✅ GAP REDUCTION COMPLETE!")
        print("")
        print("🧪 Test:")
        print("   1. Refresh your browser (or restart npm)")
        print("   2. Check pile view - gap should be half the size")
        print("")
        print("🎉 Phase 3D should now be 100% complete!")
    else:
        print("❌ Gap reduction failed")

if __name__ == "__main__":
    main()
