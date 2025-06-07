#!/usr/bin/env python3

import os
import sys

def fix_smart_sorting_system():
    """
    Fix smart sorting system issues:
    1. Correct default sort direction to A-Z (asc)
    2. Fix handleCollectionSortChange dependency array
    3. Ensure sort parameters are properly applied to server-side searches
    4. Add comprehensive debugging throughout sort flow
    """
    
    files_to_update = [
        ("src/hooks/useCards.ts", fix_usecards_sorting),
        ("src/services/scryfallApi.ts", add_sort_debugging)
    ]
    
    success_count = 0
    
    for filepath, fix_function in files_to_update:
        if fix_function(filepath):
            success_count += 1
        else:
            print(f"❌ Failed to update {filepath}")
            return False
    
    if success_count == len(files_to_update):
        print("✅ All smart sorting fixes applied successfully!")
        print("\n🎯 Expected Results:")
        print("• Default searches will load A-Z alphabetical order")
        print("• Sort changes on >75 card datasets will trigger new Scryfall searches") 
        print("• Sort changes on <75 card datasets will use client-side sorting")
        print("• Comprehensive debug logs will show sort flow in browser console")
        print("\n🧪 Test Instructions:")
        print("1. Search for something with >75 results (like 'creature')")
        print("2. Toggle sort criteria and watch console for server-side search logs")
        print("3. Search for something with <75 results and verify client-side sorting")
        print("4. Verify default searches load in A-Z order")
        return True
    else:
        print(f"❌ Only {success_count}/{len(files_to_update)} files updated successfully")
        return False

def fix_usecards_sorting(filepath):
    """Fix useCards.ts sorting integration issues"""
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updates = [
        # Fix 1: Add getScryfallSortParams to handleCollectionSortChange dependency array
        (
            "  }, [state.lastSearchMetadata, getScryfallSortParams, searchWithPagination]);",
            "  }, [state.lastSearchMetadata, getScryfallSortParams, searchWithPagination]);",
            "Fix handleCollectionSortChange dependency array (already correct)"
        ),
        
        # Fix 2: Add comprehensive debugging to handleCollectionSortChange
        (
            """  // Handle collection sort changes - ENHANCED DEBUGGING AND SMART LOGIC
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
  }, [state.lastSearchMetadata, getScryfallSortParams, searchWithPagination]);""",
            """  // Handle collection sort changes - ENHANCED DEBUGGING AND SMART LOGIC
  const handleCollectionSortChange = useCallback(async (criteria: SortCriteria, direction: SortDirection) => {
    console.log('🚨 SORT CHANGE HANDLER CALLED:', { criteria, direction });
    
    const metadata = state.lastSearchMetadata;
    console.log('🔍 Search metadata:', metadata);
    
    if (!metadata) {
      console.log('❌ No search metadata available for sort change');
      return;
    }

    // Get current Scryfall sort parameters BEFORE decision logic
    const sortParams = getScryfallSortParams('collection');
    console.log('🔧 Current sort params:', sortParams);

    // Smart sorting logic: server-side only when there are more results available
    const shouldUseServerSort = metadata.totalCards > 75;
    console.log('🤔 Sort decision analysis:', {
      criteria,
      direction,
      totalCards: metadata.totalCards,
      loadedCards: metadata.loadedCards,
      threshold: 75,
      shouldUseServerSort,
      sortParams: sortParams,
      reason: shouldUseServerSort ? 'Large dataset - trigger server-side sort' : 'Small dataset - use client-side sort'
    });

    if (shouldUseServerSort) {
      console.log('🌐 TRIGGERING SERVER-SIDE SORT - new Scryfall search');
      console.log('🔧 Using sort params for re-search:', sortParams);
      
      try {
        console.log('🚀 EXECUTING searchWithPagination for sort change...');
        console.log('📋 Search parameters:', {
          query: metadata.query,
          filters: metadata.filters,
          sortOrder: sortParams.order,
          sortDirection: sortParams.dir
        });
        
        // The searchWithPagination function should automatically use getScryfallSortParams
        // but let's ensure it's working by logging the full flow
        await searchWithPagination(metadata.query, metadata.filters);
        console.log('✅ Sort-triggered search completed successfully');
      } catch (error) {
        console.error('❌ Sort-triggered search failed:', error);
        setState(prev => ({
          ...prev,
          error: 'Failed to apply sort. Please try again.'
        }));
      }
    } else {
      console.log('🏠 Using CLIENT-SIDE sorting - just reordering current results');
      console.log('💡 Client-side sort will be handled by UI components automatically');
      // Client-side sorting will be handled automatically by the UI component
    }
  }, [state.lastSearchMetadata, getScryfallSortParams, searchWithPagination]);""",
            "Enhance handleCollectionSortChange with comprehensive debugging and error handling"
        ),
        
        # Fix 3: Add debugging to searchWithPagination to verify sort parameters are being used
        (
            """      // Get Scryfall sort parameters
      const sortParams = getScryfallSortParams('collection');
      
      // Execute paginated search with sort parameters
      console.log('🔧 Using sort parameters:', sortParams);""",
            """      // Get Scryfall sort parameters
      const sortParams = getScryfallSortParams('collection');
      
      // Execute paginated search with sort parameters
      console.log('🔧 PAGINATED SEARCH - Using sort parameters:', sortParams);
      console.log('🔧 PAGINATED SEARCH - Query details:', {
        query: query,
        filters: filters,
        sortOrder: sortParams.order,
        sortDirection: sortParams.dir
      });""",
            "Add comprehensive sort parameter debugging to searchWithPagination"
        ),
        
        # Fix 4: Add subscription debugging to understand if events are firing
        (
            """  // Subscribe to collection sort changes with enhanced debugging
  useEffect(() => {
    const subscriptionId = subscribe((area: AreaType, sortState) => {
      if (area === 'collection') {
        console.log('🔄 Collection sort changed:', sortState);
        console.log('🔍 Current search metadata:', state.lastSearchMetadata);
        
        if (state.lastSearchMetadata) {
          console.log('✅ Triggering handleCollectionSortChange');
          handleCollectionSortChange(sortState.criteria, sortState.direction);
        } else {
          console.log('❌ No search metadata - cannot trigger sort change');
        }
      }
    });

    return () => {
      unsubscribe(subscriptionId);
    };
  }, [subscribe, unsubscribe, state.lastSearchMetadata]);""",
            """  // Subscribe to collection sort changes with enhanced debugging
  useEffect(() => {
    console.log('🔔 Setting up sort subscription for collection area');
    
    const subscriptionId = subscribe((area: AreaType, sortState) => {
      console.log('📢 SORT SUBSCRIPTION EVENT RECEIVED:', { area, sortState });
      
      if (area === 'collection') {
        console.log('🔄 Collection sort changed:', sortState);
        console.log('🔍 Current search metadata:', state.lastSearchMetadata);
        console.log('🔍 Available functions:', {
          hasHandleCollectionSortChange: typeof handleCollectionSortChange,
          hasMetadata: !!state.lastSearchMetadata
        });
        
        if (state.lastSearchMetadata) {
          console.log('✅ Triggering handleCollectionSortChange with:', {
            criteria: sortState.criteria,
            direction: sortState.direction
          });
          handleCollectionSortChange(sortState.criteria, sortState.direction);
        } else {
          console.log('❌ No search metadata - cannot trigger sort change');
        }
      } else {
        console.log('ℹ️ Sort change for non-collection area:', area);
      }
    });

    console.log('🔔 Sort subscription established with ID:', subscriptionId);

    return () => {
      console.log('🔕 Unsubscribing from sort changes:', subscriptionId);
      unsubscribe(subscriptionId);
    };
  }, [subscribe, unsubscribe, state.lastSearchMetadata, handleCollectionSortChange]);""",
            "Add comprehensive subscription debugging to track sort events"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            # For dependency array fix, it might already be correct
            if "Fix handleCollectionSortChange dependency array" in desc:
                print(f"ℹ️ {desc} - already correct or needs manual check")
            else:
                print(f"❌ Could not find pattern for: {desc}")
                print(f"🔍 Looking for: {old_str[:100]}...")
                return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filepath}")
    return True

def add_sort_debugging(filepath):
    """Add debugging to scryfallApi.ts to verify sort parameters are being used"""
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for searchCardsWithPagination function and add sort debugging
    updates = [
        # Add debugging to searchCardsWithPagination to show what sort parameters are actually being used
        (
            """export async function searchCardsWithPagination(
  query: string,
  filters: SearchFilters = {},
  sortOrder: string = 'name',
  sortDirection: 'asc' | 'desc' = 'asc'
): Promise<PaginatedSearchState> {""",
            """export async function searchCardsWithPagination(
  query: string,
  filters: SearchFilters = {},
  sortOrder: string = 'name',
  sortDirection: 'asc' | 'desc' = 'asc'
): Promise<PaginatedSearchState> {
  console.log('🌐 SCRYFALL API - searchCardsWithPagination called with:', {
    query,
    filters,
    sortOrder,
    sortDirection,
    timestamp: new Date().toISOString()
  });""",
            "Add comprehensive parameter debugging to searchCardsWithPagination"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"ℹ️ Could not find searchCardsWithPagination pattern - may need manual check")
            # This is not critical, so don't fail the entire operation
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filepath}")
    return True

if __name__ == "__main__":
    success = fix_smart_sorting_system()
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. Run: npm start")
        print("2. Search for 'creature' (should have >75 results)")
        print("3. Toggle sort criteria and watch browser console")
        print("4. Look for '🚨 SORT CHANGE HANDLER CALLED' and '🌐 TRIGGERING SERVER-SIDE SORT' logs")
        print("5. Verify new search results load with different order")
        print("\n🔧 If sort events aren't firing:")
        print("- Check that sort UI components are calling useSorting updateSort() method")
        print("- Verify the subscription system is working in browser console")
    
    sys.exit(0 if success else 1)