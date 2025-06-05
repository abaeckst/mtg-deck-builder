#!/usr/bin/env python3

import os
import sys

def fix_format_filter_logic():
    """Fix the format filter logic that's still adding legal:standard"""
    
    filename = "src/services/scryfallApi.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix the format filter logic
    old_format_logic = '''  // Add format filter with proper Scryfall syntax
  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Use standard format (Final Fantasy set is standard-legal)
      searchQuery += ` legal:standard`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }'''
    
    new_format_logic = '''  // Add format filter with proper Scryfall syntax
  if (filters.format && filters.format.trim() !== '') {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Use standard format (Final Fantasy set is standard-legal)
      searchQuery += ` legal:standard`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }'''
    
    if old_format_logic in content:
        content = content.replace(old_format_logic, new_format_logic)
        print("✅ Fixed format filter logic to check for empty strings")
    else:
        print("❌ Could not find exact format filter logic")
        return False
    
    # Write the fixed content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed format filter logic")
    return True

def check_debug_logs():
    """Add debugging to see what's happening with the search"""
    
    filename = "src/services/scryfallApi.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add more detailed debugging to searchCardsWithFilters
    old_debug_log = '''  console.log('🔧 Building search query from:', { baseQuery: query, filters, sort: { order, dir } });'''
    
    new_debug_log = '''  console.log('🔧 Building search query from:', { 
    baseQuery: query, 
    filters, 
    sort: { order, dir },
    formatFilter: filters.format,
    hasFormatFilter: !!filters.format && filters.format.trim() !== ''
  });'''
    
    if old_debug_log in content:
        content = content.replace(old_debug_log, new_debug_log)
        print("✅ Added detailed debugging for format filter")
    else:
        print("ℹ️  Debug log not found - might already be detailed")
    
    # Add debugging after the search query is built
    old_return = '''  return searchCardsWithSort(searchQuery.trim(), { page, order, dir });'''
    
    new_return = '''  console.log('🔧 Final search query built:', { 
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
    
    if old_return in content:
        content = content.replace(old_return, new_return)
        print("✅ Added final query debugging")
    else:
        print("ℹ️  Final return not found - might already have debugging")
    
    # Write the updated content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    print("🔧 FIXING FORMAT FILTER LOGIC")
    print("=" * 50)
    
    success1 = fix_format_filter_logic()
    success2 = check_debug_logs()
    
    if success1:
        print("\n✅ FORMAT FILTER LOGIC FIXED")
        print("\n📋 What was fixed:")
        print("1. ✅ Format filter now checks for empty strings")
        print("2. ✅ Added detailed debugging for troubleshooting")
        print("3. ✅ Should prevent legal:standard being added when format is empty")
        print("\n📱 Test steps:")
        print("1. Refresh browser")
        print("2. Search for 'creature'")
        print("3. Check console for detailed filter debugging")
        print("4. Should see no legal:standard in the final query")
    else:
        print("\n❌ Fix failed")
    
    sys.exit(0 if success1 else 1)