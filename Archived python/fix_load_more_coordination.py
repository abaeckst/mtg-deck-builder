#!/usr/bin/env python3
"""
Fix Load More coordination between extracted hooks
Addresses the state coordination issue between usePagination and useSearch
"""

import os
import re

def read_file(filepath):
    """Read file content safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def write_file(filepath, content):
    """Write file content safely"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False

def fix_useSearch_hook():
    """Add Load More coordination to useSearch hook"""
    
    filepath = "src/hooks/useSearch.ts"
    content = read_file(filepath)
    
    if not content:
        return False
    
    # Add loadMoreCards method to useSearch
    load_more_method = '''
  // Load more cards for progressive loading
  const loadMoreCards = useCallback(async (): Promise<ScryfallCard[]> => {
    console.log('🔄 useSearch.loadMoreCards called');
    
    const metadata = state.lastSearchMetadata;
    if (!metadata) {
      console.log('❌ No search metadata available for load more');
      throw new Error('No search metadata available');
    }

    try {
      console.log('📡 Loading more cards via API...');
      
      // Use the existing pagination state to load more
      const currentPaginationState = {
        totalCards: metadata.totalCards,
        loadedCards: metadata.loadedCards,
        hasMore: metadata.loadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(metadata.loadedCards / 75) + 1,
        nextUrl: null, // Will be handled by scryfallApi
        query: metadata.query,
        filters: metadata.filters,
      };

      const { loadMoreResults } = await import('../services/scryfallApi');
      const newCards = await loadMoreResults(currentPaginationState);
      
      console.log('✅ Load more API successful:', {
        newCardsCount: newCards.length,
        previousTotal: state.cards.length
      });

      // Update local state with appended cards
      setState(prev => {
        const updatedCards = [...prev.cards, ...newCards];
        console.log('🔄 Updating useSearch cards state:', {
          previousCount: prev.cards.length,
          newCardsCount: newCards.length,
          finalCount: updatedCards.length
        });
        
        return {
          ...prev,
          cards: updatedCards,
          lastSearchMetadata: prev.lastSearchMetadata ? {
            ...prev.lastSearchMetadata,
            loadedCards: updatedCards.length
          } : null
        };
      });

      // Update pagination through callback
      onPaginationUpdate({
        loadedCards: state.cards.length + newCards.length,
        hasMore: (state.cards.length + newCards.length) < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor((state.cards.length + newCards.length) / 75) + 1,
      });

      return newCards;
      
    } catch (error) {
      console.error('❌ Load more failed in useSearch:', error);
      throw error;
    }
  }, [state.lastSearchMetadata, state.cards.length, onPaginationUpdate]);'''

    # Find the return statement and add loadMoreCards to actions
    return_pattern = r'return \{([^}]+)\};'
    return_match = re.search(return_pattern, content, re.DOTALL)
    
    if return_match:
        # Add loadMoreCards to the return statement
        return_content = return_match.group(1)
        if 'loadMoreCards,' not in return_content:
            # Add loadMoreCards to the actions
            new_return_content = return_content.rstrip() + ',\n    loadMoreCards,'
            new_return = f'return {{\n{new_return_content}\n  }};'
            content = content.replace(return_match.group(0), new_return)
    
    # Add the loadMoreCards method before the return statement
    return_index = content.rfind('  return {')
    if return_index != -1:
        content = content[:return_index] + load_more_method + '\n\n' + content[return_index:]
    
    # Update the SearchActions interface to include loadMoreCards
    interface_pattern = r'export interface SearchActions \{([^}]+)\}'
    interface_match = re.search(interface_pattern, content, re.DOTALL)
    
    if interface_match:
        interface_content = interface_match.group(1)
        if 'loadMoreCards:' not in interface_content:
            new_interface_content = interface_content.rstrip() + '\n  loadMoreCards: () => Promise<ScryfallCard[]>;'
            new_interface = f'export interface SearchActions {{\n{new_interface_content}\n}}'
            content = content.replace(interface_match.group(0), new_interface)
    
    return write_file(filepath, content)

def fix_useCards_coordinator():
    """Fix useCards coordinator to properly coordinate Load More"""
    
    filepath = "src/hooks/useCards.ts"
    content = read_file(filepath)
    
    if not content:
        return False
    
    # Replace the pagination hook initialization with proper coordination
    old_pagination_init = '''  // Pagination hook
  const {
    pagination,
    loadMoreResultsAction: originalLoadMore,
    resetPagination,
    setPaginationState,
    updatePagination,
  } = usePagination({
    cards: [], // Will be updated through coordination
    onCardsUpdate: () => {}, // Will be handled by coordination
    onErrorUpdate: () => {}, // Will be handled by coordination
  });'''

    new_pagination_init = '''  // Pagination hook with proper coordination
  const {
    pagination,
    resetPagination,
    setPaginationState,
    updatePagination,
  } = usePagination();'''

    content = content.replace(old_pagination_init, new_pagination_init)
    
    # Add the coordinated Load More function before the search hook initialization
    coordinated_load_more = '''
  // Coordinated Load More function
  const loadMoreResultsAction = useCallback(async () => {
    console.log('🎯 useCards.loadMoreResultsAction called - coordinating between hooks');
    
    if (!pagination.hasMore || pagination.isLoadingMore) {
      console.log('🚫 Cannot load more:', { 
        hasMore: pagination.hasMore,
        isLoadingMore: pagination.isLoadingMore
      });
      return;
    }

    console.log('🔄 Setting loading state...');
    updatePagination({ isLoadingMore: true });

    try {
      // This will be populated after useSearch is initialized
      console.log('📡 Calling search hook loadMoreCards...');
      // Note: searchHookLoadMore will be defined after useSearch initialization
    } catch (error) {
      console.error('❌ Load more coordination failed:', error);
      updatePagination({ isLoadingMore: false });
    }
  }, [pagination.hasMore, pagination.isLoadingMore, updatePagination]);
'''

    # Find where the search hook is initialized and add the coordinated function before it
    search_hook_pattern = r'  // Search hook with coordination callbacks'
    search_hook_index = content.find(search_hook_pattern)
    
    if search_hook_index != -1:
        content = content[:search_hook_index] + coordinated_load_more + '\n' + content[search_hook_index:]
    
    # Update the search hook initialization to include loadMoreCards
    old_search_init = '''  // Search hook with coordination callbacks
  const {
    cards,
    loading,
    error,
    searchQuery,
    totalCards,
    lastSearchMetadata,
    isResorting,
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards,
    loadRandomCard,
    clearCards: clearCardsSearch,
    handleCollectionSortChange,
  } = useSearch({
    activeFilters,
    hasActiveFilters,
    onPaginationStateChange: setPaginationState,
    onPaginationUpdate: updatePagination,
    resetPagination,
    addToSearchHistory,
  });'''

    new_search_init = '''  // Search hook with coordination callbacks
  const {
    cards,
    loading,
    error,
    searchQuery,
    totalCards,
    lastSearchMetadata,
    isResorting,
    searchForCards,
    searchWithAllFilters,
    enhancedSearch,
    loadPopularCards,
    loadRandomCard,
    clearCards: clearCardsSearch,
    handleCollectionSortChange,
    loadMoreCards: searchHookLoadMore,
  } = useSearch({
    activeFilters,
    hasActiveFilters,
    onPaginationStateChange: setPaginationState,
    onPaginationUpdate: updatePagination,
    resetPagination,
    addToSearchHistory,
  });

  // Complete the coordinated Load More function now that we have searchHookLoadMore
  const coordinatedLoadMore = useCallback(async () => {
    console.log('🎯 useCards coordinated Load More executing');
    
    if (!pagination.hasMore || pagination.isLoadingMore) {
      console.log('🚫 Cannot load more:', { 
        hasMore: pagination.hasMore,
        isLoadingMore: pagination.isLoadingMore
      });
      return;
    }

    console.log('🔄 Setting loading state...');
    updatePagination({ isLoadingMore: true });

    try {
      console.log('📡 Calling search hook loadMoreCards...');
      await searchHookLoadMore();
      console.log('✅ Coordinated Load More successful');
    } catch (error) {
      console.error('❌ Coordinated Load More failed:', error);
      updatePagination({ isLoadingMore: false });
    }
  }, [pagination.hasMore, pagination.isLoadingMore, updatePagination, searchHookLoadMore]);'''

    content = content.replace(old_search_init, new_search_init)
    
    # Update the return statement to use coordinatedLoadMore instead of originalLoadMore
    old_return_action = 'loadMoreResultsAction: originalLoadMore,'
    new_return_action = 'loadMoreResultsAction: coordinatedLoadMore,'
    
    content = content.replace(old_return_action, new_return_action)
    
    return write_file(filepath, content)

def fix_usePagination_hook():
    """Simplify usePagination to focus only on state management"""
    
    filepath = "src/hooks/usePagination.ts"
    content = read_file(filepath)
    
    if not content:
        return False
    
    # Create simplified usePagination that only manages state
    new_content = '''// src/hooks/usePagination.ts - Simplified state management for progressive loading
import { useState, useCallback } from 'react';
import { PaginatedSearchState } from '../types/card';

export interface PaginationState {
  pagination: {
    totalCards: number;
    loadedCards: number;
    hasMore: boolean;
    isLoadingMore: boolean;
    currentPage: number;
  };
}

export interface PaginationActions {
  resetPagination: () => void;
  setPaginationState: (state: PaginatedSearchState | null) => void;
  updatePagination: (update: Partial<PaginationState['pagination']>) => void;
}

export const usePagination = (): PaginationState & PaginationActions => {
  // Internal pagination state for progressive loading
  const [paginationState, setPaginationState] = useState<PaginatedSearchState | null>(null);
  
  const [pagination, setPagination] = useState({
    totalCards: 0,
    loadedCards: 0,
    hasMore: false,
    isLoadingMore: false,
    currentPage: 1,
  });

  // Reset pagination state
  const resetPagination = useCallback(() => {
    console.log('🔄 usePagination.resetPagination called');
    setPaginationState(null);
    setPagination({
      totalCards: 0,
      loadedCards: 0,
      hasMore: false,
      isLoadingMore: false,
      currentPage: 1,
    });
  }, []);

  // Update pagination state
  const updatePagination = useCallback((update: Partial<typeof pagination>) => {
    console.log('🔄 usePagination.updatePagination called:', update);
    setPagination(prev => ({ ...prev, ...update }));
  }, []);

  // Set pagination state for Load More functionality
  const setPaginationStateCallback = useCallback((state: PaginatedSearchState | null) => {
    console.log('🔄 usePagination.setPaginationState called:', state ? 'with state' : 'null');
    setPaginationState(state);
  }, []);

  return {
    pagination,
    resetPagination,
    setPaginationState: setPaginationStateCallback,
    updatePagination,
  };
};'''

    return write_file(filepath, content.replace(content, new_content))

def main():
    """Execute all fixes for Load More coordination"""
    print("🚀 Fixing Load More coordination between extracted hooks...")
    print()
    
    # Verify we're in the right directory
    if not os.path.exists("src/hooks"):
        print("❌ Error: Not in project root directory. Please run from C:\\Users\\carol\\mtg-deck-builder")
        return False
    
    success = True
    
    # Fix 1: Add loadMoreCards method to useSearch
    print("1️⃣ Adding loadMoreCards method to useSearch hook...")
    if fix_useSearch_hook():
        print("   ✅ useSearch hook updated successfully")
    else:
        print("   ❌ Failed to update useSearch hook")
        success = False
    
    print()
    
    # Fix 2: Simplify usePagination to only manage state
    print("2️⃣ Simplifying usePagination hook...")
    if fix_usePagination_hook():
        print("   ✅ usePagination hook updated successfully")
    else:
        print("   ❌ Failed to update usePagination hook")
        success = False
    
    print()
    
    # Fix 3: Fix useCards coordinator to properly coordinate Load More
    print("3️⃣ Fixing useCards coordinator...")
    if fix_useCards_coordinator():
        print("   ✅ useCards coordinator updated successfully")
    else:
        print("   ❌ Failed to update useCards coordinator")
        success = False
    
    print()
    
    if success:
        print("🎉 All Load More coordination fixes applied successfully!")
        print()
        print("📋 Summary of changes:")
        print("   • useSearch: Added loadMoreCards method that handles API calls and state updates")
        print("   • usePagination: Simplified to only manage pagination state")
        print("   • useCards: Added proper coordination between pagination and search hooks")
        print()
        print("🧪 Next steps:")
        print("   1. Run 'npm start' to verify TypeScript compilation")
        print("   2. Test Load More button functionality")
        print("   3. Verify no regressions in other features")
    else:
        print("❌ Some fixes failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main()'''