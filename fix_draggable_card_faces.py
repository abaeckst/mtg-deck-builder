#!/usr/bin/env python3
"""
Fix DraggableCard.tsx to properly pass through card_faces data for deck/sideboard cards
"""

import os
import shutil

def fix_draggable_card_faces():
    file_path = "src/components/DraggableCard.tsx"
    backup_path = f"{file_path}.backup"
    
    # Create backup
    if os.path.exists(file_path):
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
    
    # Read current content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the cardForMagicCard memo and replace it
    old_memo_part = """        keywords: [],
        layout: 'normal',
        card_faces: undefined,"""

    new_memo_part = """        keywords: [],
        layout: 'normal',
        // FIXED: Preserve card_faces for double-faced card support
        card_faces: card.card_faces,"""

    # Replace the specific part
    if old_memo_part in content:
        content = content.replace(old_memo_part, new_memo_part)
        print("✅ Updated cardForMagicCard memo to preserve card_faces from DeckCardInstance")
    else:
        print("⚠️  Could not find exact memo section - trying alternative approach")
        
        # Try to find the broader section
        if "card_faces: undefined," in content:
            content = content.replace("card_faces: undefined,", "card_faces: card.card_faces,")
            print("✅ Updated card_faces assignment in cardForMagicCard memo")
        else:
            print("❌ Could not find card_faces assignment in DraggableCard")
            return

    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {file_path}")
    print("")
    print("📝 Changes made:")
    print("   - Modified cardForMagicCard memo to preserve card_faces from DeckCardInstance")
    print("   - This ensures double-faced cards show flip buttons in deck/sideboard areas")
    print("")
    print("🧪 Complete fix ready for testing:")
    print("   1. Run: python fix_card_faces_preservation.py")
    print("   2. Run: python fix_draggable_card_faces.py")  
    print("   3. Restart app: npm start")
    print("   4. Test flip buttons on double-faced cards in ALL areas")

if __name__ == "__main__":
    fix_draggable_card_faces()
