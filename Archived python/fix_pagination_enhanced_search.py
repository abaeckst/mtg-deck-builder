#!/usr/bin/env python3

import os
import sys

def fix_pagination_enhanced_search(filename):
    """Fix searchCardsWithPagination to use enhancedSearchCards instead of searchCardsWithFilters"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the pagination function to use enhanced search
    old_pagination_call = '''    // Get first page with 75-card limit
    const response = await searchCardsWithFilters(query, filters, 1, order, dir);'''

    new_pagination_call = '''    // Get first page with 75-card limit - FIXED: Use enhanced search
    const response = await enhancedSearchCards(query, filters, 1, order, dir);'''

    # Fix the loadMoreResults function too
    old_load_more_call = '''    const response = await searchCardsWithFilters(
      paginationState.lastQuery,
      paginationState.lastFilters,
      nextPage,
      paginationState.lastSort.order,
      paginationState.lastSort.dir
    );'''

    new_load_more_call = '''    const response = await enhancedSearchCards(
      paginationState.lastQuery,
      paginationState.lastFilters,
      nextPage,
      paginationState.lastSort.order,
      paginationState.lastSort.dir
    );'''

    # Apply the fixes
    if old_pagination_call in content:
        content = content.replace(old_pagination_call, new_pagination_call)
        print("✅ Fixed searchCardsWithPagination to use enhancedSearchCards")
    else:
        print("❌ Could not find searchCardsWithPagination call to fix")
        return False
    
    if old_load_more_call in content:
        content = content.replace(old_load_more_call, new_load_more_call)
        print("✅ Fixed loadMoreResults to use enhancedSearchCards")
    else:
        print("❌ Could not find loadMoreResults call to fix")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed {filename}")
    print("\n🎯 WHAT THIS FIXES:")
    print("✅ Multi-word searches will now work properly")
    print("✅ 'lightning' will search name, oracle text, AND type fields")
    print("✅ Query: lightning → (name:lightning OR o:lightning OR type:lightning)")
    print("✅ Load More will also use enhanced search consistently")
    print("\n🧪 TEST:")
    print("1. Search for 'lightning' - should find cards with lightning in text/type")
    print("2. Search for 'dragon wizard' - should find cards that are dragons OR wizards")
    print("3. Search for 'destroy target' - should find cards with that text")
    
    return True

if __name__ == "__main__":
    success = fix_pagination_enhanced_search("src/services/scryfallApi.ts")
    sys.exit(0 if success else 1)