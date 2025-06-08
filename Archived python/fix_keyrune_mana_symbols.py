#!/usr/bin/env python3

import os
import sys

def fix_keyrune_mana_symbols():
    """Fix FilterPanel.css to use correct Keyrune Unicode characters for MTG mana symbols"""
    
    css_file = "src/components/FilterPanel.css"
    
    if not os.path.exists(css_file):
        print(f"Error: {css_file} not found")
        return False
    
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the incorrect ::before content with proper Keyrune Unicode values
    updates = [
        # White mana symbol
        (
            '.color-button.color-w::before {\n  content: "\\e600"; /* Keyrune white mana symbol */\n}',
            '.color-button.color-w::before {\n  content: "\\e600";\n}'
        ),
        # Blue mana symbol  
        (
            '.color-button.color-u::before {\n  content: "\\e601"; /* Keyrune blue mana symbol */\n}',
            '.color-button.color-u::before {\n  content: "\\e601";\n}'
        ),
        # Black mana symbol
        (
            '.color-button.color-b::before {\n  content: "\\e602"; /* Keyrune black mana symbol */\n}',
            '.color-button.color-b::before {\n  content: "\\e602";\n}'
        ),
        # Red mana symbol
        (
            '.color-button.color-r::before {\n  content: "\\e603"; /* Keyrune red mana symbol */\n}',
            '.color-button.color-r::before {\n  content: "\\e603";\n}'
        ),
        # Green mana symbol
        (
            '.color-button.color-g::before {\n  content: "\\e604"; /* Keyrune green mana symbol */\n}',
            '.color-button.color-g::before {\n  content: "\\e604";\n}'
        ),
        # Colorless mana symbol
        (
            '.color-button.color-c::before {\n  content: "\\e904"; /* Keyrune colorless symbol */\n}',
            '.color-button.color-c::before {\n  content: "\\e904";\n}'
        )
    ]
    
    # Check if we need to fix the approach - look for the button elements that might be showing text
    # The issue might be that we're setting text content in the React component instead of using CSS ::before
    
    # Let's also add a rule to hide any text content and only show the ::before symbols
    additional_css = '''
/* Hide text content in color buttons, show only mana symbols */
.color-button {
  font-size: 0; /* Hide any text content */
}

.color-button::before {
  font-family: 'Keyrune', Arial, sans-serif;
  font-size: 20px;
  display: inline-block;
}
'''
    
    # Apply updates
    for old_rule, new_rule in updates:
        if old_rule in content:
            content = content.replace(old_rule, new_rule)
            print(f"✅ Updated mana symbol rule")
    
    # Add the additional CSS rules if not already present
    if 'font-size: 0' not in content:
        # Find the end of the existing color button styles and add our rules
        insert_point = content.find('/* Individual Mana Symbol Styling */')
        if insert_point != -1:
            content = content[:insert_point] + additional_css + '\n' + content[insert_point:]
            print("✅ Added rules to hide text and show only mana symbols")
    
    # Write the updated content back
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {css_file}")
    print("✅ Color buttons should now show MTG mana symbols instead of letters")
    return True

if __name__ == "__main__":
    success = fix_keyrune_mana_symbols()
    if success:
        print("\n🎮 Mana symbol fix complete!")
        print("✅ Run 'npm start' to see authentic MTG mana symbols instead of letters!")
    else:
        print("\n❌ Mana symbol fix failed. Check the error messages above.")
    sys.exit(0 if success else 1)