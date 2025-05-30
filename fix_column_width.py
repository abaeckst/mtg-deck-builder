#!/usr/bin/env python3
"""
Fix pile column width so cards don't overflow and hide the gaps
The gap CSS is working - the issue is column width calculation
"""

def fix_column_width():
    """Fix the column width calculation in PileColumn.tsx"""
    
    # Read the current PileColumn.tsx file
    try:
        with open('src/components/PileColumn.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
            print("✅ Successfully read PileColumn.tsx")
    except Exception as e:
        print(f"❌ Error reading PileColumn.tsx: {e}")
        return False

    # Find and replace the column width calculation
    # The issue is that 115px is too narrow for Magic cards, causing overflow
    old_width_calc = """  // Calculate tight column width - just enough for the card with minimal padding
  // Magic cards are ~110px wide at scale 1.0, so we add just a tiny bit for borders
  const dynamicWidth = isEmpty ? 
    Math.max(80, Math.round(90 * scaleFactor)) : 
    Math.max(90, Math.round(115 * scaleFactor)); // Much tighter - just card width + 5px"""

    new_width_calc = """  // Calculate proper column width - ensure cards fit within column bounds
  // Magic cards are ~130px wide at scale 1.0, need proper spacing to prevent overflow
  const dynamicWidth = isEmpty ? 
    Math.max(80, Math.round(90 * scaleFactor)) : 
    Math.max(120, Math.round(140 * scaleFactor)); // Wider columns to properly contain cards"""

    if old_width_calc in content:
        content = content.replace(old_width_calc, new_width_calc)
        print("✅ Updated column width calculation to prevent card overflow")
    else:
        # Fallback - look for just the key line
        old_line = "    Math.max(90, Math.round(115 * scaleFactor)); // Much tighter - just card width + 5px"
        new_line = "    Math.max(120, Math.round(140 * scaleFactor)); // Wider columns to properly contain cards"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            print("✅ Updated column width calculation (fallback method)")
        else:
            print("⚠️ Could not find exact width calculation - showing current content around dynamicWidth")
            # Find the general area
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'dynamicWidth' in line:
                    print(f"Line {i+1}: {line}")
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
    print("🔧 Fixing Pile Column Width to Show Gaps")
    print("=" * 50)
    print("🎯 Issue: Cards overflow narrow columns, hiding the 8px gaps")
    print("🛠️ Solution: Increase column width to properly contain cards")
    print("")
    
    if fix_column_width():
        print("=" * 50)
        print("✅ COLUMN WIDTH FIX COMPLETE!")
        print("")
        print("🧪 Test:")
        print("   1. Run: npm start")
        print("   2. Switch to pile view")
        print("   3. Gaps should now be visible between columns")
        print("")
        print("📊 What changed:")
        print("   • Column width: 115px → 140px (at scale 1.0)")
        print("   • Cards now fit within column boundaries")
        print("   • 8px gaps between columns are no longer hidden")
    else:
        print("❌ Fix failed - please check the file manually")

if __name__ == "__main__":
    main()
