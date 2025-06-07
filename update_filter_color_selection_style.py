#!/usr/bin/env python3

import os
import sys

def update_filter_color_selection_style(filename):
    """Update FilterPanel.css to replace blue glow with clean deck builder-style outline"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements with exact string matching
    updates = [
        # Replace complex blue glow selection with clean outline
        (
            """.color-button.selected {
  border-color: #3b82f6;
  box-shadow: 0 0 16px rgba(59, 130, 246, 1.0), 0 0 8px rgba(59, 130, 246, 0.8), inset 0 2px 4px rgba(0, 0, 0, 0.2);
}""",
            """.color-button.selected {
  border: 2px solid #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}""",
            "Updated color button selection to clean outline style"
        ),
        
        # Update gold button selection to match
        (
            """  box-shadow: 0 0 16px rgba(59, 130, 246, 1.0), 0 0 8px rgba(59, 130, 246, 0.8), 0 0 4px rgba(255, 215, 0, 0.6), inset 0 2px 4px rgba(0, 0, 0, 0.2);""",
            """  box-shadow: 0 0 0 1px #3b82f6;""",
            "Updated gold button selection to clean outline style"
        )
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"⚠️ Could not find exact match for: {desc}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_filter_color_selection_style("src/components/FilterPanel.css")
    sys.exit(0 if success else 1)