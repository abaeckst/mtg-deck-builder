#!/usr/bin/env python3

import os
import sys

def update_scryfall_api(filename):
    """Fix TypeScript filter type issues in scryfallApi.ts"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the problematic filterDetails object creation
    old_problematic_section = '''  console.log('🔧 Final search query built:', { 
    originalQuery: query, 
    finalQuery: searchQuery.trim(),
    activeFilters: activeFilters,
    filterDetails: activeFilters.reduce((acc, key) => {
      acc[key] = filters[key];
      return acc;
    }, {} as Partial<SearchFilters>)
  });'''

    new_type_safe_section = '''  // Create type-safe filter details for debugging
  const filterDetails: Record<string, any> = {};
  activeFilters.forEach(key => {
    filterDetails[key] = filters[key];
  });
  
  console.log('🔧 Final search query built:', { 
    originalQuery: query, 
    finalQuery: searchQuery.trim(),
    activeFilters: activeFilters,
    filterDetails: filterDetails
  });'''

    if old_problematic_section in content:
        content = content.replace(old_problematic_section, new_type_safe_section)
        print("✅ Fixed TypeScript filter type issue - replaced problematic reduce with type-safe forEach")
    else:
        print("❌ Could not find the exact problematic section")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_scryfall_api("src/services/scryfallApi.ts")
    sys.exit(0 if success else 1)