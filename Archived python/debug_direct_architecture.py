#!/usr/bin/env python3

import os
import sys

def debug_direct_architecture(filename):
    """Add comprehensive debugging to verify direct architecture is working"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the direct architecture section and enhance debugging
    old_direct_section = '''    // DIRECT ARCHITECTURE: Smart sorting for collection area
    if (area === 'collection') {
      console.log('🚀 DIRECT SMART SORTING TRIGGERED');
      
      // Access global search function exposed by useCards
      const triggerSearch = (window as any).triggerSearch;
      if (triggerSearch) {
        // Get current search metadata from global state
        setTimeout(() => {
          const metadata = (window as any).lastSearchMetadata;
          if (metadata && metadata.totalCards > 75) {
            console.log('🌐 DIRECT SERVER-SIDE SORT:', {
              query: metadata.query,
              filters: metadata.filters,
              totalCards: metadata.totalCards,
              newSortState
            });
            triggerSearch(metadata.query, metadata.filters);
          } else {
            console.log('🏠 CLIENT-SIDE SORT (small dataset or no metadata)');
          }
        }, 10); // Small delay to ensure state is updated
      } else {
        console.error('❌ Global triggerSearch function not available');
      }
    }'''

    new_direct_section = '''    // DIRECT ARCHITECTURE: Smart sorting for collection area  
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

    if old_direct_section in content:
        content = content.replace(old_direct_section, new_direct_section)
        print("✅ Enhanced direct architecture debugging")
    else:
        print("❌ Could not find direct architecture section to enhance")
        return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully enhanced debugging in {filename}")
    return True

if __name__ == "__main__":
    success = debug_direct_architecture("src/hooks/useSorting.ts")
    sys.exit(0 if success else 1)
