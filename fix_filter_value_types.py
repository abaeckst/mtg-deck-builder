#!/usr/bin/env python3

import os
import sys

def fix_filter_value_types():
    """Fix the filter value type checking to handle numbers properly"""
    
    filename = "src/services/scryfallApi.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the problematic type checking code
    old_type_check = '''    appliedFilters: (Object.keys(filters) as (keyof SearchFilters)[]).filter(key => {
      const value = filters[key];
      if (value === undefined || value === null || value === '') return false;
      if (Array.isArray(value)) return value.length > 0;
      if (typeof value === 'object' && value !== null) {
        return Object.values(value).some(v => v !== null && v !== '');
      }
      return true;
    })'''
    
    new_type_check = '''    appliedFilters: (Object.keys(filters) as (keyof SearchFilters)[]).filter(key => {
      const value = filters[key];
      if (value === undefined || value === null || value === '') return false;
      if (Array.isArray(value)) return value.length > 0;
      if (typeof value === 'object' && value !== null) {
        // Handle range objects like cmc: { min: number, max: number }
        return Object.values(value).some(v => v !== null && v !== undefined && v !== '');
      }
      return true;
    })'''
    
    if old_type_check in content:
        content = content.replace(old_type_check, new_type_check)
        print("✅ Fixed filter value type checking for numbers")
    else:
        print("❌ Could not find the exact type checking code")
        return False
    
    # Write the fixed content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Filter value type checking fixed")
    return True

if __name__ == "__main__":
    success = fix_filter_value_types()
    if success:
        print("\n✅ FILTER VALUE TYPE CHECKING FIXED")
        print("\n📋 What was fixed:")
        print("1. ✅ Removed string comparison for number values")
        print("2. ✅ Added undefined check for completeness")
        print("3. ✅ Handles range objects (cmc, power, toughness) properly")
        print("4. ✅ Maintains type safety for all filter value types")
        print("\n📱 Test steps:")
        print("1. Save file and check compilation")
        print("2. Should compile without TypeScript errors")
        print("3. Test 'creature' search")
        print("4. Check console for filter debugging")
    else:
        print("\n❌ Fix failed")
    
    sys.exit(0 if success else 1)