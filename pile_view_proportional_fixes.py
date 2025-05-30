import os
import re

def update_pile_column_tsx():
    """Fix stacking to show only ~10% of each card proportionally"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\PileColumn.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix 1: Reverse stacking order if not already done
        if "zIndex: 100 - cardIndex" in content:
            content = content.replace(
                "zIndex: 100 - cardIndex, // First card has highest z-index (fully visible), last card lowest",
                "zIndex: cardIndex, // Last card has highest z-index (most visible), first card lowest"
            )
            print("✅ Fixed stacking order - last card now most visible")
        
        # Fix 2: Much more aggressive proportional stacking
        # Look for the current stack offset calculation
        old_patterns = [
            "const stackOffset = Math.round(-92 * scaleFactor); // 92% coverage - only 8% visible for tight MTGO stacking",
            "const stackOffset = Math.round(-82 * scaleFactor); // 82% coverage for proper name visibility"
        ]
        
        new_stack_offset = """// MTGO-style tight stacking - show only ~10% of each card (name area)
          // Typical card is ~180px tall, we want ~18px showing = 90% overlap
          const cardHeight = Math.round(180 * scaleFactor); // Estimated card height at current scale
          const visiblePortion = Math.round(cardHeight * 0.1); // Show 10% of card (name area)
          const stackOffset = -(cardHeight - visiblePortion); // Negative offset to stack tightly"""
        
        found_pattern = False
        for pattern in old_patterns:
            if pattern in content:
                content = content.replace(pattern, new_stack_offset)
                found_pattern = True
                print("✅ Fixed stacking overlap - proportional tight stacking (10% visible)")
                break
        
        if not found_pattern:
            print("⚠️  Could not find stack offset calculation to replace")
            # Try to find any stackOffset line and replace it
            if "const stackOffset = " in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "const stackOffset = " in line and "Math.round(" in line:
                        lines[i] = "          " + new_stack_offset.split('\n')[1].strip()  # Just the calculation line
                        content = '\n'.join(lines)
                        print("✅ Found and replaced stackOffset calculation")
                        break
        
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
    """Add card centering and reduce column gaps"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix 1: Add centering if not already done
        if "align-items: center;" not in content:
            old_pile_content = """.pile-column-content {
  flex: 1;
  padding: 3px;
  display: flex;
  flex-direction: column;
  position: relative;
  /* NO overflow or max-height - natural content flow */
}"""
            
            new_pile_content = """.pile-column-content {
  flex: 1;
  padding: 3px;
  display: flex;
  flex-direction: column;
  align-items: center; /* Center cards horizontally within column */
  position: relative;
  /* NO overflow or max-height - natural content flow */
}"""
            
            if old_pile_content in content:
                content = content.replace(old_pile_content, new_pile_content)
                print("✅ Added card centering to pile-column-content")
        
        # Fix 2: Reduce column gaps from 6px to 2px
        old_gap = "gap: 6px; /* Tight gaps like MTGO */"
        new_gap = "gap: 2px; /* Much tighter gaps between columns */"
        
        if old_gap in content:
            content = content.replace(old_gap, new_gap)
            print("✅ Reduced column gaps from 6px to 2px")
        else:
            # Try to find any gap: 6px in pile-columns-container
            if "gap: 6px;" in content and ".pile-columns-container" in content:
                content = content.replace("gap: 6px;", "gap: 2px;")
                print("✅ Found and reduced gap to 2px")
        
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
    """Apply all pile view fixes with proper proportional stacking"""
    print("🎯 Applying Phase 3D Final Fixes (Proportional Stacking):")
    print("1. Proportional tight stacking - 10% of card visible (scales with card size)")
    print("2. Last card most visible in stack")  
    print("3. Much tighter column gaps (2px instead of 6px)")
    print("4. Cards centered within columns")
    print()
    
    success_count = 0
    
    if update_pile_column_tsx():
        success_count += 1
    
    if update_mtgo_layout_css():
        success_count += 1
    
    print()
    if success_count == 2:
        print("🎉 All proportional fixes applied successfully!")
        print("✅ Cards should stack with only 10% visible (name area)")
        print("✅ Stacking scales proportionally with card size") 
        print("✅ Much tighter column gaps")
        print("✅ Cards centered within columns")
        print()
        print("🔧 Test with 'npm start' to verify the tight stacking")
        print("📏 Try different card sizes to see proportional scaling")
    else:
        print(f"⚠️  Only {success_count}/2 fixes applied successfully")
        print("Some manual fixes may be needed")

if __name__ == "__main__":
    main()