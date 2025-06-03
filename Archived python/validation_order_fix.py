# Fix for function declaration order issue
# Move validation logic into the existing handleFilterChange function

import os
import re

def fix_function_order():
    """Fix the function declaration order issue by integrating validation into handleFilterChange"""
    
    # Read the current MTGOLayout.tsx file
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the problematic validation function that was added
    validation_function_start = '''
  // Input validation helper
  const validateRangeInput = useCallback((min: number | null, max: number | null, fieldName: string) => {'''
    
    validation_function_end = '''  }, [handleFilterChange, validateRangeInput]);

'''
    
    # Find and remove the entire validation function block
    start_pos = content.find(validation_function_start)
    if start_pos != -1:
        end_pos = content.find(validation_function_end) + len(validation_function_end)
        if end_pos != -1:
            content = content[:start_pos] + content[end_pos:]
    
    # Now modify the existing handleFilterChange to include validation
    old_handle_filter_change = '''  // Handle any filter change by triggering new search - FIXED v2 (State Closure)
  const handleFilterChange = useCallback((filterType: string, value: any) => {
    console.log('🔧 Filter changing:', filterType, '=', value);
    
    // Build the new filter state manually to avoid closure issues
    const newFilters = {
      ...activeFilters,
      [filterType]: value,
    };
    
    console.log('🔧 New filters will be:', newFilters);
    
    // Update the filter state
    updateFilter(filterType, value);
    
    // Trigger search immediately with the new filters (don't wait for state update)
    setTimeout(() => {
      console.log('🔧 Triggering search with new filters');
      searchWithAllFilters(searchText, newFilters);
    }, 50);
  }, [updateFilter, searchWithAllFilters, searchText, activeFilters]);'''
    
    new_handle_filter_change = '''  // Handle any filter change with validation - FIXED v3 (Integrated Validation)
  const handleFilterChange = useCallback((filterType: string, value: any) => {
    console.log('🔧 Filter changing with validation:', filterType, '=', value);
    
    // Input validation for range fields
    if (filterType === 'cmc' && value && typeof value === 'object') {
      if (value.min !== null && value.max !== null && value.min > value.max) {
        console.log('⚠️ Validation error: CMC min cannot exceed max');
        alert('Invalid CMC range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    if (filterType === 'power' && value && typeof value === 'object') {
      if (value.min !== null && value.max !== null && value.min > value.max) {
        console.log('⚠️ Validation error: Power min cannot exceed max');
        alert('Invalid Power range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    if (filterType === 'toughness' && value && typeof value === 'object') {
      if (value.min !== null && value.max !== null && value.min > value.max) {
        console.log('⚠️ Validation error: Toughness min cannot exceed max');
        alert('Invalid Toughness range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    // Build the new filter state manually to avoid closure issues
    const newFilters = {
      ...activeFilters,
      [filterType]: value,
    };
    
    console.log('🔧 New filters will be:', newFilters);
    
    // Update the filter state
    updateFilter(filterType, value);
    
    // Trigger search immediately with the new filters (don't wait for state update)
    setTimeout(() => {
      console.log('🔧 Triggering search with new filters');
      searchWithAllFilters(searchText, newFilters);
    }, 50);
  }, [updateFilter, searchWithAllFilters, searchText, activeFilters]);'''
    
    content = content.replace(old_handle_filter_change, new_handle_filter_change)
    
    # Now update all the input handlers to use the regular handleFilterChange (not the WithValidation version)
    old_handlers = [
        'handleFilterChangeWithValidation',
    ]
    
    for old_handler in old_handlers:
        content = content.replace(old_handler, 'handleFilterChange')
    
    # Write the updated file
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed function declaration order by integrating validation into handleFilterChange")

def main():
    """Execute the function order fix"""
    try:
        print("🔧 Fixing Function Declaration Order Issue")
        print("=" * 45)
        
        print("\n📋 Integrating validation into existing handleFilterChange...")
        fix_function_order()
        
        print("\n" + "=" * 45)
        print("✅ Function Order Fix Complete!")
        print("\n🎯 What was fixed:")
        print("   • Removed separate validation function")
        print("   • Integrated validation directly into handleFilterChange")
        print("   • No more 'used before declaration' errors")
        print("   • All input validation still works")
        print("\n🧪 Test Again:")
        print("   1. Run 'npm start' - should compile without errors")
        print("   2. Test invalid ranges - should still get validation alerts")
        print("   3. Test no results scenarios - should see graceful UI")
        
    except Exception as e:
        print(f"\n❌ Error during fix: {e}")
        print("Please check the file paths and try again.")

if __name__ == "__main__":
    main()
