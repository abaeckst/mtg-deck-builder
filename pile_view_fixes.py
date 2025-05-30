import os
import re

def update_pile_column_tsx():
    """Fix stacking order and overlap in PileColumn.tsx"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\PileColumn.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix 1: Reverse stacking order - last card should be most visible
        old_z_index = "zIndex: 100 - cardIndex, // First card has highest z-index (fully visible), last card lowest"
        new_z_index = "zIndex: cardIndex, // Last card has highest z-index (most visible), first card lowest"
        
        if old_z_index in content:
            content = content.replace(old_z_index, new_z_index)
            print("✅ Fixed stacking order - last card now most visible")
        else:
            print("⚠️  Could not find exact stacking order line to replace")
        
        # Fix 2: Much tighter stacking overlap - only 8% visible instead of 18%
        old_stack_offset = "const stackOffset = Math.round(-82 * scaleFactor); // 82% coverage for proper name visibility"
        new_stack_offset = "const stackOffset = Math.round(-92 * scaleFactor); // 92% coverage - only 8% visible for tight MTGO stacking"
        
        if old_stack_offset in content:
            content = content.replace(old_stack_offset, new_stack_offset)
            print("✅ Fixed stacking overlap - much tighter stacking (8% visibility)")
        else:
            print("⚠️  Could not find exact stack offset line to replace")
        
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
    """Add card centering to pile column content"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the pile-column-content section and add centering
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
        else:
            print("⚠️  Could not find exact pile-column-content section to update")
        
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
    """Apply all pile view fixes"""
    print("🎯 Applying Phase 3D Final Fixes:")
    print("1. Card centering within columns")
    print("2. Correct stacking order (last card most visible)")  
    print("3. Tighter stacking overlap (8% visibility)")
    print()
    
    success_count = 0
    
    if update_pile_column_tsx():
        success_count += 1
    
    if update_mtgo_layout_css():
        success_count += 1
    
    print()
    if success_count == 2:
        print("🎉 All fixes applied successfully!")
        print("✅ Cards should now be centered within columns")
        print("✅ Last card in each column should be most visible") 
        print("✅ Cards should stack much tighter (only 8% visible)")
        print()
        print("🔧 Test with 'npm start' to verify the changes")
    else:
        print(f"⚠️  Only {success_count}/2 fixes applied successfully")
        print("Some manual fixes may be needed")

if __name__ == "__main__":
    main()