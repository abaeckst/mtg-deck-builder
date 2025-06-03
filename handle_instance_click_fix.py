#!/usr/bin/env python3
"""
Add handleInstanceClick function to MTGOLayout.tsx
Targeted fix for missing function error
"""

import os
import re

def add_handle_instance_click():
    filepath = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"📄 Reading {filepath}")
        
        # Check if handleInstanceClick already exists
        if "handleInstanceClick" in content and "const handleInstanceClick" in content:
            print("✅ handleInstanceClick function already exists!")
            return True
        
        # Find the handleCardClick function and add handleInstanceClick after it
        print("🔧 Adding handleInstanceClick function...")
        
        # Look for the end of handleCardClick function
        pattern = r"(const handleCardClick = useCallback\([^}]+\}, \[[^\]]*\]\);)"
        
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # Add the handleInstanceClick function right after handleCardClick
            handle_instance_click_function = """

  // Instance-based click handler for deck/sideboard cards
  const handleInstanceClick = useCallback((instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
    if (contextMenuState.visible) {
      hideContextMenu();
    }
    // Use instance-based selection for deck/sideboard cards
    console.log(`Instance click: ${instanceId} for card ${instance.name}`);
    selectCard(instanceId, instance as any, event.ctrlKey);
  }, [contextMenuState.visible, hideContextMenu, selectCard]);"""
            
            # Insert after the handleCardClick function
            insert_point = match.end()
            content = content[:insert_point] + handle_instance_click_function + content[insert_point:]
            
            print("✅ Added handleInstanceClick function after handleCardClick")
            
        else:
            # Fallback: look for handleRightClick and add before it
            right_click_pattern = r"(  const handleRightClick = useCallback)"
            
            match = re.search(right_click_pattern, content)
            
            if match:
                handle_instance_click_function = """  // Instance-based click handler for deck/sideboard cards
  const handleInstanceClick = useCallback((instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
    if (contextMenuState.visible) {
      hideContextMenu();
    }
    // Use instance-based selection for deck/sideboard cards
    console.log(`Instance click: ${instanceId} for card ${instance.name}`);
    selectCard(instanceId, instance as any, event.ctrlKey);
  }, [contextMenuState.visible, hideContextMenu, selectCard]);

  """
                
                insert_point = match.start()
                content = content[:insert_point] + handle_instance_click_function + content[insert_point:]
                
                print("✅ Added handleInstanceClick function before handleRightClick")
            else:
                print("❌ Could not find suitable insertion point for handleInstanceClick")
                return False
        
        # Write the fixed content back to file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ Successfully added handleInstanceClick to {filepath}")
        
        # Verify the function was added
        with open(filepath, 'r', encoding='utf-8') as file:
            verification_content = file.read()
        
        if "const handleInstanceClick" in verification_content:
            print("✅ VERIFICATION: handleInstanceClick function is now present in the file")
            return True
        else:
            print("❌ VERIFICATION FAILED: handleInstanceClick function not found after insertion")
            return False
            
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def show_context_around_function():
    """Show some context around where the function should be"""
    filepath = "src/components/MTGOLayout.tsx"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Look for handleCardClick or handleRightClick for context
        for i, line in enumerate(lines):
            if "const handleCardClick" in line or "const handleRightClick" in line:
                print(f"\n📍 Context around line {i+1}:")
                start = max(0, i-2)
                end = min(len(lines), i+5)
                for j in range(start, end):
                    marker = ">>> " if j == i else "    "
                    print(f"{marker}{j+1:4d}: {lines[j].rstrip()}")
                break
                
    except Exception as e:
        print(f"Error reading file for context: {e}")

if __name__ == "__main__":
    print("🔧 Adding handleInstanceClick Function")
    print("=" * 40)
    
    # Show some context first
    show_context_around_function()
    
    success = add_handle_instance_click()
    
    if success:
        print("\n✅ FUNCTION SUCCESSFULLY ADDED")
        print("The handleInstanceClick function has been added to your MTGOLayout.tsx file!")
        print("\nTry running 'npm start' now.")
    else:
        print("\n❌ FAILED TO ADD FUNCTION")
        print("Let me know if you need to see the current file content for manual insertion.")
