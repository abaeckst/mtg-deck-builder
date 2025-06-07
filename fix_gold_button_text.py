#!/usr/bin/env python3

import os
import sys

def fix_gold_button_text():
    """Remove GOLD text from GoldButton component"""
    
    gold_file = "src/components/GoldButton.tsx"
    if not os.path.exists(gold_file):
        print(f"❌ {gold_file} not found")
        return False
    
    with open(gold_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the GOLD text from the button
    old_button_content = '''    >
      GOLD
    </button>'''
    
    new_button_content = '''    >
    </button>'''
    
    if old_button_content in content:
        content = content.replace(old_button_content, new_button_content)
        print("✅ Removed GOLD text from gold button")
        
        with open(gold_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    else:
        print("❌ Could not find GOLD text pattern to remove")
        return False

if __name__ == "__main__":
    success = fix_gold_button_text()
    sys.exit(0 if success else 1)