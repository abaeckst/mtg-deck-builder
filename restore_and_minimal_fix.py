#!/usr/bin/env python3
"""
Restore MTGOLayout.tsx and apply only the minimal fix for React Hook rules
Just move the Smart Card Append useEffect to the proper location
"""

import subprocess

def restore_and_fix():
    """Restore original file and make minimal hook fix"""
    print("🔄 Restoring MTGOLayout.tsx from git...")
    
    # Restore the original file
    try:
        result = subprocess.run(['git', 'checkout', 'HEAD', '--', 'src/components/MTGOLayout.tsx'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Git restore failed: {result.stderr}")
            return False
        print("✅ Successfully restored MTGOLayout.tsx")
    except Exception as e:
        print(f"❌ Error running git: {e}")
        return False
    
    # Read the restored file
    try:
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ MTGOLayout.tsx not found after restore")
        return False
    
    lines = content.split('\n')
    
    # Find the problematic useEffect and move it to proper location
    # Look for the Smart Card Append useEffect around line 574
    useeffect_line = -1
    useeffect_content = []
    
    for i, line in enumerate(lines):
        if 'Sync loaded cards count for smart append' in line:
            # Found the comment, the useEffect should be next
            if i + 1 < len(lines) and 'useEffect(' in lines[i + 1]:
                useeffect_line = i
                # Capture the comment and useEffect
                useeffect_content = [
                    lines[i],     # Comment line
                    lines[i + 1], # useEffect(() => {
                    lines[i + 2], # if (cards.length > 0) {
                    lines[i + 3], # setLoadedCardsCount(cards.length);
                    lines[i + 4], # }
                    lines[i + 5], # }, [cards.length]);
                    lines[i + 6]  # Empty line
                ]
                break
    
    if useeffect_line == -1:
        print("⚠️ Smart Card Append useEffect not found - may already be fixed")
        return True
    
    print(f"📍 Found problematic useEffect at line {useeffect_line + 1}")
    
    # Remove the useEffect from its current location
    new_lines = lines[:useeffect_line] + lines[useeffect_line + 7:]
    
    # Find the proper insertion point - after existing useEffects but before component logic
    insertion_point = -1
    for i, line in enumerate(new_lines):
        if 'useEffect(() => {' in line and 'Click-outside effect for sort menus' in new_lines[i-1]:
            # Found the click-outside useEffect, insert after it
            # Find the end of this useEffect
            j = i + 1
            brace_count = 1
            while j < len(new_lines) and brace_count > 0:
                brace_count += new_lines[j].count('{') - new_lines[j].count('}')
                j += 1
            # Skip the dependencies array and closing
            while j < len(new_lines) and not new_lines[j].strip().endswith(');'):
                j += 1
            j += 1  # Skip the closing line
            # Skip any empty lines
            while j < len(new_lines) and new_lines[j].strip() == '':
                j += 1
            insertion_point = j
            break
    
    if insertion_point == -1:
        print("❌ Could not find proper insertion point")
        return False
    
    print(f"📍 Inserting useEffect at line {insertion_point + 1}")
    
    # Insert the useEffect at the proper location
    new_lines = new_lines[:insertion_point] + useeffect_content + new_lines[insertion_point:]
    
    # Write the fixed content
    try:
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print("✅ Successfully applied minimal React Hook rules fix")
        print("🎯 Smart Card Append useEffect moved to proper location")
        print("📝 All other functionality should remain intact")
        return True
        
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

if __name__ == "__main__":
    restore_and_fix()
