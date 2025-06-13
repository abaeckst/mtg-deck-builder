#!/usr/bin/env python3
"""
Fix flip button positioning issue caused by CSS Grid interference
Root cause: CSS Grid layout affecting absolute positioning coordinates
Solution: Add CSS isolation to prevent grid context interference
"""

import os

def fix_flip_button_positioning():
    filepath = "src/components/FlipCard.tsx"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    # Create backup
    backup_path = f"{filepath}.backup_grid_fix"
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    
    print(f"✅ Backup created: {backup_path}")
    
    # Apply the fix by adding CSS isolation to the flip-card container
    updated_content = original_content.replace(
        """  // CORRECT: flip-card container (position: relative) - Clean 2D positioning context
  const containerStyles: React.CSSProperties = {
    ...style,
    position: 'relative', // CRITICAL: This provides the positioning context for the button
  };""",
        """  // CORRECT: flip-card container (position: relative) - Clean 2D positioning context
  const containerStyles: React.CSSProperties = {
    ...style,
    position: 'relative', // CRITICAL: This provides the positioning context for the button
    // CSS GRID ISOLATION FIX: Prevent grid layout from affecting button positioning
    isolation: 'isolate',
    contain: 'layout',
  };"""
    )
    
    # Verify the replacement worked
    if updated_content == original_content:
        print("❌ No changes made - string replacement failed")
        return False
    
    # Write the updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ FlipCard.tsx updated successfully")
    print("\n🔧 Changes applied:")
    print("- Added 'isolation: isolate' to flip-card container")
    print("- Added 'contain: layout' to prevent grid interference")
    print("\n📍 Effect:")
    print("- Flip button should now appear in correct position (bottom-right of card)")
    print("- CSS Grid layout will no longer affect button coordinates")
    print("- All existing functionality preserved")
    
    return True

if __name__ == "__main__":
    print("🚀 Fixing flip button positioning issue...")
    success = fix_flip_button_positioning()
    
    if success:
        print("\n✅ Fix applied successfully!")
        print("\n🧪 Test the fix:")
        print("1. Find a double-faced card in your app")
        print("2. Check if flip button (↻) appears in bottom-right corner of card")
        print("3. Verify button is clickable and 3D flip animation works")
        print("4. Test in collection, deck, and sideboard areas")
    else:
        print("\n❌ Fix failed - please check the file manually")
