#!/usr/bin/env python3

import os
import sys

def add_comprehensive_debugging():
    """Add comprehensive debugging throughout the smart sorting system"""
    
    print("🔧 Adding comprehensive debugging to smart sorting system...")
    
    # Update useSorting.ts with detailed debugging
    useSorting_path = "src/hooks/useSorting.ts"
    if not os.path.exists(useSorting_path):
        print(f"❌ {useSorting_path} not found")
        return False
    
    with open(useSorting_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add comprehensive debugging to updateSort function
    old_updateSort = """  // Enhanced update sort with DIRECT ARCHITECTURE for smart sorting
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    console.log('🚨 ===== UPDATE SORT FUNCTION CALLED =====');
    console.log('🚨 PARAMETERS:', { area, criteria, direction });
    console.log('🚨 Current sortState:', sortState);
    
    const newSortState = {
      criteria,
      direction: direction ?? sortState[area].direction,
    };

    console.log('🎯 SORT UPDATE CALLED - DIRECT ARCHITECTURE:', {
      area,
      criteria,
      direction,
      previousState: sortState[area],
      newSortState
    });

    setSortState(prev => {
      const updatedState = {
        ...prev,
        [area]: newSortState,
      };
      console.log('🔧 SORT STATE UPDATED:', {
        area,
        oldState: prev[area],
        newState: newSortState,
        fullUpdatedState: updatedState
      });
      return updatedState;
    });

    // DIRECT ARCHITECTURE: Smart sorting for collection area  
    if (area === 'collection') {
      console.log('🚀 DIRECT SMART SORTING TRIGGERED');
      console.log('🔍 Available global functions:', {
        hasTriggerSearch: !!(window as any).triggerSearch,
        hasLastSearchMetadata: !!(window as any).lastSearchMetadata,
        windowKeys: Object.keys(window as any).filter(k => k.includes('trigger') || k.includes('Search') || k.includes('metadata'))
      });
      
      // Access global search function exposed by useCards
      const triggerSearch = (window as any).triggerSearch;
      if (triggerSearch) {
        console.log('✅ Global triggerSearch function found');
        // Get current search metadata from global state
        setTimeout(() => {
          const metadata = (window as any).lastSearchMetadata;
          console.log('🔍 Current metadata:', metadata);
          
          if (metadata && metadata.totalCards > 75) {
            // FIXED: Use the NEW sort state, not the current hook state
            const scryfallOrder = SCRYFALL_SORT_MAPPING[newSortState.criteria];
            const newSortParams = {
              order: scryfallOrder,
              dir: newSortState.direction,
            };
            
            console.log('🌐 TRIGGERING SERVER-SIDE SORT WITH NEW PARAMS:', {
              query: metadata.query,
              filters: metadata.filters,
              totalCards: metadata.totalCards,
              newSortState,
              newSortParams,
              threshold: '75+ cards = server-side sort'
            });
            console.log('🚀 CALLING triggerSearch NOW...');
            
            // Store the new sort params globally so searchWithPagination can use them
            (window as any).overrideSortParams = newSortParams;
            
            triggerSearch(metadata.query, metadata.filters);
            console.log('✅ triggerSearch call completed');
          } else {
            console.log('🏠 CLIENT-SIDE SORT:', {
              reason: metadata ? 
                (metadata.totalCards <= 75 ? `Small dataset (${metadata.totalCards} cards)` : 'Unknown reason') : 
                'No metadata available',
              metadata: metadata
            });
          }
        }, 10); // Small delay to ensure state is updated
      } else {
        console.error('❌ Global triggerSearch function not available');
        console.log('🔍 Debugging window object:', {
          allKeys: Object.keys(window as any).slice(0, 20),
          searchRelated: Object.keys(window as any).filter(k => 
            k.toLowerCase().includes('search') || 
            k.toLowerCase().includes('trigger') || 
            k.toLowerCase().includes('metadata')
          )
        });
      }
    }

    // Keep subscription system for backward compatibility (but direct takes precedence)
    const event: SortChangeEvent = {
      area,
      sortState: newSortState,
      requiresServerSearch: area === 'collection',
    };

    console.log('📢 Sort change event emitted (backup):', event);
    emitSortChange(event);
  }, [sortState]);"""

    new_updateSort = """  // Enhanced update sort with COMPREHENSIVE DEBUGGING
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
    
    console.log('🚨 ===== UPDATE SORT FUNCTION COMPLETE =====');
  }, [sortState]);"""

    content = content.replace(old_updateSort, new_updateSort)
    
    # Add debugging to getScryfallSortParams
    old_getScryfallSortParams = """  // Get Scryfall API parameters for server-side sorting
  const getScryfallSortParams = useCallback((area: AreaType) => {
    const state = sortState[area];
    const scryfallOrder = SCRYFALL_SORT_MAPPING[state.criteria];
    
    const params = {
      order: scryfallOrder,
      dir: state.direction,
    };
    
    console.log('🔧 GET SCRYFALL SORT PARAMS:', {
      area,
      currentSortState: state,
      returnedParams: params,
      fullSortState: sortState
    });
    
    return params;
  }, [sortState]);"""

    new_getScryfallSortParams = """  // Get Scryfall API parameters for server-side sorting - ENHANCED DEBUG
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

    content = content.replace(old_getScryfallSortParams, new_getScryfallSortParams)
    
    with open(useSorting_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Enhanced useSorting.ts with comprehensive debugging")
    
    # Update useCards.ts searchWithPagination function with detailed debugging
    useCards_path = "src/hooks/useCards.ts"
    if not os.path.exists(useCards_path):
        print(f"❌ {useCards_path} not found")
        return False
        
    with open(useCards_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Enhance searchWithPagination debug logging
    old_searchWithPagination = """      // Get Scryfall sort parameters with override support
      const baseSortParams = getScryfallSortParams('collection');
      const overrideParams = (window as any).overrideSortParams;
      const sortParams = overrideParams || baseSortParams;
      
      // Clear override after use
      if (overrideParams) {
        delete (window as any).overrideSortParams;
        console.log('🔧 USING OVERRIDE SORT PARAMS:', sortParams);
      } else {
        console.log('🔧 USING REGULAR SORT PARAMS:', sortParams);
      }
      
      // Execute paginated search with sort parameters
      console.log('🔧 PAGINATED SEARCH - Using sort parameters:', sortParams);
      console.log('🔧 PAGINATED SEARCH - Query details:', {
        query: query,
        filters: filters,
        sortOrder: sortParams.order,
        sortDirection: sortParams.dir
      });"""

    new_searchWithPagination = """      // COMPREHENSIVE SORT PARAMS DEBUG
      console.log('🔧 ===== SORT PARAMS RESOLUTION START =====');
      
      const baseSortParams = getScryfallSortParams('collection');
      console.log('🔧 BASE SORT PARAMS from getScryfallSortParams:', baseSortParams);
      
      const overrideParams = (window as any).overrideSortParams;
      console.log('🔧 OVERRIDE PARAMS from window:', overrideParams);
      
      const sortParams = overrideParams || baseSortParams;
      console.log('🔧 FINAL SORT PARAMS selected:', sortParams);
      
      // Clear override after use with confirmation
      if (overrideParams) {
        delete (window as any).overrideSortParams;
        console.log('🔧 ✅ USING OVERRIDE SORT PARAMS (cleared after use):', sortParams);
        console.log('🔧 Override params deleted, window.overrideSortParams now:', (window as any).overrideSortParams);
      } else {
        console.log('🔧 ✅ USING REGULAR SORT PARAMS:', sortParams);
      }
      
      console.log('🔧 ===== SORT PARAMS RESOLUTION COMPLETE =====');
      
      // Execute paginated search with comprehensive parameter logging
      console.log('🔧 PAGINATED SEARCH EXECUTION:');
      console.log('  - Query:', query);
      console.log('  - Filters:', filters);
      console.log('  - Sort Order:', sortParams.order);
      console.log('  - Sort Direction:', sortParams.dir);
      console.log('  - Full Sort Params Object:', sortParams);"""

    content = content.replace(old_searchWithPagination, new_searchWithPagination)
    
    with open(useCards_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Enhanced useCards.ts with comprehensive sort params debugging")
    
    # Update scryfallApi.ts with detailed API call logging
    scryfallApi_path = "src/services/scryfallApi.ts"
    if not os.path.exists(scryfallApi_path):
        print(f"❌ {scryfallApi_path} not found")
        return False
        
    with open(scryfallApi_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add comprehensive API request debugging
    old_api_request = """    const url = `${SCRYFALL_API_BASE}/cards/search?${params.toString()}`;
    console.log('🌐 SCRYFALL API REQUEST:', { 
      fullURL: url,
      queryParam: query.trim(),
      sortOrder: order,
      sortDirection: dir,
      parsedParams: Object.fromEntries(new URLSearchParams(url.split('?')[1] || ''))
    });
    const response = await rateLimitedFetch(url);
    const data = await response.json();"""

    new_api_request = """    const url = `${SCRYFALL_API_BASE}/cards/search?${params.toString()}`;
    
    console.log('🌐 ===== SCRYFALL API REQUEST DETAILED =====');
    console.log('🌐 FULL URL:', url);
    console.log('🌐 PARSED PARAMS:', Object.fromEntries(new URLSearchParams(url.split('?')[1] || '')));
    console.log('🌐 SORT ANALYSIS:', {
      originalQuery: query.trim(),
      sortOrder: order,
      sortDirection: dir,
      expectedBehavior: `Results should be sorted by ${order} in ${dir}ending order`,
      timestamp: new Date().toISOString()
    });
    console.log('🌐 REQUEST BREAKDOWN:', {
      baseURL: SCRYFALL_API_BASE,
      endpoint: '/cards/search',
      queryParameter: query.trim(),
      sortParameter: `order=${order}`,
      directionParameter: `dir=${dir}`,
      pageParameter: `page=${page}`
    });
    
    const response = await rateLimitedFetch(url);
    const data = await response.json();
    
    console.log('🌐 ===== SCRYFALL API RESPONSE ANALYSIS =====');
    console.log('🌐 RESPONSE STATUS:', response.status);
    console.log('🌐 TOTAL CARDS:', data.total_cards);
    console.log('🌐 RETURNED COUNT:', data.data?.length || 0);
    console.log('🌐 HAS MORE:', data.has_more);
    console.log('🌐 FIRST 3 CARD NAMES (sort verification):', 
      data.data?.slice(0, 3).map((card: any) => ({
        name: card.name,
        cmc: card.cmc,
        colors: card.colors
      })) || []
    );
    console.log('🌐 ===== API RESPONSE COMPLETE =====');"""

    content = content.replace(old_api_request, new_api_request)
    
    with open(scryfallApi_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Enhanced scryfallApi.ts with comprehensive API debugging")
    
    # Add debugging to MTGOLayout.tsx sort button clicks
    mtgoLayout_path = "src/components/MTGOLayout.tsx"
    if not os.path.exists(mtgoLayout_path):
        print(f"❌ {mtgoLayout_path} not found")
        return False
        
    with open(mtgoLayout_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add debugging to sort button clicks - find the first sort button
    old_sort_button = """                    <button 
                      className={collectionSort.criteria === 'name' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSort.criteria === 'name') {
                          updateSort('collection', 'name', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          updateSort('collection', 'name', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Name {collectionSort.criteria === 'name' ? (collectionSort.direction === 'asc' ? '↑' : '↓') : ''}
                    </button>"""

    new_sort_button = """                    <button 
                      className={collectionSort.criteria === 'name' ? 'active' : ''}
                      onClick={() => { 
                        console.log('🖱️ ===== SORT BUTTON CLICKED: NAME =====');
                        console.log('🖱️ Current sort state:', collectionSort);
                        console.log('🖱️ User action timestamp:', new Date().toISOString());
                        
                        if (collectionSort.criteria === 'name') {
                          const newDirection = collectionSort.direction === 'asc' ? 'desc' : 'asc';
                          console.log('🖱️ Toggling direction:', collectionSort.direction, '→', newDirection);
                          updateSort('collection', 'name', newDirection);
                        } else {
                          console.log('🖱️ Switching to name sort with asc direction');
                          updateSort('collection', 'name', 'asc');
                        }
                        
                        console.log('🖱️ updateSort call completed, closing menu');
                        setShowCollectionSortMenu(false); 
                        console.log('🖱️ ===== SORT BUTTON CLICK COMPLETE =====');
                      }}
                    >
                      Name {collectionSort.criteria === 'name' ? (collectionSort.direction === 'asc' ? '↑' : '↓') : ''}
                    </button>"""

    content = content.replace(old_sort_button, new_sort_button)
    
    with open(mtgoLayout_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Enhanced MTGOLayout.tsx with sort button click debugging")
    
    return True

if __name__ == "__main__":
    success = add_comprehensive_debugging()
    if success:
        print("\n🎯 COMPREHENSIVE DEBUGGING ADDED SUCCESSFULLY!")
        print("\n📋 NEXT STEPS:")
        print("1. Run `npm start` to test the application")
        print("2. Open browser console and click any collection sort button")
        print("3. Watch for detailed logging throughout the entire sort flow:")
        print("   - 🖱️ Sort button click logging")
        print("   - 🚨 updateSort function execution")
        print("   - 🔧 Sort params resolution")
        print("   - 🌐 Scryfall API request details")
        print("   - 🌐 API response analysis")
        print("\n🔍 WHAT TO LOOK FOR:")
        print("- Are sort buttons triggering updateSort()?")
        print("- Are sort parameters being computed correctly?")
        print("- Are API requests using the right sort order/direction?")
        print("- Are the returned card names actually sorted correctly?")
    else:
        print("❌ Failed to add comprehensive debugging")
    
    sys.exit(0 if success else 1)