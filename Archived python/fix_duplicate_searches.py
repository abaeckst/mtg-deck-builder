#!/usr/bin/env python3
"""
Fix duplicate search calls that cause the race condition
The console logs show multiple searches firing for the same query
"""

def fix_duplicate_searches():
    file_path = 'src/hooks/useCards.ts'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print('Fixing duplicate search calls...')
    
    # Add request deduplication to prevent multiple identical searches
    old_search_start = '''  // Search for cards with query and optional format filter - WITH DEBUG LOGGING
  const searchForCards = useCallback(async (query: string, format?: string) => {
    if (!query.trim()) {
      setState(prev => ({ 
        ...prev, 
        cards: [], 
        searchQuery: '', 
        totalCards: 0,
        selectedCards: new Set() // Clear selection when clearing search
      }));
      return;
    }

    console.log('SEARCH DEBUG:', { 
      query: query, 
      format: format, 
      timestamp: new Date().toISOString() 
    });

    clearError();
    setLoading(true);'''

    new_search_start = '''  // Search for cards with query and optional format filter - DEDUPLICATED
  const searchForCards = useCallback(async (query: string, format?: string) => {
    if (!query.trim()) {
      setState(prev => ({ 
        ...prev, 
        cards: [], 
        searchQuery: '', 
        totalCards: 0,
        selectedCards: new Set() // Clear selection when clearing search
      }));
      return;
    }

    // Create unique search key to prevent duplicate searches
    const searchKey = `${query}|${format || ''}`;
    const currentTime = Date.now();
    
    // Prevent duplicate searches within 1 second
    if (window.lastSearchKey === searchKey && window.lastSearchTime && (currentTime - window.lastSearchTime) < 1000) {
      console.log('SEARCH SKIPPED - Duplicate:', { query, format, searchKey });
      return;
    }
    
    window.lastSearchKey = searchKey;
    window.lastSearchTime = currentTime;

    console.log('SEARCH DEBUG:', { 
      query: query, 
      format: format, 
      searchKey: searchKey,
      timestamp: new Date().toISOString() 
    });

    clearError();
    setLoading(true);'''

    if old_search_start in content:
        content = content.replace(old_search_start, new_search_start)
        print('✅ Added search deduplication')
    else:
        print('❌ Could not find search function to update')
        return False

    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('✅ Fixed duplicate search issue')
    print('🧪 Test: Search for "angel" or "dawn" - should only see ONE search log per action')
    return True

if __name__ == '__main__':
    print('🚀 Fixing Duplicate Search Calls')
    print('=' * 50)
    fix_duplicate_searches()
