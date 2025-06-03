#!/usr/bin/env python3
"""
Remove duplicate function declarations in MTGOLayout.tsx
Fix compilation error from duplicate getOriginalCardId
"""

import os
import re

def remove_duplicate_functions():
    filepath = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print("🔧 Removing duplicate function declarations...")
        
        # Find all occurrences of getOriginalCardId function
        pattern = r'// Helper to get original card ID for quantity tracking\s*const getOriginalCardId = \(card: ScryfallCard \| DeckCard \| DeckCardInstance\): string => \{\s*if \(\'cardId\' in card\) return card\.cardId;\s*return [^}]+\};'
        
        matches = list(re.finditer(pattern, content, re.DOTALL))
        print(f"Found {len(matches)} getOriginalCardId function declarations")
        
        if len(matches) > 1:
            # Keep only the first occurrence, remove all others
            # Remove from the end to avoid index shifting
            for match in reversed(matches[1:]):
                content = content[:match.start()] + content[match.end():]
                print(f"✅ Removed duplicate getOriginalCardId at position {match.start()}")
        
        # Also check for any standalone getOriginalCardId without the comment
        standalone_pattern = r'const getOriginalCardId = \(card: ScryfallCard \| DeckCard \| DeckCardInstance\): string => \{\s*if \(\'cardId\' in card\) return card\.cardId;\s*return [^}]+\};'
        
        standalone_matches = list(re.finditer(standalone_pattern, content, re.DOTALL))
        
        # If we found standalone ones and we already have one with comment, remove the standalone ones
        if len(standalone_matches) > 0 and len(matches) > 0:
            for match in reversed(standalone_matches):
                # Check if this match is already covered by the commented version
                is_part_of_commented = any(
                    commented_match.start() <= match.start() <= commented_match.end() 
                    for commented_match in matches
                )
                
                if not is_part_of_commented:
                    content = content[:match.start()] + content[match.end():]
                    print(f"✅ Removed standalone duplicate getOriginalCardId at position {match.start()}")
        
        # Clean up any empty lines left behind
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Write the cleaned content back
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("✅ File cleaned successfully")
        
        # Verify there's only one getOriginalCardId left
        with open(filepath, 'r', encoding='utf-8') as file:
            verification_content = file.read()
        
        final_count = len(re.findall(r'const getOriginalCardId', verification_content))
        print(f"✅ VERIFICATION: Found {final_count} getOriginalCardId declaration(s) remaining")
        
        if final_count == 1:
            print("✅ Perfect! Only one getOriginalCardId function remains")
            return True
        elif final_count == 0:
            print("⚠️ No getOriginalCardId function found - you might need to add it back")
            return True
        else:
            print("⚠️ Still multiple getOriginalCardId functions - manual cleanup needed")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_function_locations():
    """Show where getOriginalCardId functions are located"""
    filepath = "src/components/MTGOLayout.tsx"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        print("\n📍 Current getOriginalCardId function locations:")
        for i, line in enumerate(lines):
            if "const getOriginalCardId" in line:
                print(f"   Line {i+1}: {line.strip()}")
                # Show a few lines of context
                start = max(0, i-1)
                end = min(len(lines), i+4)
                for j in range(start, end):
                    marker = ">>> " if j == i else "    "
                    print(f"{marker}{j+1:4d}: {lines[j].rstrip()}")
                print()
                
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    print("🔧 Removing Duplicate Functions")
    print("=" * 35)
    
    # Show current state
    show_function_locations()
    
    success = remove_duplicate_functions()
    
    if success:
        print("\n✅ DUPLICATES REMOVED!")
        print("The duplicate function declarations have been cleaned up.")
        print("\nTry 'npm start' again - compilation should work now.")
    else:
        print("\n❌ MANUAL CLEANUP NEEDED")
        print("Please check the file manually for any remaining duplicates.")
