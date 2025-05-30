import os
import re

def update_mtgo_layout_css():
    """Add small breathing room between columns"""
    file_path = r"C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Fix: Increase gap from 3px to 6px for better breathing room
        gap_patterns = [
            "gap: 3px; /* Small but visible gap between columns */",
            "gap: 3px;"
        ]
        
        new_gap = "gap: 6px; /* Small breathing room between columns */"
        
        found = False
        for pattern in gap_patterns:
            if pattern in content:
                content = content.replace(pattern, new_gap)
                found = True
                print("✅ Increased gap to 6px for better breathing room")
                break
        
        if not found:
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
    """Add breathing room between pile columns"""
    print("🌬️  ADDING BREATHING ROOM:")
    print("💡 Current: 3px gap - too tight, cards touching")
    print("💡 Solution: 6px gap - small but visible separation")
    print()
    print("📊 Expected Result:")
    print("   • Small visible gap between each column")
    print("   • Cards have breathing room but still look tight")
    print("   • Professional MTGO-style spacing")
    print()
    
    if update_mtgo_layout_css():
        print()
        print("🎉 BREATHING ROOM ADDED!")
        print("✅ Gap increased from 3px to 6px")
        print("✅ Cards should now have proper visual separation")
        print()
        print("🔧 Test with 'npm start' to see the improved spacing")
    else:
        print("❌ Failed to add breathing room")

if __name__ == "__main__":
    main()