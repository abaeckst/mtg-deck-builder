#!/usr/bin/env python3

import os
import sys
import re

def fix_css_syntax_errors():
    """Fix CSS syntax errors in FilterPanel.css and clean up color button styling"""
    
    css_file = "src/components/FilterPanel.css"
    
    if not os.path.exists(css_file):
        print(f"❌ {css_file} not found")
        return False
    
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Fixing CSS syntax errors and cleaning up color button styling...")
    
    # Remove all broken Keyrune-related CSS sections
    sections_to_remove = [
        # Remove the broken section starting with "Hide text content"
        r'/\* Hide text content in color buttons, show only mana symbols \*/\s*\.color-button\s*\{[^}]*\}',
        
        # Remove ::before rules
        r'\.color-button::before\s*\{[^}]*\}',
        
        # Remove individual color ::before rules
        r'\.color-button\.color-[wubrgc]::before\s*\{[^}]*\}',
        
        # Remove any orphaned Keyrune font references
        r"font-family:\s*'Keyrune'[^;]*;",
        r'content:\s*"\\e[0-9]+";',
    ]
    
    for pattern in sections_to_remove:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Clean up any multiple newlines
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    
    # Find the color button section and replace it with clean styling
    color_button_start = content.find('/* Mana Symbol Buttons with Keyrune Font */')
    if color_button_start == -1:
        color_button_start = content.find('.color-button {')
    
    color_button_end = content.find('.color-button.disabled {')
    if color_button_end == -1:
        color_button_end = content.find('/* Enhanced Filter Panel Layout */')
    
    if color_button_start != -1 and color_button_end != -1:
        # Replace the entire color button section with clean CSS
        clean_color_button_css = '''/* Clean Color Button Styling - Letters in Circles */
.color-button {
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 14px;
  font-weight: bold;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  text-shadow: none;
}

.color-button:hover:not(.disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.color-button.selected {
  border-color: #3b82f6;
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.8), inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Individual Color Styling */
.color-button.color-w {
  background: linear-gradient(135deg, #FFFBD5 0%, #F0F0F0 100%);
  color: #333333;
  border-color: #E0E0E0;
}

.color-button.color-u {
  background: linear-gradient(135deg, #0E68AB 0%, #1E88E5 100%);
  color: #ffffff;
  border-color: #1976D2;
}

.color-button.color-b {
  background: linear-gradient(135deg, #150B00 0%, #2D1B00 100%);
  color: #ffffff;
  border-color: #4A3000;
}

.color-button.color-r {
  background: linear-gradient(135deg, #D32F2F 0%, #F44336 100%);
  color: #ffffff;
  border-color: #C62828;
}

.color-button.color-g {
  background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
  color: #ffffff;
  border-color: #1B5E20;
}

.color-button.color-c {
  background: linear-gradient(135deg, #9E9E9E 0%, #BDBDBD 100%);
  color: #333333;
  border-color: #757575;
}

'''
        
        content = content[:color_button_start] + clean_color_button_css + content[color_button_end:]
        print("✅ Replaced color button section with clean CSS")
    
    # Remove any remaining Keyrune font declaration
    keyrune_font_pattern = r'@font-face\s*\{[^}]*font-family:\s*[\'"]Keyrune[\'"][^}]*\}'
    content = re.sub(keyrune_font_pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Clean up any extra whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    
    # Write the cleaned content back
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed CSS syntax errors and cleaned up color button styling")
    print("✅ Removed broken Keyrune font references")
    print("✅ Color buttons now use clean letters in colored circles")
    
    return True

if __name__ == "__main__":
    success = fix_css_syntax_errors()
    if success:
        print("\n🎮 CSS fixed! Run 'npm start' to see clean color buttons with letters!")
    else:
        print("\n❌ CSS fix failed")
    sys.exit(0 if success else 1)