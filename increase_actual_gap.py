#!/usr/bin/env python3
"""
Increase the actual gap between columns from 4px to 6px
Keep column width at 125px, just make more physical space between columns
"""

def increase_gap_size():
    """Increase gap from 4px to 6px for better MTGO-style spacing"""
    
    # Read the current CSS file
    try:
        with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
            print("✅ Successfully read MTGOLayout.css")
    except Exception as e:
        print(f"❌ Error reading CSS file: {e}")
        return False

    # Find and replace the gap value - increase from 4px to 6px
    old_gap = "gap: 4px"
    new_gap = "gap: 6px"
    
    # Count and replace all instances
    gap_count = css_content.count(old_gap)
    if gap_count > 0:
        css_content = css_content.replace(old_gap, new_gap)
        print(f"✅ Updated {gap_count} instances of gap from 4px to 6px")
    else:
        print("⚠️ No 'gap: 4px' found - checking for !important version")
        
    # Also check for !important version
    old_gap_important = "gap: 4px !important"
    new_gap_important = "gap: 6px !important"
    
    important_count = css_content.count(old_gap_important)
    if important_count > 0:
        css_content = css_content.replace(old_gap_important, new_gap_important)
        print(f"✅ Updated {important_count} instances of gap: 4px !important to 6px !important")

    if gap_count == 0 and important_count == 0:
        print("❌ Could not find any gap settings to update")
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
    print("📏 Increasing Physical Gap Between Columns")
    print("=" * 50)
    print("🎯 Goal: More physical space between columns (MTGO-style)")
    print("📊 Change: gap: 4px → gap: 6px")
    print("🏗️ Column width: Stays at 125px (cards properly contained)")
    print("")
    
    if increase_gap_size():
        print("=" * 50)
        print("✅ GAP INCREASE COMPLETE!")
        print("")
        print("📊 Result:")
        print("   • Gap: 4px → 6px (50% wider spacing)")
        print("   • Column width: 125px (unchanged)")
        print("   • Cards: Still properly contained")
        print("")
        print("🧪 Test:")
        print("   1. Refresh browser")
        print("   2. Check pile view - columns should feel less cramped")
        print("   3. Should match MTGO spacing better")
        print("")
        print("✨ Phase 3D pile view spacing optimized!")
    else:
        print("❌ Gap increase failed")

if __name__ == "__main__":
    main()
