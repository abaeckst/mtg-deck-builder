#!/usr/bin/env python3
"""
Fix search race condition in useCards.ts
Issue: Multiple searches overwrite each other when typing quickly
Solution: Cancel old searches and only process the latest one
"""

def fix_search_race_condition():
    file_path = "src/hooks/useCards.ts"
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading {file_path}")
        print(f"📏 File size: {len(content)} characters")
        
        # Find the simplified search function and replace it with race-condition-safe version
        old_search_function = '''  // Search for cards with query and optional format filter - SIMPLIFIED
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

    console.log('🔍 SEARCH STARTED:', { query, format: format || 'none' });

    try {
      clearError();
      setLoading(true);

      // Simple rate limiting - wait 150ms between searches
      const now = Date.now();
      const lastSearch = (window as any).lastSearchTime || 0;
      const timeSinceLastSearch = now - lastSearch;
      
      if (timeSinceLastSearch < 150) {
        await new Promise(resolve => setTimeout(resolve, 150 - timeSinceLastSearch));
      }
      
      (window as any).lastSearchTime = Date.now();

      // Execute API call
      const response = format && format !== '' 
        ? await searchCardsWithFilters(query, { 
            format: format === 'custom-standard' ? 'standard' : format 
          })
        : await searchCards(query);

      console.log('✅ SEARCH SUCCESS:', {
        query: query,
        format: format || 'none',
        resultCount: response.data.length,
        firstCard: response.data[0]?.name || 'NO_RESULTS'
      });

      // Always update state with results - no complex validation
      setState(prev => ({
        ...prev,
        cards: response.data,
        searchQuery: query,
        totalCards: response.total_cards,
        hasMore: response.has_more,
        selectedCards: new Set(), // Clear selection on new search
      }));

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
      
      console.error('❌ SEARCH ERROR:', {
        query: query,
        format: format || 'none',
        error: errorMessage
      });

      setState(prev => ({
        ...prev,
        error: errorMessage,
        cards: [],
        totalCards: 0,
        hasMore: false,
      }));
    } finally {
      setLoading(false);
    }
  }, [clearError, setLoading]);'''
        
        new_search_function = '''  // Search for cards with query and optional format filter - RACE CONDITION SAFE
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

    // Create unique search ID to prevent race conditions
    const searchId = Date.now() + Math.random();
    (window as any).currentSearchId = searchId;

    console.log('🔍 SEARCH STARTED:', { 
      searchId: searchId.toFixed(3), 
      query, 
      format: format || 'none' 
    });

    try {
      clearError();
      setLoading(true);

      // Simple rate limiting - wait 150ms between searches
      const now = Date.now();
      const lastSearch = (window as any).lastSearchTime || 0;
      const timeSinceLastSearch = now - lastSearch;
      
      if (timeSinceLastSearch < 150) {
        await new Promise(resolve => setTimeout(resolve, 150 - timeSinceLastSearch));
      }
      
      // Check if this search was cancelled while waiting
      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 SEARCH CANCELLED:', { 
          searchId: searchId.toFixed(3), 
          query,
          reason: 'superseded by newer search'
        });
        return;
      }
      
      (window as any).lastSearchTime = Date.now();

      // Execute API call
      const response = format && format !== '' 
        ? await searchCardsWithFilters(query, { 
            format: format === 'custom-standard' ? 'standard' : format 
          })
        : await searchCards(query);

      // Check if this search was cancelled while API call was in progress
      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 SEARCH CANCELLED:', { 
          searchId: searchId.toFixed(3), 
          query,
          reason: 'superseded during API call'
        });
        return;
      }

      console.log('✅ SEARCH SUCCESS:', {
        searchId: searchId.toFixed(3),
        query: query,
        format: format || 'none',
        resultCount: response.data.length,
        firstCard: response.data[0]?.name || 'NO_RESULTS'
      });

      // Only update state if this is still the current search
      setState(prev => ({
        ...prev,
        cards: response.data,
        searchQuery: query,
        totalCards: response.total_cards,
        hasMore: response.has_more,
        selectedCards: new Set(), // Clear selection on new search
      }));

    } catch (error) {
      // Only show error if this search wasn't cancelled
      if ((window as any).currentSearchId === searchId) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
        
        console.error('❌ SEARCH ERROR:', {
          searchId: searchId.toFixed(3),
          query: query,
          format: format || 'none',
          error: errorMessage
        });

        setState(prev => ({
          ...prev,
          error: errorMessage,
          cards: [],
          totalCards: 0,
          hasMore: false,
        }));
      }
    } finally {
      // Only clear loading if this is still the current search
      if ((window as any).currentSearchId === searchId) {
        setLoading(false);
      }
    }
  }, [clearError, setLoading]);'''
        
        if old_search_function in content:
            content = content.replace(old_search_function, new_search_function)
            print("✅ Replaced search function with race-condition-safe version")
        else:
            print("❌ Could not find search function to replace")
            return False
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Successfully updated {file_path}")
        print("🎯 Changes made:")
        print("   - Added unique search ID tracking")
        print("   - Cancel old searches when new ones start")
        print("   - Only update UI with results from current search")
        print("   - Added detailed logging with search IDs")
        print("   - Prevents race conditions during typing")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        return False
    except Exception as e:
        print(f"❌ Error updating file: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing search race condition...")
    success = fix_search_race_condition()
    
    if success:
        print("\n✅ RACE CONDITION FIX COMPLETE!")
        print("🧪 Test the fix:")
        print("   1. Run: npm start")
        print("   2. Type 'smoke' quickly - should only show smoke cards")
        print("   3. Type 'angel' quickly - should only show angel cards")
        print("   4. Console should show cancelled searches with 🚫 SEARCH CANCELLED")
        print("   5. Only the final search should update the UI")
    else:
        print("\n❌ Fix failed - please check error messages above")
