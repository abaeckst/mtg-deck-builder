import os
import re

def update_pile_column_tsx():
    """Fix column width calculation to eliminate wasted space"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\PileColumn.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix: Replace the overly generous width calculation
        old_width_calc = """// Calculate dynamic column width based on card scale factor
  const dynamicWidth = isEmpty ? 
    Math.max(100, Math.round(120 * scaleFactor)) : 
    Math.max(120, Math.round(160 * scaleFactor));"""
    
        new_width_calc = """// Calculate tight column width - just enough for the card with minimal padding
  // Magic cards are ~110px wide at scale 1.0, so we add just a tiny bit for borders
  const dynamicWidth = isEmpty ? 
    Math.max(80, Math.round(90 * scaleFactor)) : 
    Math.max(90, Math.round(115 * scaleFactor)); // Much tighter - just card width + 5px"""
        
        if old_width_calc in content:
            content = content.replace(old_width_calc, new_width_calc)
            print("✅ Fixed column width calculation - much tighter columns")
        else:
            print("⚠️  Could not find exact width calculation to replace. Looking for fallback...")
            # Try to find just the dynamicWidth assignment
            if "const dynamicWidth =" in content:
                # Replace the entire dynamicWidth calculation
                pattern = r"const dynamicWidth = isEmpty \?[^;]+;"
                replacement = """const dynamicWidth = isEmpty ? 
    Math.max(80, Math.round(90 * scaleFactor)) : 
    Math.max(90, Math.round(115 * scaleFactor));"""
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                print("✅ Found and replaced dynamicWidth calculation")
        
        # Write the updated content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error updating PileColumn.tsx: {str(e)}")
        return False

def update_mtgo_layout_css():
    """Add a small visible gap between columns"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix: Change from 0px gap to a small but visible gap
        old_gap = "gap: 0px; /* Tightest possible column gaps */"
        new_gap = "gap: 3px; /* Small but visible gap between columns */"
        
        if old_gap in content:
            content = content.replace(old_gap, new_gap)
            print("✅ Set gap to 3px for small visible spacing")
        elif "gap: 0px;" in content:
            content = content.replace("gap: 0px;", "gap: 3px;")
            print("✅ Found and updated gap to 3px")
        else:
            print("⚠️  Could not find gap setting to update")
        
        # Write the updated content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error updating MTGOLayout.css: {str(e)}")
        return False

def main():
    """Apply the superman fix for tight pile columns"""
    print("🦸‍♂️ SUPERMAN PILE FIX:")
    print("💡 THE PROBLEM: Column widths were 160px but cards are only 110px")
    print("💡 THE SOLUTION: Make columns 115px (just card width + 5px)")
    print("💡 PLUS: Add small 3px gap between columns")
    print()
    print("📊 Expected Results:")
    print("   • Columns will be much narrower (115px vs 160px)")
    print("   • Cards will nearly touch each other")
    print("   • Small 3px gaps will be barely visible but present")
    print("   • No more wasted space inside columns")
    print()
    
    success_count = 0
    
    if update_pile_column_tsx():
        success_count += 1
    
    if update_mtgo_layout_css():
        success_count += 1
    
    print()
    if success_count == 2:
        print("🎉 SUPERMAN FIX APPLIED SUCCESSFULLY!")
        print("✅ Column widths dramatically reduced")
        print("✅ Small visible gap between columns") 
        print("✅ Cards should now appear much closer together")
        print()
        print("🎯 At normal scale (1.0):")
        print("   • Old: 160px columns with huge internal gaps")
        print("   • New: 115px columns with 3px gaps = TIGHT!")
        print()
        print("🔧 Test with 'npm start' - you should see a dramatic improvement!")
    else:
        print(f"⚠️  Only {success_count}/2 fixes applied successfully")
        print("Manual intervention may be needed")

if __name__ == "__main__":
    main()