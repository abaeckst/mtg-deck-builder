#!/usr/bin/env python3

import os
import sys

def update_cards_hook_enhanced_filters(filename):
    """Update useCards.ts with enhanced filter state for Phase 4B"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements with exact string matching
    updates = [
        # 1. Add enhanced filter state structure
        (
            """  // Enhanced filtering state
  activeFilters: {
    format: string;
    colors: string[];
    colorIdentity: 'exact' | 'subset' | 'include';
    types: string[];
    rarity: string[];
    sets: string[];
    cmc: { min: number | null; max: number | null };
    power: { min: number | null; max: number | null };
    toughness: { min: number | null; max: number | null };
  };""",
            """  // Enhanced filtering state
  activeFilters: {
    format: string;
    colors: string[];
    colorIdentity: 'exact' | 'subset' | 'include';
    types: string[];
    rarity: string[];
    sets: string[];
    cmc: { min: number | null; max: number | null };
    power: { min: number | null; max: number | null };
    toughness: { min: number | null; max: number | null };
    // Phase 4B: Enhanced filter state
    subtypes: string[];
    isGoldMode: boolean;
    sectionStates: {
      colors: boolean;
      cmc: boolean;
      types: boolean;
      subtypes: boolean;
      sets: boolean;
      rarity: boolean;
      stats: boolean;
    };
  };""",
            "Enhanced filter state interface"
        ),
        
        # 2. Initialize enhanced filter state in useState
        (
            """    // Enhanced filtering state
    activeFilters: {
      format: 'custom-standard',
      colors: [],
      colorIdentity: 'exact',
      types: [],
      rarity: [],
      sets: [],
      cmc: { min: null, max: null },
      power: { min: null, max: null },
      toughness: { min: null, max: null },
    },""",
            """    // Enhanced filtering state
    activeFilters: {
      format: 'custom-standard',
      colors: [],
      colorIdentity: 'exact',
      types: [],
      rarity: [],
      sets: [],
      cmc: { min: null, max: null },
      power: { min: null, max: null },
      toughness: { min: null, max: null },
      // Phase 4B: Enhanced filter state initialization
      subtypes: [],
      isGoldMode: false,
      sectionStates: {
        colors: true,      // Default sections expanded
        cmc: true,
        types: true,
        subtypes: true,
        sets: false,       // Advanced sections collapsed
        rarity: false,
        stats: false,
      },
    },""",
            "Enhanced filter state initialization"
        ),
        
        # 3. Update clearCards filter reset
        (
            """      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },""",
            """      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
        // Phase 4B: Enhanced filter reset
        subtypes: [],
        isGoldMode: false,
        sectionStates: {
          colors: true,
          cmc: true,
          types: true,
          subtypes: true,
          sets: false,
          rarity: false,
          stats: false,
        },
      },""",
            "Enhanced filter reset in clearCards"
        ),
        
        # 4. Update clearAllFilters function
        (
            """  const clearAllFilters = useCallback(() => {
    console.log('🧹 Clearing all filters and resetting search');
    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
    }));""",
            """  const clearAllFilters = useCallback(() => {
    console.log('🧹 Clearing all filters and resetting search');
    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
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
          subtypes: true,
          sets: false,
          rarity: false,
          stats: false,
        },
      },
    }));""",
            "Enhanced filter clear in clearAllFilters"
        ),
        
        # 5. Update hasActiveFilters function
        (
            """  const hasActiveFilters = useCallback((): boolean => {
    const filters = state.activeFilters;
    return (
      filters.format !== '' ||
      filters.colors.length > 0 ||
      filters.types.length > 0 ||
      filters.rarity.length > 0 ||
      filters.sets.length > 0 ||
      filters.cmc.min !== null ||
      filters.cmc.max !== null ||
      filters.power.min !== null ||
      filters.power.max !== null ||
      filters.toughness.min !== null ||
      filters.toughness.max !== null
    );
  }, [state.activeFilters]);""",
            """  const hasActiveFilters = useCallback((): boolean => {
    const filters = state.activeFilters;
    return (
      filters.format !== '' ||
      filters.colors.length > 0 ||
      filters.types.length > 0 ||
      filters.rarity.length > 0 ||
      filters.sets.length > 0 ||
      filters.cmc.min !== null ||
      filters.cmc.max !== null ||
      filters.power.min !== null ||
      filters.power.max !== null ||
      filters.toughness.min !== null ||
      filters.toughness.max !== null ||
      // Phase 4B: Enhanced filter detection
      filters.subtypes.length > 0 ||
      filters.isGoldMode
    );
  }, [state.activeFilters]);""",
            "Enhanced filter detection in hasActiveFilters"
        ),
        
        # 6. Add section state management functions
        (
            """  // Enhanced search function that uses all active filters with pagination
  const searchWithAllFilters = useCallback(async (query: string, filtersOverride?: any) => {""",
            """  // Phase 4B: Section state management functions
  const updateSectionState = useCallback((section: string, isExpanded: boolean) => {
    setState(prev => ({
      ...prev,
      activeFilters: {
        ...prev.activeFilters,
        sectionStates: {
          ...prev.activeFilters.sectionStates,
          [section]: isExpanded,
        },
      },
    }));
  }, []);

  const getSectionState = useCallback((section: string): boolean => {
    return state.activeFilters.sectionStates[section as keyof typeof state.activeFilters.sectionStates] ?? true;
  }, [state.activeFilters.sectionStates]);

  const autoExpandSection = useCallback((section: string) => {
    // Auto-expand sections that have active filters
    const filters = state.activeFilters;
    let shouldExpand = false;
    
    switch (section) {
      case 'colors':
        shouldExpand = filters.colors.length > 0 || filters.isGoldMode;
        break;
      case 'types':
        shouldExpand = filters.types.length > 0;
        break;
      case 'subtypes':
        shouldExpand = filters.subtypes.length > 0;
        break;
      case 'rarity':
        shouldExpand = filters.rarity.length > 0;
        break;
      case 'stats':
        shouldExpand = filters.power.min !== null || filters.power.max !== null || 
                     filters.toughness.min !== null || filters.toughness.max !== null;
        break;
      case 'cmc':
        shouldExpand = filters.cmc.min !== null || filters.cmc.max !== null;
        break;
      case 'sets':
        shouldExpand = filters.sets.length > 0;
        break;
    }
    
    if (shouldExpand && !getSectionState(section)) {
      updateSectionState(section, true);
    }
  }, [state.activeFilters, getSectionState, updateSectionState]);

  // Enhanced search function that uses all active filters with pagination
  const searchWithAllFilters = useCallback(async (query: string, filtersOverride?: any) => {""",
            "Section state management functions"
        ),
        
        # 7. Add enhanced actions to return object
        (
            """    enhancedSearch,
    getSearchSuggestions: getSearchSuggestionsFunc,
    clearSearchSuggestions,
    addToSearchHistory,
    handleCollectionSortChange,
    loadMoreResultsAction,
    resetPagination,""",
            """    enhancedSearch,
    getSearchSuggestions: getSearchSuggestionsFunc,
    clearSearchSuggestions,
    addToSearchHistory,
    handleCollectionSortChange,
    loadMoreResultsAction,
    resetPagination,
    // Phase 4B: Enhanced filter actions
    updateSectionState,
    getSectionState,
    autoExpandSection,""",
            "Enhanced filter actions export"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_cards_hook_enhanced_filters("src/hooks/useCards.ts")
    sys.exit(0 if success else 1)
