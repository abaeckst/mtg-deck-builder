#!/usr/bin/env python3

import os
import sys

def fix_typescript_properly():
    """Fix the TypeScript error properly by adding proper type handling"""
    
    filename = "src/services/scryfallApi.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the problematic debugging code with proper TypeScript
    old_debug_code = '''  console.log('🔧 Final search query built:', { 
    originalQuery: query, 
    finalQuery: searchQuery.trim(),
    appliedFilters: Object.keys(filters).filter(key => {
      const value = filters[key];
      return value && (Array.isArray(value) ? value.length > 0 : 
                      typeof value === 'object' ? Object.values(value).some(v => v !== null && v !== '') :
                      value !== '' && value !== null);
    })
  });
  
  return searchCardsWithSort(searchQuery.trim(), { page, order, dir });'''
    
    new_debug_code = '''  console.log('🔧 Final search query built:', { 
    originalQuery: query, 
    finalQuery: searchQuery.trim(),
    appliedFilters: (Object.keys(filters) as (keyof SearchFilters)[]).filter(key => {
      const value = filters[key];
      if (value === undefined || value === null || value === '') return false;
      if (Array.isArray(value)) return value.length > 0;
      if (typeof value === 'object' && value !== null) {
        return Object.values(value).some(v => v !== null && v !== '');
      }
      return true;
    })
  });
  
  return searchCardsWithSort(searchQuery.trim(), { page, order, dir });'''
    
    if old_debug_code in content:
        content = content.replace(old_debug_code, new_debug_code)
        print("✅ Fixed TypeScript error with proper type assertion")
    else:
        print("❌ Could not find the problematic debugging code")
        return False
    
    # Write the fixed content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ TypeScript error fixed properly with type safety")
    return True

if __name__ == "__main__":
    success = fix_typescript_properly()
    if success:
        print("\n✅ TYPESCRIPT ERROR FIXED PROPERLY")
        print("\n📋 What was done:")
        print("1. ✅ Added proper type assertion: (keyof SearchFilters)[]")
        print("2. ✅ Maintained full debugging functionality")
        print("3. ✅ Preserved type safety throughout")
        print("4. ✅ Handles all filter value types correctly")
        print("\n📱 Test steps:")
        print("1. Save file and check compilation")
        print("2. Should compile without TypeScript errors")
        print("3. Test 'creature' search")
        print("4. Check console for complete filter debugging")
    else:
        print("\n❌ Fix failed")
    
    sys.exit(0 if success else 1)