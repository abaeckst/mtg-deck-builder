#!/usr/bin/env python3

import os
import sys

def fix_search_id_scope():
    """Fix the searchId scope issue in useCards.ts"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the searchId scope issue by moving the searchId declaration outside try block
    old_code = """    if (shouldUseServerSort) {
      console.log('🌐 Using server-side sorting - re-searching with new sort parameters');
      
      // Get Scryfall sort parameters
      const sortParams = getScryfallSortParams('collection');
      console.log('🔧 Scryfall sort params:', sortParams);
      
      // Re-search with same query and filters but new sort
      try {
        clearError();
        setLoading(true);
        
        const searchId = Date.now() + Math.random();
        (window as any).currentSearchId = searchId;"""

    new_code = """    if (shouldUseServerSort) {
      console.log('🌐 Using server-side sorting - re-searching with new sort parameters');
      
      // Get Scryfall sort parameters
      const sortParams = getScryfallSortParams('collection');
      console.log('🔧 Scryfall sort params:', sortParams);
      
      // Create unique search ID for race condition prevention
      const searchId = Date.now() + Math.random();
      (window as any).currentSearchId = searchId;
      
      // Re-search with same query and filters but new sort
      try {
        clearError();
        setLoading(true);"""

    if old_code in content:
        content = content.replace(old_code, new_code)
        print("✅ Fixed searchId scope issue by moving declaration outside try block")
    else:
        print("❌ Could not find the searchId scope issue to fix")
        print("Searching for alternative pattern...")
        
        # Alternative fix - look for the specific problematic section
        problematic_section = """        clearError();
        setLoading(true);
        
        const searchId = Date.now() + Math.random();
        (window as any).currentSearchId = searchId;
        
        // Rate limiting"""
        
        fixed_section = """        clearError();
        setLoading(true);
        
        // Rate limiting"""
        
        if problematic_section in content:
            # First, add searchId declaration before try block
            pre_try_pattern = """      // Re-search with same query and filters but new sort
      try {"""
            
            pre_try_replacement = """      // Create unique search ID for race condition prevention
      const searchId = Date.now() + Math.random();
      (window as any).currentSearchId = searchId;
      
      // Re-search with same query and filters but new sort
      try {"""
            
            content = content.replace(pre_try_pattern, pre_try_replacement)
            
            # Then remove the duplicate declaration inside try block
            content = content.replace(problematic_section, fixed_section)
            print("✅ Fixed searchId scope issue using alternative pattern")
        else:
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed {filename}")
    return True

if __name__ == "__main__":
    success = fix_search_id_scope()
    sys.exit(0 if success else 1)