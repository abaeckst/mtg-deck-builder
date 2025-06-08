#!/usr/bin/env python3

import os
import sys

def fix_sort_state_timing(filename):
    """Fix the timing issue where sort parameters use old state instead of new state"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The issue is in the direct architecture - it's using the current sort state
    # but the state update happens after the search is triggered
    # We need to use the NEW sort state instead of getting it from the hook
    
    old_direct_architecture = '''    // DIRECT ARCHITECTURE: Smart sorting for collection area  
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
            console.log('🌐 TRIGGERING SERVER-SIDE SORT:', {
              query: metadata.query,
              filters: metadata.filters,
              totalCards: metadata.totalCards,
              newSortState,
              threshold: '75+ cards = server-side sort'
            });
            console.log('🚀 CALLING triggerSearch NOW...');
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
    }'''

    new_direct_architecture = '''    // DIRECT ARCHITECTURE: Smart sorting for collection area  
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
    }'''

    if old_direct_architecture in content:
        content = content.replace(old_direct_architecture, new_direct_architecture)
        print("✅ Fixed direct architecture to use new sort state")
    else:
        print("❌ Could not find direct architecture section to fix")
        return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed sort state timing in {filename}")
    return True

if __name__ == "__main__":
    success = fix_sort_state_timing("src/hooks/useSorting.ts")
    sys.exit(0 if success else 1)
