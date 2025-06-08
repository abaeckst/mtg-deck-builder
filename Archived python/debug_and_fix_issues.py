#!/usr/bin/env python3

import os
import sys

def debug_and_fix_issues():
    """Fix both the Popular Cards loading issue and Sort change issue"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Add error handling to loadPopularCards and use a simpler query
    old_popular_query = """const POPULAR_CARDS_QUERY = 'legal:standard (type:creature OR type:instant OR type:sorcery OR type:planeswalker OR type:enchantment OR type:artifact)';"""
    
    new_popular_query = """const POPULAR_CARDS_QUERY = 'type:creature legal:standard';"""
    
    if old_popular_query in content:
        content = content.replace(old_popular_query, new_popular_query)
        print("✅ Simplified popular cards query")
    else:
        print("⚠️ Could not find popular cards query")
    
    # Fix 2: Add debugging to loadPopularCards function
    old_load_popular = """  // Load popular/example cards with proper pagination
  const loadPopularCards = useCallback(async () => {
    console.log('🎯 Loading popular cards with pagination support...');
    
    // Use the same pagination system as searches
    await searchWithPagination(POPULAR_CARDS_QUERY, {});
    
    // Update the search query display
    setState(prev => ({
      ...prev,
      searchQuery: 'Popular Cards',
    }));
  }, [searchWithPagination]);"""
    
    new_load_popular = """  // Load popular/example cards with proper pagination and error handling
  const loadPopularCards = useCallback(async () => {
    console.log('🎯 Loading popular cards with pagination support...');
    
    try {
      // Use the same pagination system as searches
      await searchWithPagination(POPULAR_CARDS_QUERY, {});
      
      // Update the search query display
      setState(prev => ({
        ...prev,
        searchQuery: 'Popular Cards',
      }));
      
      console.log('✅ Popular cards loaded successfully');
    } catch (error) {
      console.error('❌ Failed to load popular cards:', error);
      
      // Fallback: try a simpler query
      try {
        console.log('🔄 Trying fallback query: creature');
        await searchWithPagination('creature', {});
        setState(prev => ({
          ...prev,
          searchQuery: 'Popular Cards',
        }));
        console.log('✅ Fallback popular cards loaded');
      } catch (fallbackError) {
        console.error('❌ Fallback also failed:', fallbackError);
        setState(prev => ({
          ...prev,
          error: 'Failed to load popular cards. Try searching manually.',
          searchQuery: 'Error loading popular cards',
        }));
      }
    }
  }, [searchWithPagination]);"""
    
    if old_load_popular in content:
        content = content.replace(old_load_popular, new_load_popular)
        print("✅ Added error handling to loadPopularCards")
    else:
        print("❌ Could not find loadPopularCards function")
        return False
    
    # Fix 3: Add debugging to handleCollectionSortChange to see why it's not working
    old_sort_handler = """  // Handle collection sort changes with smart re-search logic - FIXED SERVER-SIDE INTEGRATION
  const handleCollectionSortChange = useCallback(async (criteria: SortCriteria, direction: SortDirection) => {
    const metadata = state.lastSearchMetadata;
    if (!metadata) {
      console.log('🔄 No search metadata available for sort change');
      return;
    }

    // FORCE server-side sorting for datasets with >75 cards to get different results
    const shouldUseServerSort = metadata.totalCards > 75;
    console.log('🔄 Sort change analysis:', {
      criteria,
      direction,
      totalCards: metadata.totalCards,
      loadedCards: metadata.loadedCards,
      threshold: 75,
      shouldUseServerSort,
      reason: shouldUseServerSort ? 'FORCE server-side sort - get different cards from Scryfall' : 'Small dataset - use client sort'
    });

    if (shouldUseServerSort) {
      console.log('🌐 FORCING server-side sorting - fetching completely different results from Scryfall');
      
      // Get current Scryfall sort parameters (will reflect the new sort)
      const sortParams = getScryfallSortParams('collection');
      console.log('🔧 Scryfall sort params for FORCED re-search:', sortParams);
      
      // FORCE re-search with same query and filters but new sort parameters
      // This will get different cards from Scryfall, not just reorder the same 75
      await searchWithPagination(metadata.query, metadata.filters);
    } else {
      console.log('🏠 Using client-side sorting - dataset is small, no re-search needed');
      // Client-side sorting will be handled by the UI component automatically
    }
  }, [state.lastSearchMetadata, getScryfallSortParams, searchWithPagination]);"""
    
    new_sort_handler = """  // Handle collection sort changes - ENHANCED DEBUGGING AND SMART LOGIC
  const handleCollectionSortChange = useCallback(async (criteria: SortCriteria, direction: SortDirection) => {
    console.log('🚨 SORT CHANGE HANDLER CALLED:', { criteria, direction });
    
    const metadata = state.lastSearchMetadata;
    console.log('🔍 Search metadata:', metadata);
    
    if (!metadata) {
      console.log('❌ No search metadata available for sort change');
      return;
    }

    // Smart sorting logic: server-side only when there are more results available
    const shouldUseServerSort = metadata.totalCards > 75;
    console.log('🤔 Sort decision analysis:', {
      criteria,
      direction,
      totalCards: metadata.totalCards,
      loadedCards: metadata.loadedCards,
      threshold: 75,
      shouldUseServerSort,
      reason: shouldUseServerSort ? 'Large dataset - trigger server-side sort' : 'Small dataset - use client-side sort'
    });

    if (shouldUseServerSort) {
      console.log('🌐 TRIGGERING SERVER-SIDE SORT - new Scryfall search');
      
      // Get current Scryfall sort parameters
      const sortParams = getScryfallSortParams('collection');
      console.log('🔧 Sort params for re-search:', sortParams);
      
      try {
        console.log('🚀 EXECUTING searchWithPagination for sort change...');
        await searchWithPagination(metadata.query, metadata.filters);
        console.log('✅ Sort-triggered search completed successfully');
      } catch (error) {
        console.error('❌ Sort-triggered search failed:', error);
      }
    } else {
      console.log('🏠 Using CLIENT-SIDE sorting - just reordering current results');
      // Client-side sorting will be handled automatically by the UI component
    }
  }, [state.lastSearchMetadata, getScryfallSortParams, searchWithPagination]);"""
    
    if old_sort_handler in content:
        content = content.replace(old_sort_handler, new_sort_handler)
        print("✅ Enhanced handleCollectionSortChange with debugging")
    else:
        print("❌ Could not find handleCollectionSortChange function")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed both popular cards loading and sort change debugging")
    return True

if __name__ == "__main__":
    success = debug_and_fix_issues()
    sys.exit(0 if success else 1)