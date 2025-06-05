#!/usr/bin/env python3

import os
import sys

def restore_search_functionality():
    """Restore all original search functionality that was removed during debugging"""
    
    # Fix scryfallApi.ts first
    api_filename = "src/services/scryfallApi.ts"
    
    if not os.path.exists(api_filename):
        print(f"Error: {api_filename} not found")
        return False
    
    with open(api_filename, 'r', encoding='utf-8') as f:
        api_content = f.read()
    
    # Remove the debugging bypass for 'creature' search
    old_build_query = '''function buildEnhancedSearchQuery(query: string): string {
  console.log('🔍 Building enhanced query for:', query);
  
  // SIMPLIFIED: For debugging, use simple type search for 'creature'
  if (query.toLowerCase().trim() === 'creature') {
    console.log('🔍 Using simple type:creature search');
    return 'type:creature';
  }
  
  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    const words = query.trim().split(/\\s+/);
    
    if (words.length > 1) {
      // Multi-word query: Each word should match name, oracle text, OR type
      // Format: (name:word1 OR o:word1 OR type:word1) (name:word2 OR o:word2 OR type:word2)
      console.log('🔍 Multi-word query detected, using comprehensive field search:', query);
      const wordQueries = words.map(word => `(name:${word} OR o:${word} OR type:${word})`);
      const result = wordQueries.join(' ');
      console.log('🔍 Multi-word result:', result);
      return result;
    } else {
      // Single word: search across multiple fields
      const result = `(name:${query} OR o:${query} OR type:${query})`;
      console.log('🔍 Single word query, using field search:', result);
      return result;
    }
  }'''
    
    # Restore original comprehensive search logic
    new_build_query = '''function buildEnhancedSearchQuery(query: string): string {
  // RESTORED: Full comprehensive multi-field search functionality
  console.log('🔍 Building enhanced query for:', query);
  
  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    const words = query.trim().split(/\\s+/);
    
    if (words.length > 1) {
      // Multi-word query: Each word should match name, oracle text, OR type
      // Format: (name:word1 OR o:word1 OR type:word1) (name:word2 OR o:word2 OR type:word2)
      console.log('🔍 Multi-word query detected, using comprehensive field search:', query);
      const wordQueries = words.map(word => `(name:${word} OR o:${word} OR type:${word})`);
      const result = wordQueries.join(' ');
      console.log('🔍 Multi-word result:', result);
      return result;
    } else {
      // Single word: search across multiple fields
      const result = `(name:${query} OR o:${query} OR type:${query})`;
      console.log('🔍 Single word query, using field search:', result);
      return result;
    }
  }'''
    
    if old_build_query in api_content:
        api_content = api_content.replace(old_build_query, new_build_query)
        print("✅ Restored comprehensive search query building")
    else:
        print("ℹ️  Could not find exact debugging bypass - search might already be restored")
    
    # Remove any other debugging bypasses in enhancedSearchCards
    old_enhanced_debug = '''  // For debugging, try simple search first without complex filtering
  if (query.trim() === 'creature') {
    console.log('🔍 Using simple creature search for debugging');
    return searchCards('type:creature', page, 'cards', order, dir);
  }'''
    
    if old_enhanced_debug in api_content:
        api_content = api_content.replace(old_enhanced_debug, '')
        print("✅ Removed debugging bypass from enhancedSearchCards")
    
    # Write the restored API file
    with open(api_filename, 'w', encoding='utf-8') as f:
        f.write(api_content)
    
    # Fix useCards.ts to restore filter functionality
    cards_filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(cards_filename):
        print(f"Error: {cards_filename} not found")
        return False
    
    with open(cards_filename, 'r', encoding='utf-8') as f:
        cards_content = f.read()
    
    # Remove the debugging bypass that removed filters
    old_enhanced_search_debug = '''    // For debugging: try simple search without filters for 'creature'
    if (query.trim() === 'creature') {
      console.log('🔍 Using simple creature search - bypassing filters');
      await searchWithPagination(query, {});
    } else {
      await searchWithPagination(query, filters);
    }'''
    
    new_enhanced_search_restored = '''    await searchWithPagination(query, filters);'''
    
    if old_enhanced_search_debug in cards_content:
        cards_content = cards_content.replace(old_enhanced_search_debug, new_enhanced_search_restored)
        print("✅ Restored filter functionality in enhancedSearch")
    else:
        print("ℹ️  Could not find debugging bypass in useCards - filters might already be restored")
    
    # Write the restored cards file
    with open(cards_filename, 'w', encoding='utf-8') as f:
        f.write(cards_content)
    
    print("✅ Restored all original search functionality")
    return True

def verify_functionality_restored():
    """Verify that key search functionality has been restored"""
    
    api_filename = "src/services/scryfallApi.ts"
    cards_filename = "src/hooks/useCards.ts"
    
    print("\n🔍 VERIFICATION - Checking restored functionality:")
    
    # Check API file
    if os.path.exists(api_filename):
        with open(api_filename, 'r', encoding='utf-8') as f:
            api_content = f.read()
        
        if 'name:${query} OR o:${query} OR type:${query}' in api_content:
            print("✅ Multi-field search (name, oracle text, type) restored")
        else:
            print("❌ Multi-field search not found")
            
        if 'type:creature' in api_content and 'SIMPLIFIED' in api_content:
            print("❌ Debugging bypass still present")
        else:
            print("✅ Debugging bypasses removed")
    
    # Check cards file  
    if os.path.exists(cards_filename):
        with open(cards_filename, 'r', encoding='utf-8') as f:
            cards_content = f.read()
            
        if 'searchWithPagination(query, filters)' in cards_content:
            print("✅ Filter functionality restored")
        else:
            print("❌ Filter functionality not restored")
            
        if 'bypassing filters' in cards_content:
            print("❌ Filter bypass still present")
        else:
            print("✅ Filter bypasses removed")
    
    print("\n📋 Expected behavior after restoration:")
    print("- 'creature' search should find cards with 'creature' in name, text, OR type")
    print("- All filters should work properly")
    print("- Multi-word searches should work across all fields")
    print("- Load More button should still work")

if __name__ == "__main__":
    print("🔧 RESTORING ORIGINAL SEARCH FUNCTIONALITY")
    print("=" * 50)
    
    success = restore_search_functionality()
    
    if success:
        verify_functionality_restored()
        print("\n✅ RESTORATION COMPLETE")
        print("\n📋 Next steps:")
        print("1. Refresh your browser")
        print("2. Test 'creature' search - should find creatures by name, text, and type")
        print("3. Test filters - should work with searches")
        print("4. Verify Load More button still works")
        print("5. Report any remaining issues")
    else:
        print("\n❌ RESTORATION FAILED")
        print("Please share the current search-related files for manual restoration")
    
    sys.exit(0 if success else 1)