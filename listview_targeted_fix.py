#!/usr/bin/env python3
"""
Targeted fix for the missing ListView deck sort props
"""

import os
import sys

def fix_missing_listview_update():
    """Fix the specific ListView update that failed"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    print("🔍 Searching for deck ListView sort props...")
    
    # Find all ListView components and their context
    listview_sections = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if 'ListView' in line and 'sortCriteria=' in line:
            # Get context around this ListView
            start = max(0, i - 5)
            end = min(len(lines), i + 15)
            section = '\n'.join(lines[start:end])
            listview_sections.append({
                'line_num': i,
                'section': section,
                'context': 'deck' if 'deck' in section.lower() else 'sideboard' if 'sideboard' in section.lower() else 'collection'
            })
    
    print(f"Found {len(listview_sections)} ListView sections:")
    for i, section in enumerate(listview_sections):
        print(f"\n📍 Section {i+1} (around line {section['line_num']}, context: {section['context']}):")
        print("=" * 50)
        print(section['section'])
        print("=" * 50)
    
    # Now let's try to find and fix the deck ListView specifically
    deck_patterns_to_try = [
        # Pattern 1: Standard deck ListView
        (
            """                  sortCriteria={deckSortCriteria}
                  sortDirection={deckSortDirection}
                  onSortChange={(criteria, direction) => {
                    setDeckSortCriteria(criteria);
                    setDeckSortDirection(direction);
                  }}""",
            """                  sortCriteria={deckSort.criteria}
                  sortDirection={deckSort.direction}
                  onSortChange={(criteria, direction) => {
                    updateSort('deck', criteria, direction);
                  }}"""
        ),
        # Pattern 2: Slightly different spacing
        (
            """                sortCriteria={deckSortCriteria}
                sortDirection={deckSortDirection}
                onSortChange={(criteria, direction) => {
                  setDeckSortCriteria(criteria);
                  setDeckSortDirection(direction);
                }}""",
            """                sortCriteria={deckSort.criteria}
                sortDirection={deckSort.direction}
                onSortChange={(criteria, direction) => {
                  updateSort('deck', criteria, direction);
                }}"""
        ),
        # Pattern 3: Single line version
        (
            "sortCriteria={deckSortCriteria}",
            "sortCriteria={deckSort.criteria}"
        ),
        (
            "sortDirection={deckSortDirection}",
            "sortDirection={deckSort.direction}"
        ),
        (
            "setDeckSortCriteria(criteria);",
            "updateSort('deck', criteria, direction);"
        ),
        (
            "setDeckSortDirection(direction);",
            "// direction handled by updateSort above"
        )
    ]
    
    success_count = 0
    original_content = content
    
    for i, (old_str, new_str) in enumerate(deck_patterns_to_try, 1):
        if old_str in content:
            content = content.replace(old_str, new_str)
            success_count += 1
            print(f"✅ Pattern {i}: Successfully updated")
        else:
            print(f"❌ Pattern {i}: Could not find - {old_str[:50]}...")
    
    if success_count == 0:
        print("❌ No patterns found. Let's search for any remaining deck sort references...")
        
        # Search for any remaining deck sort variable references
        remaining_refs = []
        if 'deckSortCriteria' in content:
            remaining_refs.append('deckSortCriteria')
        if 'deckSortDirection' in content:
            remaining_refs.append('deckSortDirection')
        if 'setDeckSortCriteria' in content:
            remaining_refs.append('setDeckSortCriteria')
        if 'setDeckSortDirection' in content:
            remaining_refs.append('setDeckSortDirection')
        
        if remaining_refs:
            print("🔍 Found remaining references:", remaining_refs)
            # Show context for each reference
            for ref in remaining_refs:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if ref in line:
                        start = max(0, i - 2)
                        end = min(len(lines), i + 3)
                        print(f"\n📍 {ref} found at line {i+1}:")
                        for j in range(start, end):
                            marker = ">>> " if j == i else "    "
                            print(f"{marker}{j+1:4d}: {lines[j]}")
        else:
            print("✅ No remaining deck sort references found!")
        
        return False
    
    # Write the updated content
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully applied {success_count} deck ListView fixes")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def main():
    print("🔧 ListView Fix - Completing Phase 4A Session 2 Integration")
    print("=" * 60)
    
    success = fix_missing_listview_update()
    
    if success:
        print("\n🎉 ListView fix complete!")
        print("✅ All integration updates should now be applied")
        print("\n🔬 Now test the application:")
        print("1. npm start")
        print("2. Test collection sorting with large/small searches")
        print("3. Test deck/sideboard sorting in list view")
    else:
        print("\n🔍 Manual fix needed:")
        print("1. Look for remaining deckSortCriteria/deckSortDirection references")
        print("2. Replace with deckSort.criteria/deckSort.direction")
        print("3. Replace setDeckSortCriteria/Direction with updateSort('deck', criteria, direction)")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)