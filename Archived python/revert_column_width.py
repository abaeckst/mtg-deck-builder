#!/usr/bin/env python3
"""
URGENT: Revert column width back to 125px - the gap disappeared at 118px
Need to restore the working state before investigating further
"""

def revert_column_width():
    """Revert column width from 118px back to 125px"""
    
    # Read the current PileColumn.tsx file
    try:
        with open('src/components/PileColumn.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
            print("✅ Successfully read PileColumn.tsx")
    except Exception as e:
        print(f"❌ Error reading PileColumn.tsx: {e}")
        return False

    # Revert the column width calculation
    current_line = "    Math.max(108, Math.round(118 * scaleFactor)); // Optimized width for perfect gap-to-column ratio"
    reverted_line = "    Math.max(110, Math.round(125 * scaleFactor)); // Balanced width - contains cards but makes gap visible"
    
    if current_line in content:
        content = content.replace(current_line, reverted_line)
        print("✅ Reverted column width from 118px back to 125px")
    else:
        # Fallback - look for the calculation
        if "Math.round(118 * scaleFactor)" in content:
            content = content.replace("Math.round(118 * scaleFactor)", "Math.round(125 * scaleFactor)")
            content = content.replace("Math.max(108,", "Math.max(110,")
            print("✅ Reverted column width calculation (fallback method)")
        else:
            print("⚠️ Could not find current width calculation to revert")
            return False

    # Write the reverted file
    try:
        with open('src/components/PileColumn.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully reverted PileColumn.tsx")
        return True
    except Exception as e:
        print(f"❌ Error writing PileColumn.tsx: {e}")
        return False

def main():
    """Main execution"""
    print("🚨 REVERTING FAILED CHANGE")
    print("=" * 35)
    print("❌ Issue: 118px columns caused gap to disappear")
    print("🔄 Action: Reverting to 125px (working state)")
    print("")
    
    if revert_column_width():
        print("=" * 35)
        print("✅ REVERT COMPLETE!")
        print("")
        print("📊 Restored:")
        print("   • Column width: 118px → 125px")
        print("   • Gap should be visible again")
        print("")
        print("🧪 Test by refreshing browser")
        print("💬 Ready for clarifying questions")
    else:
        print("❌ Revert failed - manual intervention needed")

if __name__ == "__main__":
    main()
