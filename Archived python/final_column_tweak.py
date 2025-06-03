#!/usr/bin/env python3
"""
Final tweak: Reduce column width slightly more to make 4px gap appear larger
Same gap setting, better visual proportion
"""

def tweak_column_width():
    """Reduce column width from 125px to 118px for optimal gap visibility"""
    
    # Read the current PileColumn.tsx file
    try:
        with open('src/components/PileColumn.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
            print("✅ Successfully read PileColumn.tsx")
    except Exception as e:
        print(f"❌ Error reading PileColumn.tsx: {e}")
        return False

    # Find and replace the column width calculation
    old_width_line = "    Math.max(110, Math.round(125 * scaleFactor)); // Balanced width - contains cards but makes gap visible"
    new_width_line = "    Math.max(108, Math.round(118 * scaleFactor)); // Optimized width for perfect gap-to-column ratio"
    
    if old_width_line in content:
        content = content.replace(old_width_line, new_width_line)
        print("✅ Updated column width from 125px to 118px")
    else:
        # Fallback - look for the calculation
        if "Math.round(125 * scaleFactor)" in content:
            content = content.replace("Math.round(125 * scaleFactor)", "Math.round(118 * scaleFactor)")
            content = content.replace("Math.max(110,", "Math.max(108,")
            print("✅ Updated column width calculation (fallback method)")
        else:
            print("⚠️ Could not find width calculation to update")
            return False

    # Write the updated file
    try:
        with open('src/components/PileColumn.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully updated PileColumn.tsx")
        return True
    except Exception as e:
        print(f"❌ Error writing PileColumn.tsx: {e}")
        return False

def main():
    """Main execution"""
    print("🎯 Final Gap Appearance Optimization")
    print("=" * 45)
    print("📏 Change: 125px → 118px column width")
    print("🔍 Effect: 4px gap appears proportionally larger")
    print("")
    
    if tweak_column_width():
        print("=" * 45)
        print("✅ FINAL OPTIMIZATION COMPLETE!")
        print("")
        print("📊 Result:")
        print("   • Column width: 125px → 118px")
        print("   • Gap setting: 4px (unchanged)")
        print("   • Visual effect: Gap appears larger")
        print("")
        print("🧪 Test by refreshing browser")
        print("🎉 Phase 3D should now be perfect!")
    else:
        print("❌ Optimization failed")

if __name__ == "__main__":
    main()
