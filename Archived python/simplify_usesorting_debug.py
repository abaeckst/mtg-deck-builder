#!/usr/bin/env python3

import os
import sys

def simplify_usesorting_debug():
    """Simplify useSorting hook debug output and improve direct architecture"""
    
    filename = "src/hooks/useSorting.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simplify the updateSort function to be more reliable
    old_update_start = """  // Enhanced update sort with COMPREHENSIVE DEBUGGING
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    console.log('🚨 ===== UPDATE SORT FUNCTION CALLED =====');
    console.log('🚨 PARAMETERS:', { area, criteria, direction });
    console.log('🚨 Current sortState:', sortState);
    console.log('🚨 TIMESTAMP:', new Date().toISOString());
    
    const newSortState = {
      criteria,
      direction: direction ?? sortState[area].direction,
    };

    console.log('🎯 SORT UPDATE ANALYSIS:', {
      area,
      criteria,
      direction,
      previousState: sortState[area],
      newSortState,
      stateChanged: JSON.stringify(sortState[area]) !== JSON.stringify(newSortState),
      isCollection: area === 'collection'
    });

    // COMPREHENSIVE STATE CHANGE LOGGING
    setSortState(prev => {
      const updatedState = {
        ...prev,
        [area]: newSortState,
      };
      console.log('🔧 SORT STATE UPDATE COMPLETE:', {
        area,
        beforeUpdate: prev[area],
        afterUpdate: newSortState,
        fullStateAfter: updatedState,
        timestamp: new Date().toISOString()
      });
      return updatedState;
    });

    // COMPREHENSIVE DIRECT ARCHITECTURE DEBUGGING
    if (area === 'collection') {
      console.log('🚀 COLLECTION SORT TRIGGERED - COMPREHENSIVE DEBUG');
      
      // Global function availability check
      const globalState = {
        hasTriggerSearch: !!(window as any).triggerSearch,
        hasLastSearchMetadata: !!(window as any).lastSearchMetadata,
        hasOverrideSortParams: !!(window as any).overrideSortParams,
        allGlobalKeys: Object.keys(window as any).filter(k => 
          k.includes('trigger') || k.includes('Search') || k.includes('metadata') || k.includes('sort')
        )
      };
      console.log('🔍 GLOBAL STATE ANALYSIS:', globalState);
      
      const triggerSearch = (window as any).triggerSearch;
      if (triggerSearch) {
        console.log('✅ Global triggerSearch function available');
        
        // Immediate metadata check
        const metadata = (window as any).lastSearchMetadata;
        console.log('🔍 SEARCH METADATA ANALYSIS:', {
          hasMetadata: !!metadata,
          metadata: metadata,
          totalCards: metadata?.totalCards,
          loadedCards: metadata?.loadedCards,
          query: metadata?.query,
          isLargeDataset: metadata?.totalCards > 75
        });
        
        // Sort parameters computation
        const scryfallOrder = SCRYFALL_SORT_MAPPING[newSortState.criteria];
        const newSortParams = {
          order: scryfallOrder,
          dir: newSortState.direction,
        };
        console.log('🔧 SORT PARAMS COMPUTATION:', {
          inputCriteria: newSortState.criteria,
          scryfallOrder: scryfallOrder,
          direction: newSortState.direction,
          finalParams: newSortParams,
          mappingTable: SCRYFALL_SORT_MAPPING
        });
        
        // Decision logic comprehensive logging
        if (metadata && metadata.totalCards > 75) {
          console.log('🌐 SERVER-SIDE SORT DECISION CONFIRMED:', {
            reason: 'Large dataset detected',
            totalCards: metadata.totalCards,
            threshold: 75,
            triggerServerSort: true,
            query: metadata.query,
            filters: metadata.filters,
            sortParams: newSortParams
          });
          
          console.log('🚀 EXECUTING SERVER-SIDE SORT SEQUENCE:');
          console.log('  Step 1: Storing override params...');
          (window as any).overrideSortParams = newSortParams;
          console.log('  Step 2: Override params stored:', (window as any).overrideSortParams);
          
          console.log('  Step 3: Calling triggerSearch...');
          try {
            triggerSearch(metadata.query, metadata.filters);
            console.log('  Step 4: ✅ triggerSearch call completed successfully');
          } catch (error) {
            console.error('  Step 4: ❌ triggerSearch call failed:', error);
          }
        } else {
          console.log('🏠 CLIENT-SIDE SORT DECISION:', {
            reason: metadata ? 
              (metadata.totalCards <= 75 ? 'Small dataset' : 'Unknown reason') : 
              'No metadata available',
            totalCards: metadata?.totalCards || 0,
            threshold: 75,
            triggerServerSort: false,
            willUseClientSort: true
          });
        }
      } else {
        console.error('❌ CRITICAL: Global triggerSearch function NOT AVAILABLE');
        console.log('🔍 Window object debug:', {
          windowType: typeof window,
          hasWindow: typeof window !== 'undefined',
          allKeys: typeof window !== 'undefined' ? Object.keys(window as any).slice(0, 30) : 'No window',
          searchForTrigger: typeof window !== 'undefined' ? 
            Object.keys(window as any).filter(k => k.toLowerCase().includes('trigger')) : 'No window'
        });
      }
    }

    // Subscription system backup (comprehensive logging)
    const event: SortChangeEvent = {
      area,
      sortState: newSortState,
      requiresServerSearch: area === 'collection',
    };

    console.log('📢 SUBSCRIPTION EVENT EMISSION:', {
      event: event,
      subscriberCount: subscribers.length,
      timestamp: new Date().toISOString()
    });
    emitSortChange(event);
    
    // Track sort change timing for smart sorting logic in MTGOLayout
    (window as any).lastSortChangeTime = Date.now();
    
    console.log('🚨 ===== UPDATE SORT FUNCTION COMPLETE =====');
  }, [sortState]);"""

    new_update_start = """  // Simplified and reliable updateSort function
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    console.log('🎯 SORT UPDATE:', { area, criteria, direction });
    
    const newSortState = {
      criteria,
      direction: direction ?? sortState[area].direction,
    };

    // Update sort state
    setSortState(prev => ({
      ...prev,
      [area]: newSortState,
    }));

    // Handle collection sorting with simplified logic
    if (area === 'collection') {
      const triggerSearch = (window as any).triggerSearch;
      const metadata = (window as any).lastSearchMetadata;
      
      if (triggerSearch && metadata && metadata.totalCards > 75) {
        console.log('🌐 TRIGGERING SERVER-SIDE SORT:', {
          criteria: newSortState.criteria,
          direction: newSortState.direction,
          totalCards: metadata.totalCards
        });
        
        // Set override parameters for the search
        const scryfallOrder = SCRYFALL_SORT_MAPPING[newSortState.criteria];
        (window as any).overrideSortParams = {
          order: scryfallOrder,
          dir: newSortState.direction,
        };
        
        // Track sort timing
        (window as any).lastSortChangeTime = Date.now();
        
        // Trigger new search with sort parameters
        try {
          triggerSearch(metadata.query, metadata.filters);
          console.log('✅ Server-side sort search triggered');
        } catch (error) {
          console.error('❌ Failed to trigger sort search:', error);
        }
      } else {
        console.log('🏠 Client-side sort will be applied by UI components');
        (window as any).lastSortChangeTime = Date.now();
      }
    }

    // Emit subscription event for any remaining subscribers
    emitSortChange({
      area,
      sortState: newSortState,
      requiresServerSearch: area === 'collection',
    });
  }, [sortState]);"""

    if old_update_start in content:
        content = content.replace(old_update_start, new_update_start)
        print("✅ Simplified updateSort function with more reliable logic")
    else:
        print("❌ Could not find updateSort function")
        return False

    # Simplify the getScryfallSortParams function
    old_get_params = """  // Get Scryfall API parameters for server-side sorting - ENHANCED DEBUG
  const getScryfallSortParams = useCallback((area: AreaType) => {
    const state = sortState[area];
    const scryfallOrder = SCRYFALL_SORT_MAPPING[state.criteria];
    
    const params = {
      order: scryfallOrder,
      dir: state.direction,
    };
    
    console.log('🔧 GET SCRYFALL SORT PARAMS - DETAILED:', {
      functionCalled: 'getScryfallSortParams',
      inputArea: area,
      currentSortState: state,
      mappingLookup: {
        inputCriteria: state.criteria,
        mappedToScryfall: scryfallOrder,
        mappingTable: SCRYFALL_SORT_MAPPING
      },
      finalReturnedParams: params,
      fullSortStateContext: sortState,
      timestamp: new Date().toISOString()
    });
    
    return params;
  }, [sortState]);"""

    new_get_params = """  // Get Scryfall API parameters for server-side sorting
  const getScryfallSortParams = useCallback((area: AreaType) => {
    const state = sortState[area];
    const scryfallOrder = SCRYFALL_SORT_MAPPING[state.criteria];
    
    const params = {
      order: scryfallOrder,
      dir: state.direction,
    };
    
    console.log('🔧 Sort params for', area + ':', params);
    return params;
  }, [sortState]);"""

    if old_get_params in content:
        content = content.replace(old_get_params, new_get_params)
        print("✅ Simplified getScryfallSortParams function")
    else:
        print("❌ Could not find getScryfallSortParams function")

    # Write the updated content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully simplified {filename}")
    return True

if __name__ == "__main__":
    success = simplify_usesorting_debug()
    sys.exit(0 if success else 1)