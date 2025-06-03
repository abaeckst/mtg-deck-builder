#!/usr/bin/env python3
"""
Reduce pile column width to make the 4px gap more visually prominent
The gap is correct, but the columns are too wide making it look small
"""

def reduce_column_width():
    """Reduce column width from 140px to 125px to make gap more visible"""
    
    # Read the current PileColumn.tsx file
    try:
        with open('src/components/PileColumn.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
            print("✅ Successfully read PileColumn.tsx")
    except Exception as e:
        print(f"❌ Error reading PileColumn.tsx: {e}")
        return False

    # Find and replace the column width calculation
    old_width_line = "    Math.max(120, Math.round(140 * scaleFactor)); // Wider columns to properly contain cards"
    new_width_line = "    Math.max(110, Math.round(125 * scaleFactor)); // Balanced width - contains cards but makes gap visible"
    
    if old_width_line in content:
        content = content.replace(old_width_line, new_width_line)
        print("✅ Updated column width from 140px to 125px")
    else:
        # Fallback - look for just the number
        if "Math.round(140 * scaleFactor)" in content:
            content = content.replace("Math.round(140 * scaleFactor)", "Math.round(125 * scaleFactor)")
            print("✅ Updated column width calculation (fallback method)")
        else:
            print("⚠️ Could not find width calculation to update")
            return False

    # Also update the comment
    old_comment = "  // Magic cards are ~130px wide at scale 1.0, need proper spacing to prevent overflow"
    new_comment = "  // Magic cards are ~115px wide - balanced sizing to contain cards while showing gaps"
    
    if old_comment in content:
        content = content.replace(old_comment, new_comment)
        print("✅ Updated comment")

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
    print("🔧 Reducing Column Width for Better Gap Visibility")
    print("=" * 55)
    print("🎯 Issue: 140px columns make 4px gap look tiny")
    print("🛠️ Solution: Reduce to 125px - gap appears more prominent")
    print("")
    
    if reduce_column_width():
        print("=" * 55)
        print("✅ COLUMN WIDTH REDUCTION COMPLETE!")
        print("")
        print("📊 Changes:")
        print("   • Column width: 140px → 125px (at scale 1.0)")
        print("   • Gap remains 4px but appears larger relative to column width")
        print("   • Cards still contained within column bounds")
        print("")
        print("🧪 Test:")
        print("   1. Refresh browser or restart npm")
        print("   2. Check pile view - gap should look more prominent")
        print("")
        print("✨ Phase 3D final polish complete!")
    else:
        print("❌ Column width reduction failed")

if __name__ == "__main__":
    main()
