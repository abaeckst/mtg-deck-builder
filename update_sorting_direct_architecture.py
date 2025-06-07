#!/usr/bin/env python3

import os
import sys

def update_sorting_direct_architecture(filename):
    """Update useSorting.ts with direct architecture for smart sorting"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the updateSort function and replace it with direct architecture version
    old_update_sort = '''  // Enhanced update sort with subscription notification
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    const newSortState = {
      criteria,
      direction: direction ?? sortState[area].direction,
    };

    console.log('🎯 SORT UPDATE CALLED:', {
      area,
      criteria,
      direction,
      previousState: sortState[area],
      newSortState,
      subscriberCount: subscribers.length
    });

    setSortState(prev => ({
      ...prev,
      [area]: newSortState,
    }));

    // Determine if this change requires server-side re-search
    const requiresServerSearch = area === 'collection';

    // Emit sort change event to subscribers
    const event: SortChangeEvent = {
      area,
      sortState: newSortState,
      requiresServerSearch,
    };

    console.log('📢 Sort change event emitted:', event);
    console.log('📢 Notifying', subscribers.length, 'subscribers');
    emitSortChange(event);
  }, [sortState]);'''

    new_update_sort = '''  // Enhanced update sort with DIRECT ARCHITECTURE for smart sorting
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
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

    setSortState(prev => ({
      ...prev,
      [area]: newSortState,
    }));

    // DIRECT ARCHITECTURE: Smart sorting for collection area
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
    }

    // Keep subscription system for backward compatibility (but direct takes precedence)
    const event: SortChangeEvent = {
      area,
      sortState: newSortState,
      requiresServerSearch: area === 'collection',
    };

    console.log('📢 Sort change event emitted (backup):', event);
    emitSortChange(event);
  }, [sortState]);'''

    if old_update_sort in content:
        content = content.replace(old_update_sort, new_update_sort)
        print("✅ Updated updateSort function with direct architecture")
    else:
        print("❌ Could not find updateSort function to replace")
        return False

    # Add global metadata exposure function
    add_global_metadata = '''// Global metadata exposure for direct architecture
const exposeSearchMetadata = (metadata: any) => {
  (window as any).lastSearchMetadata = metadata;
};

// Export for use by useCards
(window as any).exposeSearchMetadata = exposeSearchMetadata;

// Global subscription system'''

    if '// Global subscription system' in content:
        content = content.replace('// Global subscription system', add_global_metadata)
        print("✅ Added global metadata exposure system")
    else:
        print("❌ Could not find insertion point for global metadata system")
        return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename} with direct architecture")
    return True

if __name__ == "__main__":
    success = update_sorting_direct_architecture("src/hooks/useSorting.ts")
    sys.exit(0 if success else 1)
