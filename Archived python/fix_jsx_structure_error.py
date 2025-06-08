#!/usr/bin/env python3

import os
import sys

def fix_jsx_structure_error():
    """Fix JSX structure error in FilterPanel.tsx"""
    
    filename = "src/components/FilterPanel.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Print some context around the error to understand the structure
    lines = content.split('\n')
    error_line = 295
    print("Context around error line:")
    for i in range(max(0, error_line-10), min(len(lines), error_line+5)):
        prefix = ">>> " if i == error_line-1 else "    "
        print(f"{prefix}{i+1:3d}: {lines[i]}")
    
    # Fix the JSX structure by finding the problematic area and correcting it
    updates = [
        # Fix missing div tag for card types section
        (
            '            ))}',
            '            ))}\n          </div>',
            "Add missing div closing tag"
        ),
        
        # Make sure More Types section is properly structured
        (
            '        {/* More Types (Subtypes) Group - Always Visible */}\n        <div className="filter-group">',
            '        {/* More Types (Subtypes) Group - Collapsible */}\n        <CollapsibleSection\n          title="MORE TYPES"\n          isExpanded={getSectionState(\'subtypes\')}\n          hasActiveFilters={activeFilters.subtypes.length > 0}\n          onToggle={() => updateSectionState(\'subtypes\', !getSectionState(\'subtypes\'))}\n        >\n          <div className="filter-group">',
            "Fix More Types section structure"
        ),
        
        # Close More Types section properly
        (
            '          />\n        </div>',
            '          />\n          </div>\n        </CollapsibleSection>',
            "Close More Types section properly"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
    
    # Write the corrected content back
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_jsx_structure_error()
    sys.exit(0 if success else 1)