import re

def update_deckarea_segment2():
    """
    Update DeckArea.tsx for Segment 2: Replace view buttons with ViewModeDropdown
    Uses multiple fallback approaches to find and replace the buttons
    """
    
    file_path = "src/components/DeckArea.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"📁 Reading {file_path}...")
        original_content = content
        
        # 1. Add ViewModeDropdown import after existing imports
        if "ViewModeDropdown" not in content:
            # Find the line with PileView import and add after it
            pileview_import_pattern = r"(import PileView from './PileView';)"
            if re.search(pileview_import_pattern, content):
                content = re.sub(
                    pileview_import_pattern, 
                    r"\1\nimport ViewModeDropdown from './ViewModeDropdown';", 
                    content
                )
                print("✅ Added ViewModeDropdown import")
            else:
                print("⚠️ Could not find PileView import, adding import at end of imports")
                # Find any import and add after the last one
                import_pattern = r"(import [^;]+;)(?=\n\n)"
                if re.search(import_pattern, content):
                    content = re.sub(
                        import_pattern,
                        r"\1\nimport ViewModeDropdown from './ViewModeDropdown';",
                        content
                    )
                    print("✅ Added ViewModeDropdown import after last import")
        
        # 2. Find and replace the view buttons using multiple approaches
        replaced = False
        
        # Approach 1: Look for the specific structure around the buttons
        # Find the section that has "View:" label followed by the buttons
        pattern1 = r'(<span style=\{\{ color: \'#cccccc\' \}\}>View:</span>\s*<div style=\{\{ display: \'flex\', gap: \'4px\' \}\}>)([\s\S]*?)(</div>)(\s*<div className="sort-button-container")'
        
        if re.search(pattern1, content, re.DOTALL):
            def replace_buttons(match):
                return f"{match.group(1)}\n            <ViewModeDropdown\n              currentView={{viewMode}}\n              onViewChange={{(mode) => {{ clearSelection(); onViewModeChange(mode); }}}}\n            />\n          {match.group(3)}{match.group(4)}"
            
            content = re.sub(pattern1, replace_buttons, content, flags=re.DOTALL)
            replaced = True
            print("✅ Replaced view buttons using pattern 1 (with View: label)")
        
        # Approach 2: If that didn't work, look for just the button container
        if not replaced:
            pattern2 = r'(<div style=\{\{ display: \'flex\', gap: \'4px\' \}\}>)[\s\S]*?(Card)[\s\S]*?(Pile)[\s\S]*?(List)[\s\S]*?(</div>)(\s*<div className="sort-button-container")'
            
            if re.search(pattern2, content, re.DOTALL):
                replacement2 = r'<ViewModeDropdown\n              currentView={viewMode}\n              onViewChange={(mode) => { clearSelection(); onViewModeChange(mode); }}\n            />\6'
                content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)
                replaced = True
                print("✅ Replaced view buttons using pattern 2 (button container)")
        
        # Approach 3: Line-by-line approach if regex fails
        if not replaced:
            lines = content.split('\n')
            start_idx = -1
            end_idx = -1
            button_count = 0
            
            for i, line in enumerate(lines):
                # Look for the div with flex styling
                if "display: 'flex', gap: '4px'" in line and "View:" not in lines[max(0, i-2):i]:
                    start_idx = i
                    button_count = 0
                elif start_idx != -1:
                    # Count buttons and look for Card, Pile, List
                    if ">Card</button>" in line:
                        button_count += 1
                    elif ">Pile</button>" in line:
                        button_count += 1
                    elif ">List</button>" in line:
                        button_count += 1
                        # After finding List button, look for closing div
                        for j in range(i+1, min(i+5, len(lines))):
                            if "</div>" in lines[j] and "sort-button-container" not in lines[j+1:j+3]:
                                end_idx = j
                                break
                        break
            
            if start_idx != -1 and end_idx != -1 and button_count == 3:
                # Get the indentation from the original div
                original_line = lines[start_idx]
                indent = original_line[:len(original_line) - len(original_line.lstrip())]
                
                # Create replacement
                replacement_lines = [
                    f"{indent}<ViewModeDropdown",
                    f"{indent}  currentView={{viewMode}}",
                    f"{indent}  onViewChange={{(mode) => {{ clearSelection(); onViewModeChange(mode); }}}}",
                    f"{indent}/>"
                ]
                
                new_lines = lines[:start_idx] + replacement_lines + lines[end_idx+1:]
                content = '\n'.join(new_lines)
                replaced = True
                print("✅ Replaced view buttons using line-by-line approach")
                print(f"   Found buttons from line {start_idx+1} to {end_idx+1}")
            else:
                print(f"❌ Line-by-line approach failed: start={start_idx}, end={end_idx}, buttons={button_count}")
        
        if not replaced:
            print("❌ Could not find and replace view buttons")
            print("ℹ️  Manual replacement needed in DeckArea.tsx:")
            print("    Find the three buttons (Card, Pile, List) and replace with ViewModeDropdown")
            return False
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"\n🎉 Successfully updated {file_path}")
        print("📋 Changes applied:")
        print("   • Added ViewModeDropdown import")
        print("   • Replaced Card/Pile/List buttons with dropdown")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        return False
    except Exception as e:
        print(f"❌ Error updating file: {e}")
        print("   Try running the script again or check file permissions")
        return False

if __name__ == "__main__":
    success = update_deckarea_segment2()
    if success:
        print("\n✅ Script completed successfully!")
    else:
        print("\n❌ Script failed - manual intervention may be needed")