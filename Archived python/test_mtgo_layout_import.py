#!/usr/bin/env python3

import os
import sys

def test_mtgo_layout_import(filename):
    """Add diagnostics to MTGOLayout.tsx to verify useSorting import"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the useSorting hook usage and add diagnostics
    old_hook_usage = '''  // Enhanced sorting system - replaces local sort state
  const { updateSort, getSortState } = useSorting();'''

    new_hook_usage = '''  // Enhanced sorting system - replaces local sort state
  console.log('🟡 MTGO LAYOUT: About to call useSorting hook');
  const sortingHookResult = useSorting();
  console.log('🟡 MTGO LAYOUT: useSorting hook result:', sortingHookResult);
  const { updateSort, getSortState } = sortingHookResult;
  console.log('🟡 MTGO LAYOUT: Extracted functions:', {
    updateSort: typeof updateSort,
    getSortState: typeof getSortState
  });'''

    if old_hook_usage in content:
        content = content.replace(old_hook_usage, new_hook_usage)
        print("✅ Added MTGOLayout hook usage diagnostics")
    else:
        print("❌ Could not find useSorting hook usage in MTGOLayout")
        return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully added diagnostics to {filename}")
    return True

if __name__ == "__main__":
    success = test_mtgo_layout_import("src/components/MTGOLayout.tsx")
    sys.exit(0 if success else 1)
