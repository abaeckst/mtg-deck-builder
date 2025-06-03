import os
import re

def update_pile_column_tsx():
    """Adjust stacking to show 14% of each card"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\PileColumn.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix: Change to 14% visibility
        patterns_to_find = [
            "const visiblePortion = Math.round(cardHeight * 0.15); // Show 15% of card (name area)",
            "const visiblePortion = Math.round(cardHeight * 0.1); // Show 10% of card (name area)"
        ]
        
        new_line = "const visiblePortion = Math.round(cardHeight * 0.14); // Show 14% of card (name area)"
        
        found = False
        for pattern in patterns_to_find:
            if pattern in content:
                content = content.replace(pattern, new_line)
                found = True
                print("✅ Adjusted stacking to 14% visibility")
                break
        
        if not found:
            print("⚠️  Could not find visiblePortion line to update")
        
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
    """Make visual gaps much tighter by reducing both gap and container padding"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix 1: Reduce gap from 2px to 0px for tightest possible spacing
        gap_patterns = [
            "gap: 2px; /* Much tighter gaps between columns */",
            "gap: 2px;"
        ]
        
        for pattern in gap_patterns:
            if pattern in content:
                content = content.replace(pattern, "gap: 0px; /* Tightest possible column gaps */")
                print("✅ Reduced gap to 0px for tightest spacing")
                break
        
        # Fix 2: Also reduce the container padding to make columns even closer
        old_container = """.pile-columns-container {
  flex: 1;
  display: flex;
  overflow-x: auto;
  overflow-y: auto;
  padding: 4px;
  gap: 0px; /* Tightest possible column gaps */
  align-items: flex-start;
  max-height: 100%;
}"""
        
        new_container = """.pile-columns-container {
  flex: 1;
  display: flex;
  overflow-x: auto;
  overflow-y: auto;
  padding: 2px; /* Reduced container padding for tighter layout */
  gap: 0px; /* Tightest possible column gaps */
  align-items: flex-start;
  max-height: 100%;
}"""
        
        if old_container in content:
            content = content.replace(old_container, new_container)
            print("✅ Reduced container padding for tighter layout")
        elif "padding: 4px;" in content and ".pile-columns-container" in content:
            content = content.replace("padding: 4px;", "padding: 1px; /* Minimal container padding */")
            print("✅ Found and reduced container padding")
        
        # Fix 3: Remove any margin from pile-column itself
        if ".pile-column {" in content:
            # Look for margin in pile-column and remove it
            lines = content.split('\n')
            in_pile_column = False
            for i, line in enumerate(lines):
                if '.pile-column {' in line:
                    in_pile_column = True
                elif in_pile_column and '}' in line and not line.strip().startswith('/*'):
                    in_pile_column = False
                elif in_pile_column and 'margin:' in line:
                    lines[i] = '  /* margin removed for tighter spacing */'
                    print("✅ Removed margin from pile-column")
            content = '\n'.join(lines)
        
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
    """Apply aggressive visual gap reduction and 14% visibility"""
    print("🎯 Applying Aggressive Visual Tightening:")
    print("1. Reduce card visibility to 14% (tighter stacking)")
    print("2. Set gap to 0px (no spacing between columns)")
    print("3. Reduce container padding (columns closer to edges)")
    print("4. Remove any column margins")
    print()
    
    success_count = 0
    
    if update_pile_column_tsx():
        success_count += 1
    
    if update_mtgo_layout_css():
        success_count += 1
    
    print()
    if success_count == 2:
        print("🎉 Maximum visual tightening applied!")
        print("✅ 14% card visibility (86% overlap)")
        print("✅ 0px gaps between columns")
        print("✅ Minimal container padding")
        print("✅ No column margins")
        print()
        print("📊 Expected card visibility:")
        print("   • Small cards (0.7x): ~126px tall, ~18px visible")
        print("   • Normal cards (1.0x): ~180px tall, ~25px visible") 
        print("   • Large cards (2.0x): ~360px tall, ~50px visible")
        print()
        print("🔧 Test with 'npm start' - columns should be touching or nearly touching")
    else:
        print(f"⚠️  Only {success_count}/2 fixes applied successfully")

if __name__ == "__main__":
    main()