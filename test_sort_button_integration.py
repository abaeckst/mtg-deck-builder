#!/usr/bin/env python3

import os
import sys

def test_sort_button_integration(filename):
    """Add debugging to useSorting.ts to verify updateSort is being called"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the updateSort function and add debugging at the very beginning
    old_function_start = '''  // Enhanced update sort with DIRECT ARCHITECTURE for smart sorting
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    const newSortState = {
      criteria,
      direction: direction ?? sortState[area].direction,
    };

    console.log('🎯 SORT UPDATE CALLED - DIRECT ARCHITECTURE:', {'''

    new_function_start = '''  // Enhanced update sort with DIRECT ARCHITECTURE for smart sorting
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    console.log('🚨 ===== UPDATE SORT FUNCTION CALLED =====');
    console.log('🚨 PARAMETERS:', { area, criteria, direction });
    console.log('🚨 Current sortState:', sortState);
    
    const newSortState = {
      criteria,
      direction: direction ?? sortState[area].direction,
    };

    console.log('🎯 SORT UPDATE CALLED - DIRECT ARCHITECTURE:', {'''

    if old_function_start in content:
        content = content.replace(old_function_start, new_function_start)
        print("✅ Added entry-level debugging to updateSort function")
    else:
        print("❌ Could not find updateSort function start to add debugging")
        return False

    # Also add global test function exposure
    add_global_test = '''// Global test function for direct debugging
const testUpdateSort = () => {
  console.log('🧪 MANUAL TEST: Calling updateSort directly');
  updateSort('collection', 'name', 'desc');
};

// Expose test function globally
(window as any).testUpdateSort = testUpdateSort;

// Global metadata exposure for direct architecture'''

    if '// Global metadata exposure for direct architecture' in content:
        content = content.replace('// Global metadata exposure for direct architecture', add_global_test)
        print("✅ Added global test function for manual debugging")
    else:
        print("❌ Could not find insertion point for global test function")
        return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully added debugging to {filename}")
    return True

if __name__ == "__main__":
    success = test_sort_button_integration("src/hooks/useSorting.ts")
    sys.exit(0 if success else 1)
