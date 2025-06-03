#!/usr/bin/env python3
"""
Simplify search logic in useCards.ts
Issue: Queue validation system is completely broken and blocking all results
Solution: Replace with simple, working search logic
"""

def simplify_search_logic():
    file_path = "src/hooks/useCards.ts"
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading {file_path}")
        print(f"📏 File size: {len(content)} characters")
        
        # Find the start and end of the complex search function
        start_marker = "  // Search for cards with query and optional format filter - API DEGRADATION FIX"
        end_marker = "  }, [clearError, setLoading]);"
        
        start_index = content.find(start_marker)
        end_index = content.find(end_marker, start_index) + len(end_marker)
        
        if start_index == -1 or end_index == -1:
            print(f"❌ Could not find search function boundaries")
            return False
        
        # Create simplified search function
        simplified_search = '''  // Search for cards with query and optional format filter - SIMPLIFIED
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
        
        # Replace the complex function with the simplified one
        new_content = content[:start_index] + simplified_search + content[end_index:]
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"💾 Successfully updated {file_path}")
        print("🎯 Changes made:")
        print("   - Removed broken queue system entirely")
        print("   - Simplified to direct API calls with basic rate limiting")
        print("   - No complex validation that was blocking results")
        print("   - All valid search results will display immediately")
        print("   - Maintained error handling and loading states")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        return False
    except Exception as e:
        print(f"❌ Error updating file: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Simplifying search logic...")
    success = simplify_search_logic()
    
    if success:
        print("\n✅ SEARCH SIMPLIFICATION COMPLETE!")
        print("🧪 Test the fix:")
        print("   1. Run: npm start")
        print("   2. Search for 'angel' - should show angel cards immediately")
        print("   3. Search for 'snap' - should show snap cards immediately")
        print("   4. Try format filtering")
        print("   5. Console should only show simple logs without complex validation")
    else:
        print("\n❌ Fix failed - please check error messages above")
