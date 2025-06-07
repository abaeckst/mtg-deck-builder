#!/usr/bin/env python3

import os
import sys

def update_layout_css_import(filename):
    """Add FilterPanel.css import to MTGOLayout.tsx for Phase 4B"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements with exact string matching
    updates = [
        # Add FilterPanel.css import after existing CSS imports
        (
            """import './MTGOLayout.css';
import './ContextMenu.css';""",
            """import './MTGOLayout.css';
import './ContextMenu.css';
import './FilterPanel.css';""",
            "Add FilterPanel.css import"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_layout_css_import("src/components/MTGOLayout.tsx")
    sys.exit(0 if success else 1)
