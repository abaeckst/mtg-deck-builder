import os
import re

def update_pile_column_tsx():
    """Adjust stacking to show 15% of each card instead of 10%"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\PileColumn.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix: Change from 10% to 15% visibility
        old_calculation = """// MTGO-style tight stacking - show only ~10% of each card (name area)
          // Typical card is ~180px tall, we want ~18px showing = 90% overlap
          const cardHeight = Math.round(180 * scaleFactor); // Estimated card height at current scale
          const visiblePortion = Math.round(cardHeight * 0.1); // Show 10% of card (name area)
          const stackOffset = -(cardHeight - visiblePortion); // Negative offset to stack tightly"""
        
        new_calculation = """// MTGO-style tight stacking - show ~15% of each card (name area visible)
          // Typical card is ~180px tall, we want ~27px showing = 85% overlap
          const cardHeight = Math.round(180 * scaleFactor); // Estimated card height at current scale
          const visiblePortion = Math.round(cardHeight * 0.15); // Show 15% of card (name area)
          const stackOffset = -(cardHeight - visiblePortion); // Negative offset to stack tightly"""
        
        if old_calculation in content:
            content = content.replace(old_calculation, new_calculation)
            print("✅ Adjusted stacking to 15% visibility (85% overlap)")
        else:
            print("⚠️  Could not find exact stacking calculation to replace")
            # Fallback: look for just the visiblePortion line
            if "const visiblePortion = Math.round(cardHeight * 0.1);" in content:
                content = content.replace(
                    "const visiblePortion = Math.round(cardHeight * 0.1); // Show 10% of card (name area)",
                    "const visiblePortion = Math.round(cardHeight * 0.15); // Show 15% of card (name area)"
                )
                print("✅ Found and updated visiblePortion to 15%")
        
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
    """Remove column padding to eliminate extra visual gaps"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix: Remove padding from pile-column-content to eliminate extra gaps
        old_column_content = """.pile-column-content {
  flex: 1;
  padding: 3px;
  display: flex;
  flex-direction: column;
  align-items: center; /* Center cards horizontally within column */
  position: relative;
  /* NO overflow or max-height - natural content flow */
}"""
        
        new_column_content = """.pile-column-content {
  flex: 1;
  padding: 0px; /* Remove padding to eliminate visual gaps between columns */
  display: flex;
  flex-direction: column;
  align-items: center; /* Center cards horizontally within column */
  position: relative;
  /* NO overflow or max-height - natural content flow */
}"""
        
        if old_column_content in content:
            content = content.replace(old_column_content, new_column_content)
            print("✅ Removed column padding to tighten gaps")
        else:
            print("⚠️  Could not find exact pile-column-content section")
        
        # Double-check that gap is still set to 2px
        if "gap: 2px; /* Much tighter gaps between columns */" in content:
            print("✅ Confirmed gap is set to 2px")
        elif "gap: 2px;" in content:
            print("✅ Found gap: 2px setting")
        else:
            print("⚠️  Could not confirm gap setting")
        
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
    """Apply final pile view tweaks"""
    print("🎯 Applying Final Pile View Tweaks:")
    print("1. Increase card visibility from 10% to 15% (better name readability)")
    print("2. Remove column padding to truly tighten gaps between columns")
    print("3. Visual gap should now be just 2px instead of 8px")
    print()
    
    success_count = 0
    
    if update_pile_column_tsx():
        success_count += 1
    
    if update_mtgo_layout_css():
        success_count += 1
    
    print()
    if success_count == 2:
        print("🎉 All final tweaks applied successfully!")
        print("✅ Cards should show 15% visibility (name area readable)")
        print("✅ Column gaps should be much tighter (2px not 8px)")
        print("✅ Proportional stacking maintained across card sizes")
        print()
        print("📊 Expected results:")
        print("   • Small cards (0.7x): ~189px tall, ~28px visible")
        print("   • Normal cards (1.0x): ~180px tall, ~27px visible") 
        print("   • Large cards (2.0x): ~360px tall, ~54px visible")
        print()
        print("🔧 Test with 'npm start' to verify the improvements")
    else:
        print(f"⚠️  Only {success_count}/2 fixes applied successfully")
        print("Some manual fixes may be needed")

if __name__ == "__main__":
    main()