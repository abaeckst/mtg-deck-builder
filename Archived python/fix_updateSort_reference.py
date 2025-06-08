#!/usr/bin/env python3

import os
import sys

def fix_updateSort_reference(filename):
    """Fix the updateSort reference issue by moving test function after definition"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the incorrectly placed test function
    incorrect_test_function = '''// Global test function for direct debugging
const testUpdateSort = () => {
  console.log('🧪 MANUAL TEST: Calling updateSort directly');
  updateSort('collection', 'name', 'desc');
};

// Expose test function globally
(window as any).testUpdateSort = testUpdateSort;

// Global metadata exposure for direct architecture'''
    
    if incorrect_test_function in content:
        content = content.replace(incorrect_test_function, '// Global metadata exposure for direct architecture')
        print("✅ Removed incorrectly placed test function")
    else:
        print("❌ Could not find incorrectly placed test function")
        return False
    
    # Find the end of the updateSort function and add the test function there
    # Look for the end of the updateSort useCallback
    updateSort_end = '  }, [sortState]);'
    
    if updateSort_end in content:
        # Add the test function right after updateSort definition
        test_function_addition = '''  }, [sortState]);

  // Global test function for direct debugging (defined after updateSort)
  const testUpdateSort = useCallback(() => {
    console.log('🧪 MANUAL TEST: Calling updateSort directly');
    updateSort('collection', 'name', 'desc');
  }, [updateSort]);

  // Expose test function globally after definition
  useEffect(() => {
    (window as any).testUpdateSort = testUpdateSort;
    console.log('🧪 Global test function available: window.testUpdateSort()');
  }, [testUpdateSort]);'''
        
        content = content.replace(updateSort_end, test_function_addition)
        print("✅ Added test function after updateSort definition")
    else:
        print("❌ Could not find updateSort function end")
        return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed {filename}")
    return True

if __name__ == "__main__":
    success = fix_updateSort_reference("src/hooks/useSorting.ts")
    sys.exit(0 if success else 1)
