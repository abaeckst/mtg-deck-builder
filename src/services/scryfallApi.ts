// src/services/scryfallApi.ts - Complete working version
import { ScryfallCard, ScryfallSearchResponse } from '../types/card';

const SCRYFALL_API_BASE = 'https://api.scryfall.com';
const REQUEST_DELAY = 100; // 100ms delay between requests to respect rate limiting

// Simple delay function for rate limiting
const delay = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

// Rate limiting implementation
let lastRequestTime = 0;

const rateLimitedFetch = async (url: string): Promise<Response> => {
  const now = Date.now();
  const timeSinceLastRequest = now - lastRequestTime;
  
  if (timeSinceLastRequest < REQUEST_DELAY) {
    await delay(REQUEST_DELAY - timeSinceLastRequest);
  }
  
  lastRequestTime = Date.now();
  
  const response = await fetch(url, {
    headers: {
      'Accept': 'application/json',
    },
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response;
};

/**
 * Search for cards using Scryfall's search API
 */
export const searchCards = async (
  query: string,
  page = 1,
  unique = 'cards',
  order = 'name'
): Promise<ScryfallSearchResponse> => {
  try {
    // Handle empty queries - Scryfall doesn't accept empty q parameter
    if (!query || query.trim() === '') {
      throw new Error('Search query cannot be empty');
    }
    
    const params = new URLSearchParams({
      q: query.trim(),
      page: page.toString(),
      unique,
      order,
    });
    
    const url = `${SCRYFALL_API_BASE}/cards/search?${params.toString()}`;
    console.log('🌐 API Request:', url);
    const response = await rateLimitedFetch(url);
    const data = await response.json();
    
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
 * Get a random card from Scryfall
 */
export const getRandomCard = async (): Promise<ScryfallCard> => {
  try {
    const url = `${SCRYFALL_API_BASE}/cards/random`;
    const response = await rateLimitedFetch(url);
    const data = await response.json();
    
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
    const data = await response.json();
    
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
    const data = await response.json();
    
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
    const data = await response.json();
    
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
    const data = await response.json();
    
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
 * Advanced search with filters (for Phase 2)
 */
export interface SearchFilters {
  format?: string;
  colors?: string[];
  colorIdentity?: 'exact' | 'subset' | 'include'; // How to match colors
  types?: string[];
  rarity?: string[];
  sets?: string[];
  cmc?: { min?: number; max?: number };
  power?: { min?: number; max?: number };
  toughness?: { min?: number; max?: number };
  keywords?: string[];
  artist?: string;
  price?: { min?: number; max?: number };
}

export const searchCardsWithFilters = async (
  query: string,
  filters: SearchFilters = {},
  page = 1
): Promise<ScryfallSearchResponse> => {
  // Start with base query - ensure we never have empty query
  let searchQuery = query || '*';
  
  console.log('🔧 Building search query from:', { baseQuery: query, filters });
  
  // Add format filter with Custom Standard support
  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Standard-legal cards + Final Fantasy set
      searchQuery += ` (legal:standard OR set:fin)`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }
  
  // Add color identity filters with advanced logic
  if (filters.colors && filters.colors.length > 0) {
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
  
  return searchCards(searchQuery.trim(), page);
};

/**
 * Enhanced search with full-text capabilities and operator support
 */
export const enhancedSearchCards = async (
  query: string,
  filters: SearchFilters = {},
  page = 1
): Promise<ScryfallSearchResponse> => {
  // Handle empty queries
  if (!query || query.trim() === '') {
    // If we have filters, use wildcard search
    if (Object.keys(filters).length > 0) {
      return searchCardsWithFilters('*', filters, page);
    }
    throw new Error('Search query cannot be empty');
  }
  
  // Build enhanced query for full-text search
  const searchQuery = buildEnhancedSearchQuery(query.trim());
  
  console.log('🔍 Enhanced search query:', { 
    original: query, 
    enhanced: searchQuery,
    filters: Object.keys(filters)
  });
  
  // Use existing searchCardsWithFilters with enhanced query
  return searchCardsWithFilters(searchQuery, filters, page);
};

/**
 * Build enhanced search query with operator support
 */
function buildEnhancedSearchQuery(query: string): string {
  // For simple queries without operators, enable full-text search
  // This searches across name, oracle text, and type line
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    return `(name:${query} OR oracle:${query} OR type:${query})`;
  }
  
  // Only do advanced parsing for queries with operators
  const parts: string[] = [];
  let workingQuery = query;
  
  // Handle quoted phrases
  const quotedPhrases = query.match(/"[^"]+"/g) || [];
  quotedPhrases.forEach(phrase => {
    parts.push(phrase); // Keep quoted phrases as-is for Scryfall
    workingQuery = workingQuery.replace(phrase, '');
  });
  
  // Handle exclusions
  const exclusions = workingQuery.match(/-\w+/g) || [];
  exclusions.forEach(exclusion => {
    parts.push(exclusion); // Keep exclusions as-is
    workingQuery = workingQuery.replace(exclusion, '');
  });
  
  // Handle field-specific searches
  const fieldSearches = workingQuery.match(/(name|text|type):[\w\s]+/g) || [];
  fieldSearches.forEach(fieldSearch => {
    const [field, value] = fieldSearch.split(':');
    if (field === 'text') {
      parts.push(`oracle:${value}`); // Convert text: to oracle: for Scryfall
    } else {
      parts.push(fieldSearch); // Keep name: and type: as-is
    }
    workingQuery = workingQuery.replace(fieldSearch, '');
  });
  
  // Handle remaining terms - for advanced queries, do full-text search
  const remainingTerms = workingQuery.trim().split(/\s+/).filter(term => term.length > 0);
  if (remainingTerms.length > 0) {
    const fullTextSearch = remainingTerms.join(' ');
    // Only use complex OR logic if we already have other operators
    if (parts.length > 0) {
      parts.push(`(name:${fullTextSearch} OR oracle:${fullTextSearch} OR type:${fullTextSearch})`);
    } else {
      // If no operators detected, just add the simple search
      parts.push(fullTextSearch);
    }
  }
  
  return parts.join(' ').trim() || query;
}

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