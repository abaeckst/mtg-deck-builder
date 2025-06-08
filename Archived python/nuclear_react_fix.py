#!/usr/bin/env python3

import os
import sys

def nuclear_react_fix():
    """Nuclear option: Force complete array recreation and component unmounting/remounting"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add a sort tracking state
    old_sort_metadata = """    // Sort integration state
    lastSearchMetadata: null,"""

    new_sort_metadata = """    // Sort integration state
    lastSearchMetadata: null,
    sortChangeId: 0, // Force React updates on sort changes"""

    if old_sort_metadata in content:
        content = content.replace(old_sort_metadata, new_sort_metadata)
        print("✅ Added sort change ID tracking")
    else:
        print("❌ Could not find sort metadata")
        return False

    # Update the state when sort-triggered searches complete
    old_sort_complete = """      // Clear priority status after successful update
      if (isPrioritySearch) {
        setTimeout(() => {
          delete (window as any).prioritySearchId;
          console.log('🔄 PRIORITY SEARCH COMPLETED - Status cleared');
        }, 100);
      }
      
      // Force component re-render by updating a tracking value
      if (isSortTriggered) {
        (window as any).lastSuccessfulSortUpdate = updateTimestamp;
        console.log('🔄 SORT UPDATE COMPLETED:', {
          updateTimestamp,
          newCardCount: newCards.length,
          firstCard: newCards[0]?.name,
          lastCard: newCards[newCards.length - 1]?.name
        });
      }"""

    new_sort_complete = """      // Clear priority status after successful update
      if (isPrioritySearch) {
        setTimeout(() => {
          delete (window as any).prioritySearchId;
          console.log('🔄 PRIORITY SEARCH COMPLETED - Status cleared');
        }, 100);
      }
      
      // NUCLEAR: Force complete state reset for sort changes
      if (isSortTriggered) {
        (window as any).lastSuccessfulSortUpdate = updateTimestamp;
        
        // Force React to see this as completely new data
        const sortChangeId = Date.now();
        console.log('🔄 NUCLEAR SORT UPDATE - COMPLETE STATE RESET:', {
          updateTimestamp,
          sortChangeId,
          newCardCount: newCards.length,
          firstCard: newCards[0]?.name,
          lastCard: newCards[newCards.length - 1]?.name
        });
        
        // Update state with sort change ID to force React re-render
        setState(prevState => ({
          ...prevState,
          sortChangeId,
        }));
      }"""

    if old_sort_complete in content:
        content = content.replace(old_sort_complete, new_sort_complete)
        print("✅ Added nuclear sort update logic")
    else:
        print("❌ Could not find sort complete section")
        return False

    # Also update the clear all filters to reset sort change ID
    old_clear_filters = """    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'subset',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
        // Phase 4B: Enhanced filter clear
        subtypes: [],
        isGoldMode: false,
        sectionStates: {
          colors: true,
          cmc: true,
          types: true,
          subtypes: false,
          sets: false,
          rarity: false,
          stats: false,
        },
      },
    }));"""

    new_clear_filters = """    setState(prev => ({
      ...prev,
      sortChangeId: Date.now(), // Force re-render
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'subset',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
        // Phase 4B: Enhanced filter clear
        subtypes: [],
        isGoldMode: false,
        sectionStates: {
          colors: true,
          cmc: true,
          types: true,
          subtypes: false,
          sets: false,
          rarity: false,
          stats: false,
        },
      },
    }));"""

    if old_clear_filters in content:
        content = content.replace(old_clear_filters, new_clear_filters)
        print("✅ Added sort change ID to clear filters")
    else:
        print("❌ Could not find clear filters section")

    # Write the updated useCards.ts
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Now update MTGOLayout.tsx to use the sort change ID in keys
    filename2 = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename2):
        print(f"Error: {filename2} not found")
        return False
    
    with open(filename2, 'r', encoding='utf-8') as f:
        content2 = f.read()
    
    # Add sortChangeId to destructuring
    old_destructure_end = """    // Phase 4B: Enhanced filter actions
    updateSectionState,
    getSectionState,
    autoExpandSection,} = useCards();"""

    new_destructure_end = """    // Phase 4B: Enhanced filter actions
    updateSectionState,
    getSectionState,
    autoExpandSection,
    // Sort change tracking
    sortChangeId,} = useCards();"""

    if old_destructure_end in content2:
        content2 = content2.replace(old_destructure_end, new_destructure_end)
        print("✅ Added sortChangeId to destructuring")
    else:
        print("❌ Could not find destructuring end")
        return False

    # Update the collection content container key to include sortChangeId
    old_container_key = """            <div key={`collection-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`}>"""

    new_container_key = """            <div key={`collection-${sortChangeId}-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`}>"""

    if old_container_key in content2:
        content2 = content2.replace(old_container_key, new_container_key)
        print("✅ Updated container key with sortChangeId")
    else:
        print("❌ Could not find container key")
        return False

    # Update the debug logging to include sortChangeId
    old_container_debug = """                console.log('🎨 COLLECTION CONTENT CONTAINER RENDER:', {
                  containerKey: `collection-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`,
                  viewMode: layout.viewModes.collection,
                  cardsLength: cards.length,
                  sortedCardsLength: sortedCollectionCards.length
                });"""

    new_container_debug = """                console.log('🎨 COLLECTION CONTENT CONTAINER RENDER:', {
                  containerKey: `collection-${sortChangeId}-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`,
                  sortChangeId: sortChangeId,
                  viewMode: layout.viewModes.collection,
                  cardsLength: cards.length,
                  sortedCardsLength: sortedCollectionCards.length
                });"""

    if old_container_debug in content2:
        content2 = content2.replace(old_container_debug, new_container_debug)
        print("✅ Updated container debug logging")
    else:
        print("❌ Could not find container debug")

    # Write the updated MTGOLayout.tsx
    with open(filename2, 'w', encoding='utf-8') as f:
        f.write(content2)
    
    print(f"✅ Successfully applied nuclear React fix to {filename} and {filename2}")
    return True

if __name__ == "__main__":
    success = nuclear_react_fix()
    sys.exit(0 if success else 1)