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
    const params = new URLSearchParams({
      q: query,
      page: page.toString(),
      unique,
      order,
    });
    
    const url = `${SCRYFALL_API_BASE}/cards/search?${params.toString()}`;
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
  types?: string[];
  rarity?: string[];
  set?: string;
  cmc?: { min?: number; max?: number };
  power?: { min?: number; max?: number };
  toughness?: { min?: number; max?: number };
}

export const searchCardsWithFilters = async (
  query: string,
  filters: SearchFilters = {},
  page = 1
): Promise<ScryfallSearchResponse> => {
  let searchQuery = query;
  
  // Add format filter
  if (filters.format) {
    searchQuery += ` legal:${filters.format}`;
  }
  
  // Add color filters
  if (filters.colors && filters.colors.length > 0) {
    const colorQuery = filters.colors.join('');
    searchQuery += ` color:${colorQuery}`;
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
  
  // Add set filter
  if (filters.set) {
    searchQuery += ` set:${filters.set}`;
  }
  
  // Add CMC filter
  if (filters.cmc) {
    if (filters.cmc.min !== undefined) {
      searchQuery += ` cmc>=${filters.cmc.min}`;
    }
    if (filters.cmc.max !== undefined) {
      searchQuery += ` cmc<=${filters.cmc.max}`;
    }
  }
  
  // Add power filter
  if (filters.power) {
    if (filters.power.min !== undefined) {
      searchQuery += ` power>=${filters.power.min}`;
    }
    if (filters.power.max !== undefined) {
      searchQuery += ` power<=${filters.power.max}`;
    }
  }
  
  // Add toughness filter
  if (filters.toughness) {
    if (filters.toughness.min !== undefined) {
      searchQuery += ` toughness>=${filters.toughness.min}`;
    }
    if (filters.toughness.max !== undefined) {
      searchQuery += ` toughness<=${filters.toughness.max}`;
    }
  }
  
  return searchCards(searchQuery.trim(), page);
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