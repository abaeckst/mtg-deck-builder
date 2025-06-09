// src/services/scryfallApi.ts - Enhanced with progressive loading and 60-card batches
import { ScryfallCard, ScryfallSearchResponse, PaginatedSearchState } from '../types/card';
// DEBUGGING HELPER: Copy this function to browser console for easy output capture



const SCRYFALL_API_BASE = 'https://api.scryfall.com';
const REQUEST_DELAY = 100; // 100ms delay between requests to respect rate limiting
const INITIAL_PAGE_SIZE = 75; // Initial results limited to 75 cards

// Simple delay function for rate limiting
const delay = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

// Rate limiting implementation
let lastRequestTime = 0;

const rateLimitedFetch = async (url: string): Promise<Response> => {
  console.time("⏱️ API_REQUEST_TIME");
  const now = Date.now();
  const timeSinceLastRequest = now - lastRequestTime;
  
  if (timeSinceLastRequest < REQUEST_DELAY) {
    await delay(REQUEST_DELAY - timeSinceLastRequest);
  }
  
  lastRequestTime = Date.now();
  
  const response = await fetch(url, {
    headers: {
      'Accept': 'application/json',
      'User-Agent': 'MTGDeckBuilder/1.0',
    },
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  console.timeEnd("⏱️ API_REQUEST_TIME");

  
  return response;
};

;

/**
 * Advanced search with filters and enhanced sort support
 */
export interface SearchFilters {
  format?: string;
  colors?: string[];
  colorIdentity?: 'exact' | 'subset' | 'include';
  types?: string[];
  rarity?: string[];
  sets?: string[];
  cmc?: { min?: number; max?: number };
  power?: { min?: number; max?: number };
  toughness?: { min?: number; max?: number };
  keywords?: string[];
  artist?: string;
  price?: { min?: number; max?: number };
  // Phase 4B: Enhanced filter types
  subtypes?: string[];
  isGoldMode?: boolean;
}

/**
 * Build enhanced search query with operator support
 */
function buildEnhancedSearchQuery(query: string): string {
  console.time("⏱️ QUERY_BUILDING_TIME");
  // FIXED: Scryfall-compatible multi-word search syntax
  console.log('🔍 Building enhanced query for:', query);
  console.log('🔍 INPUT ANALYSIS:', {
    originalQuery: query,
    hasQuotes: query.includes('"'),
    hasDashes: query.includes('-'),
    hasColons: query.includes(':'),
    wordCount: query.trim().split(/\s+/).length
  });
  
  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    const words = query.trim().split(/\s+/);
    
    if (words.length > 1) {
      // Multi-word query: Each word should match name, oracle text, OR type
      // Format: (name:word1 OR o:word1 OR type:word1) (name:word2 OR o:word2 OR type:word2)
      console.log('🔍 Multi-word query detected, using comprehensive field search:', query);
      const wordQueries = words.map(word => `(name:${word} OR o:${word} OR type:${word})`);
      const result = wordQueries.join(' ');
      console.log('🔍 Multi-word result:', result);
      return result;
    } else {
      // Single word: search across multiple fields
      const result = `(name:${query} OR o:${query} OR type:${query})`;
      console.log('🔍 Single word query, using field search:', result);
      return result;
    }
  }
  
  // Advanced parsing for queries with explicit operators
  const parts: string[] = [];
  let workingQuery = query;
  
  // Handle quoted phrases (user explicitly wants exact match)
  const quotedPhrases = query.match(/"[^"]+"/g) || [];
  quotedPhrases.forEach(phrase => {
    parts.push(phrase);
    workingQuery = workingQuery.replace(phrase, '');
  });
  
  // Handle exclusions
  const exclusions = workingQuery.match(/-"[^"]+"|--?[\w\s]+/g) || [];
  exclusions.forEach(exclusion => {
    parts.push(exclusion);
    workingQuery = workingQuery.replace(exclusion, '');
  });
  
  // Handle field-specific searches - QUOTE multi-word values
  const fieldSearches = workingQuery.match(/(name|text|type|oracle):"[^"]+"|(?:name|text|type|oracle):[\w\s]+(?=\s|$)/g) || [];
  fieldSearches.forEach(fieldSearch => {
    const colonIndex = fieldSearch.indexOf(':');
    const field = fieldSearch.substring(0, colonIndex);
    const value = fieldSearch.substring(colonIndex + 1);
    
    // If multi-word field value, add quotes
    const processedValue = value.includes(' ') && !value.startsWith('"') ? `"${value}"` : value;
    
    if (field === 'text') {
      parts.push(`o:${processedValue}`);
    } else {
      parts.push(`${field}:${processedValue}`);
    }
    workingQuery = workingQuery.replace(fieldSearch, '');
  });
  
  // Handle remaining terms - use simple syntax for multi-word
  const remainingTerms = workingQuery.trim().split(/\s+/).filter(term => term.length > 0);
  if (remainingTerms.length > 0) {
    const fullTextSearch = remainingTerms.join(' ');
    
    if (parts.length > 0) {
      // If we have other operators, add as simple search
      parts.push(fullTextSearch);
    } else {
      // Simple search without field restrictions
      parts.push(fullTextSearch);
    }
  }
  
  const result = parts.join(' ').trim() || query;
  console.log('🔍 ENHANCED QUERY RESULT:', {
    originalInput: query,
    processedOutput: result,
    parts: parts,
    isMultiWord: query.trim().split(/\s+/).length > 1,
    hasOperators: query.includes('"') || query.includes('-') || query.includes(':')
  });
  console.timeEnd("⏱️ QUERY_BUILDING_TIME");
  return result;
}

/**
 * Search for cards using Scryfall's search API with enhanced sort support
 */
export const searchCards = async (
  query: string,
  page = 1,
  unique = 'cards',
  order = 'name',
  dir: 'asc' | 'desc' = 'asc'
): Promise<ScryfallSearchResponse> => {
  try {
    console.time("⏱️ TOTAL_SEARCH_TIME");
    console.log("🔍 Search started:", { query, order, dir });
    // Handle empty queries - Scryfall doesn't accept empty q parameter
    if (!query || query.trim() === '') {
      throw new Error('Search query cannot be empty');
    }
    
    const params = new URLSearchParams({
      q: query.trim(),
      page: page.toString(),
      unique,
      order,
      dir,
    });
    
    const url = `${SCRYFALL_API_BASE}/cards/search?${params.toString()}`;
    
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
    console.time("⏱️ JSON_PARSING_TIME");

    const data = await response.json();

    console.timeEnd("⏱️ JSON_PARSING_TIME");
    
    console.log('🌐 ===== SCRYFALL API RESPONSE ANALYSIS =====');
    console.log('🌐 RESPONSE STATUS:', response.status);
    console.log('🌐 TOTAL CARDS:', data.total_cards);
    console.log('🌐 RETURNED COUNT:', data.data?.length || 0);
    console.log('🌐 HAS MORE:', data.has_more);
    
    // ULTRA-SIMPLE card name debugging
    if (data.data && data.data.length > 0) {
      console.log('🌐 CARD 1 NAME:', data.data[0].name);
      if (data.data.length > 1) console.log('🌐 CARD 2 NAME:', data.data[1].name);
      if (data.data.length > 2) console.log('🌐 CARD 3 NAME:', data.data[2].name);
      
      console.log('🌐 SORT VERIFICATION SIMPLE:', {
        direction: dir,
        expectedOrder: dir === 'asc' ? 'A→Z' : 'Z→A',
        card1: data.data[0].name,
        card2: data.data[1]?.name || 'N/A',
        card3: data.data[2]?.name || 'N/A'
      });
      
      // Simple A-Z verification
      if (data.data.length >= 2) {
        const isAscending = data.data[0].name <= data.data[1].name;
        const expectedAscending = dir === 'asc';
        console.log('🌐 SORT ORDER CHECK:', {
          actuallyAscending: isAscending,
          shouldBeAscending: expectedAscending,
          isCorrect: isAscending === expectedAscending
        });
      }
    } else {
      console.log('🌐 NO CARDS IN RESPONSE');
    }
    console.log('🌐 ===== API RESPONSE COMPLETE =====');
    
    console.timeEnd("⏱️ TOTAL_SEARCH_TIME");

    
    console.log("✅ Search completed successfully");

    
    return data as ScryfallSearchResponse;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to search cards: ${error.message}`);
    } else {
      throw new Error('Failed to search cards: Unknown error');
    }
  }
};

/**
 * Enhanced search with sorting parameters
 */
export const searchCardsWithSort = async (
  query: string,
  options: {
    page?: number;
    unique?: string;
    order?: string;
    dir?: 'asc' | 'desc';
  } = {}
): Promise<ScryfallSearchResponse> => {
  const {
    page = 1,
    unique = 'cards',
    order = 'name',
    dir = 'asc'
  } = options;
  
  return searchCards(query, page, unique, order, dir);
};

export const searchCardsWithFilters = async (
  query: string,
  filters: SearchFilters = {},
  page = 1,
  order = 'name',
  dir: 'asc' | 'desc' = 'asc'
): Promise<ScryfallSearchResponse> => {
  // Start with base query - ensure we never have empty query
  let searchQuery = query || '*';
  
  console.log('🔧 SEARCH FILTERS INPUT:', { 
    baseQuery: query, 
    filters: JSON.stringify(filters, null, 2),
    sort: { order, dir },
    formatFilter: filters.format,
    hasFormatFilter: !!filters.format && filters.format.trim() !== ''
  });
  
  // Add format filter with proper Scryfall syntax
  if (filters.format && filters.format.trim() !== '') {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Use standard format (Final Fantasy set is standard-legal)
      searchQuery += ` legal:standard`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }
  
  // Phase 4B: Enhanced color and gold mode filtering
  if (filters.isGoldMode && filters.colors && filters.colors.length > 0) {
    // Gold mode: multicolor cards containing selected colors
    const colorQuery = filters.colors.join('');
    searchQuery += ` color>=2 color:${colorQuery}`;
  } else if (filters.isGoldMode && (!filters.colors || filters.colors.length === 0)) {
    // Gold mode with no specific colors: just multicolor
    searchQuery += ` color>=2`;
  } else if (filters.colors && filters.colors.length > 0) {
    // Standard color filtering (no gold mode)
    // Handle colorless separately
    if (filters.colors.includes('C')) {
      // If colorless is selected with other colors, handle as multicolor search
      if (filters.colors.length > 1) {
        const otherColors = filters.colors.filter(c => c !== 'C').join('');
        const colorMode = filters.colorIdentity || 'exact';
        
        switch (colorMode) {
          case 'exact':
            // For exact with colorless + colors, search for colorless OR exact colors
            if (otherColors) {
              searchQuery += ` (identity=C OR identity=${otherColors})`;
            } else {
              searchQuery += ` identity=C`;
            }
            break;
          case 'subset':
            searchQuery += ` identity<=${otherColors}C`;
            break;
          case 'include':
          default:
            searchQuery += ` (identity:C OR identity:${otherColors})`;
            break;
        }
      } else {
        // Only colorless selected
        searchQuery += ` identity=C`;
      }
    } else {
      // No colorless, handle normally
      const colorQuery = filters.colors.join('');
      const colorMode = filters.colorIdentity || 'exact';
      
      switch (colorMode) {
        case 'exact':
          searchQuery += ` identity=${colorQuery}`;
          break;
        case 'subset':
          searchQuery += ` identity<=${colorQuery}`;
          break;
        case 'include':
        default:
          searchQuery += ` identity:${colorQuery}`;
          break;
      }
    }
  }
  
  // Add type filters
  if (filters.types && filters.types.length > 0) {
    const typeQuery = filters.types.map(type => `type:${type}`).join(' OR ');
    searchQuery += ` (${typeQuery})`;
  }
  
  // Phase 4B: Add subtype filters
  if (filters.subtypes && filters.subtypes.length > 0) {
    const subtypeQuery = filters.subtypes.map(subtype => `type:${subtype}`).join(' OR ');
    searchQuery += ` (${subtypeQuery})`;
  }
  
  // Add rarity filter
  if (filters.rarity && filters.rarity.length > 0) {
    const rarityQuery = filters.rarity.map(r => `rarity:${r}`).join(' OR ');
    searchQuery += ` (${rarityQuery})`;
  }
  
  // Add set filters (multiple sets support)
  if (filters.sets && filters.sets.length > 0) {
    if (filters.sets.length === 1) {
      searchQuery += ` set:${filters.sets[0]}`;
    } else {
      const setQuery = filters.sets.map(set => `set:${set}`).join(' OR ');
      searchQuery += ` (${setQuery})`;
    }
  }

  // Add CMC filter
  if (filters.cmc) {
    if (filters.cmc.min !== undefined && filters.cmc.min !== null) {
      searchQuery += ` cmc>=${filters.cmc.min}`;
    }
    if (filters.cmc.max !== undefined && filters.cmc.max !== null) {
      searchQuery += ` cmc<=${filters.cmc.max}`;
    }
  }
  
  // Add power filter
  if (filters.power) {
    if (filters.power.min !== undefined && filters.power.min !== null) {
      searchQuery += ` power>=${filters.power.min}`;
    }
    if (filters.power.max !== undefined && filters.power.max !== null) {
      searchQuery += ` power<=${filters.power.max}`;
    }
  }
  
  // Add toughness filter
  if (filters.toughness) {
    if (filters.toughness.min !== undefined && filters.toughness.min !== null) {
      searchQuery += ` toughness>=${filters.toughness.min}`;
    }
    if (filters.toughness.max !== undefined && filters.toughness.max !== null) {
      searchQuery += ` toughness<=${filters.toughness.max}`;
    }
  }
  
  // Helper function to check if a filter is actually active
  const isFilterActive = (key: keyof SearchFilters, value: any): boolean => {
    switch (key) {
      case 'format':
        return typeof value === 'string' && value.trim() !== '';
      case 'colors':
      case 'types':
      case 'rarity':
      case 'sets':
      case 'keywords':
      case 'subtypes':
        return Array.isArray(value) && value.length > 0;
      case 'colorIdentity':
        return typeof value === 'string' && value !== 'exact'; // 'exact' is default
      case 'isGoldMode':
        return typeof value === 'boolean' && value === true;
      case 'cmc':
      case 'power':
      case 'toughness':
      case 'price':
        return value && typeof value === 'object' && (
          (typeof value.min === 'number' && !isNaN(value.min)) ||
          (typeof value.max === 'number' && !isNaN(value.max))
        );
      case 'artist':
        return typeof value === 'string' && value.trim() !== '';
      default:
        return false;
    }
  };
  
  const activeFilters = (Object.keys(filters) as (keyof SearchFilters)[])
    .filter(key => isFilterActive(key, filters[key]));
  
  // Create type-safe filter details for debugging
  const filterDetails: Record<string, any> = {};
  activeFilters.forEach(key => {
    filterDetails[key] = filters[key];
  });
  
  console.log('🔧 FINAL SEARCH QUERY:', { 
    step1_originalQuery: query, 
    step2_finalQuery: searchQuery.trim(),
    step3_activeFilters: activeFilters,
    step4_filterDetails: JSON.stringify(filterDetails, null, 2),
    step5_willCallSearchCardsWithSort: true
  });
  
  return searchCardsWithSort(searchQuery.trim(), { page, order, dir });
};

/**
 * Search with pagination support - returns only first 75 cards initially
 */
export const searchCardsWithPagination = async (
  query: string,
  filters: SearchFilters = {},
  order = 'cmc',
  dir: 'asc' | 'desc' = 'asc'
): Promise<PaginatedSearchState> => {
  try {
    console.log('🔍 Initial paginated search:', { query, filters, sort: { order, dir }, pageSize: INITIAL_PAGE_SIZE });
    
    // Get first page with 75-card limit - FIXED: Use enhanced search
    const response = await enhancedSearchCards(query, filters, 1, order, dir);
    
    // Limit initial results to 75 cards
    const initialResults = response.data.slice(0, INITIAL_PAGE_SIZE);
    const hasMore = response.has_more || response.data.length > INITIAL_PAGE_SIZE;
    
    console.log('✅ Initial paginated results:', {
      totalAvailable: response.total_cards,
      initialLoaded: initialResults.length,
      hasMore,
      remainingApprox: response.total_cards - initialResults.length
    });
    
    return {
      initialResults,
      totalCards: response.total_cards,
      loadedCards: initialResults.length,
      hasMore,
      isLoadingMore: false,
      currentPage: 1,
      lastQuery: query,
      lastFilters: filters,
      lastSort: { order, dir },
      // Partial page consumption tracking
      currentScryfallPage: 1,
      cardsConsumedFromCurrentPage: initialResults.length,
      currentPageCards: response.data,
      scryfallPageSize: 175,
      displayBatchSize: 75,
    };
  } catch (error) {
    console.error('❌ Paginated search failed:', error);
    throw error;
  }
};

/**
 * Load more results progressively (next 175 cards)
 */
export const loadMoreResults = async (
  paginationState: PaginatedSearchState,
  onProgress?: (loaded: number, total: number) => void
): Promise<ScryfallCard[]> => {
  try {
    console.log('🔄 Load More with partial page consumption:', { 
      currentScryfallPage: paginationState.currentScryfallPage,
      cardsConsumedFromCurrentPage: paginationState.cardsConsumedFromCurrentPage,
      currentPageCards: paginationState.currentPageCards?.length || 0,
      loadedSoFar: paginationState.loadedCards,
      totalCards: paginationState.totalCards,
      scryfallPageSize: paginationState.scryfallPageSize || 175,
      displayBatchSize: paginationState.displayBatchSize || 75
    });
    
    // Report progress start
    if (onProgress) {
      onProgress(paginationState.loadedCards, paginationState.totalCards);
    }
    
    const scryfallPageSize = paginationState.scryfallPageSize || 175;
    const displayBatchSize = paginationState.displayBatchSize || 75;
    const cardsConsumed = paginationState.cardsConsumedFromCurrentPage || 0;
    const currentPageCards = paginationState.currentPageCards || [];
    
    // Check if current Scryfall page has remaining cards
    const remainingInCurrentPage = currentPageCards.length - cardsConsumed;
    
    console.log('📊 Partial page analysis:', {
      currentPageTotalCards: currentPageCards.length,
      cardsAlreadyConsumed: cardsConsumed,
      remainingInCurrentPage,
      needsNewPage: remainingInCurrentPage <= 0
    });
    
    let newCards: ScryfallCard[];
    
    if (remainingInCurrentPage > 0) {
      // Return remaining cards from current page
      const cardsToReturn = Math.min(remainingInCurrentPage, displayBatchSize);
      newCards = currentPageCards.slice(cardsConsumed, cardsConsumed + cardsToReturn);
      
      console.log('📄 Returning remaining cards from current page:', {
        cardsToReturn,
        sliceStart: cardsConsumed,
        sliceEnd: cardsConsumed + cardsToReturn,
        remainingAfterThis: remainingInCurrentPage - cardsToReturn
      });
      
    } else {
      // Current page exhausted - fetch next Scryfall page
      const nextScryfallPage = paginationState.currentScryfallPage + 1;
      
      console.log('🌐 Fetching next Scryfall page:', {
        currentPage: paginationState.currentScryfallPage,
        nextPage: nextScryfallPage,
        reason: 'Current page exhausted'
      });
      
      const response = await enhancedSearchCards(
        paginationState.lastQuery,
        paginationState.lastFilters,
        nextScryfallPage,
        paginationState.lastSort.order,
        paginationState.lastSort.dir
      );
      
      // Return first batch from new page
      const cardsToReturn = Math.min(response.data.length, displayBatchSize);
      newCards = response.data.slice(0, cardsToReturn);
      
      console.log('🌐 New page fetched:', {
        newPageCards: response.data.length,
        cardsToReturn,
        hasMorePages: response.has_more
      });
    }
    
    console.log('✅ Load more batch complete:', {
      batchLoaded: newCards.length,
      totalLoadedNow: paginationState.loadedCards + newCards.length,
      alphabeticalSequence: newCards.length > 0 ? `${newCards[0].name} → ${newCards[newCards.length - 1].name}` : 'No cards'
    });
    
    // Report progress completion
    if (onProgress) {
      onProgress(paginationState.loadedCards + newCards.length, paginationState.totalCards);
    }
    
    return newCards;
  } catch (error) {
    console.error('❌ Load more results failed:', error);
    throw error;
  }
};

/**
 * Get a random card from Scryfall
 */
export const getRandomCard = async (): Promise<ScryfallCard> => {
  try {
    const url = `${SCRYFALL_API_BASE}/cards/random`;
    const response = await rateLimitedFetch(url);
    console.time("⏱️ JSON_PARSING_TIME");

    const data = await response.json();

    console.timeEnd("⏱️ JSON_PARSING_TIME");
    
    return data as ScryfallCard;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to get random card: ${error.message}`);
    } else {
      throw new Error('Failed to get random card: Unknown error');
    }
  }
};

/**
 * Get a specific card by ID
 */
export const getCardById = async (id: string): Promise<ScryfallCard> => {
  try {
    const url = `${SCRYFALL_API_BASE}/cards/${id}`;
    const response = await rateLimitedFetch(url);
    console.time("⏱️ JSON_PARSING_TIME");

    const data = await response.json();

    console.timeEnd("⏱️ JSON_PARSING_TIME");
    
    return data as ScryfallCard;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to get card by ID: ${error.message}`);
    } else {
      throw new Error('Failed to get card by ID: Unknown error');
    }
  }
};

/**
 * Get a card by name (exact match)
 */
export const getCardByName = async (name: string): Promise<ScryfallCard> => {
  try {
    const params = new URLSearchParams({
      exact: name,
    });
    
    const url = `${SCRYFALL_API_BASE}/cards/named?${params.toString()}`;
    const response = await rateLimitedFetch(url);
    console.time("⏱️ JSON_PARSING_TIME");

    const data = await response.json();

    console.timeEnd("⏱️ JSON_PARSING_TIME");
    
    return data as ScryfallCard;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to get card by name: ${error.message}`);
    } else {
      throw new Error('Failed to get card by name: Unknown error');
    }
  }
};

/**
 * Autocomplete card names
 */
export const autocompleteCardNames = async (query: string): Promise<string[]> => {
  try {
    const params = new URLSearchParams({
      q: query,
    });
    
    const url = `${SCRYFALL_API_BASE}/cards/autocomplete?${params.toString()}`;
    const response = await rateLimitedFetch(url);
    console.time("⏱️ JSON_PARSING_TIME");

    const data = await response.json();

    console.timeEnd("⏱️ JSON_PARSING_TIME");
    
    return data.data || [];
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to autocomplete: ${error.message}`);
    } else {
      throw new Error('Failed to autocomplete: Unknown error');
    }
  }
};

/**
 * Get all sets from Scryfall
 */
export const getSets = async (): Promise<any[]> => {
  try {
    const url = `${SCRYFALL_API_BASE}/sets`;
    const response = await rateLimitedFetch(url);
    console.time("⏱️ JSON_PARSING_TIME");

    const data = await response.json();

    console.timeEnd("⏱️ JSON_PARSING_TIME");
    
    return data.data || [];
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to get sets: ${error.message}`);
    } else {
      throw new Error('Failed to get sets: Unknown error');
    }
  }
};

/**
 * Enhanced search with full-text capabilities and operator support
 */
export const enhancedSearchCards = async (
  query: string,
  filters: SearchFilters = {},
  page = 1,
  order = 'cmc',
  dir: 'asc' | 'desc' = 'asc'
): Promise<ScryfallSearchResponse> => {
  // Handle empty queries
  if (!query || query.trim() === '') {
    // If we have filters, use wildcard search
    if (Object.keys(filters).length > 0) {
      return searchCardsWithFilters('*', filters, page, order, dir);
    }
    throw new Error('Search query cannot be empty');
  }
  

  
  // Build enhanced query for full-text search
  const searchQuery = buildEnhancedSearchQuery(query.trim());
  
  console.log('🔍 Enhanced search query:', { 
    original: query, 
    enhanced: searchQuery,
    filters: Object.keys(filters),
    sort: { order, dir }
  });
  
  // Use existing searchCardsWithFilters with enhanced query and sort
  return searchCardsWithFilters(searchQuery, filters, page, order, dir);
};

/**
 * Get autocomplete suggestions for search terms
 */
export const getSearchSuggestions = async (query: string): Promise<string[]> => {
  try {
    // Use Scryfall's autocomplete for card names
    const cardNames = await autocompleteCardNames(query);
    
    // Add common Magic terms and operators
    const suggestions: string[] = [...cardNames];
    
    // Add operator suggestions if query is short
    if (query.length <= 3) {
      const operators = [
        '"exact phrase"',
        '-exclude',
        'name:cardname',
        'text:ability',
        'type:creature'
      ];
      suggestions.push(...operators);
    }
    
    // Add common Magic keywords that match the query
    const magicTerms = [
      'flying', 'trample', 'lifelink', 'deathtouch', 'vigilance', 'reach',
      'first strike', 'double strike', 'haste', 'hexproof', 'indestructible',
      'destroy', 'exile', 'draw', 'discard', 'counter', 'target', 'choose',
      'creature', 'instant', 'sorcery', 'artifact', 'enchantment', 'planeswalker'
    ];
    
    const matchingTerms = magicTerms.filter(term => 
      term.toLowerCase().includes(query.toLowerCase())
    );
    
    suggestions.push(...matchingTerms);
    
    // Remove duplicates and limit results
    const uniqueSuggestions = Array.from(new Set(suggestions));
    return uniqueSuggestions.slice(0, 10);
    
  } catch (error) {
    console.error('Failed to get search suggestions:', error);
    return [];
  }
};

// Export commonly used search queries
export const COMMON_QUERIES = {
  POPULAR_CARDS: 'is:commander OR name:"Lightning Bolt" OR name:"Counterspell" OR name:"Sol Ring" OR name:"Path to Exile" OR name:"Swords to Plowshares" OR name:"Birds of Paradise" OR name:"Dark Ritual" OR name:"Giant Growth"',
  BASIC_LANDS: 'type:basic type:land',
  CREATURES: 'type:creature',
  INSTANTS: 'type:instant',
  SORCERIES: 'type:sorcery',
  ARTIFACTS: 'type:artifact',
  ENCHANTMENTS: 'type:enchantment',
  PLANESWALKERS: 'type:planeswalker',
};