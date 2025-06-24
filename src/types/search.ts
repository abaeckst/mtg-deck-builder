// src/types/search.ts - Enhanced search interfaces for Phase 3E

/**
 * Enhanced search query structure with operator support
 */
export interface SearchQuery {
  raw: string;                    // Original search string
  terms: SearchTerm[];           // Parsed search terms
  operators: SearchOperator[];   // Special operators
  fields: SearchField[];         // Field-specific searches
}

/**
 * Individual search term with type and modifier
 */
export interface SearchTerm {
  value: string;
  type: 'name' | 'text' | 'type' | 'all';
  modifier: 'include' | 'exclude' | 'exact';
}

/**
 * Search operators for advanced queries
 */
export interface SearchOperator {
  type: 'exclude' | 'exact' | 'wildcard' | 'field';
  field?: 'name' | 'text' | 'type';
  value: string;
}

/**
 * Field-specific search constraints
 */
export interface SearchField {
  field: 'name' | 'text' | 'type';
  value: string;
  exact: boolean;
}

/**
 * Autocomplete suggestion with categorization
 */
export interface SearchSuggestion {
  text: string;
  type: 'name' | 'text' | 'type' | 'history' | 'operator';
  score: number;
  category: string;
  description?: string;
}

/**
 * Search result with relevance scoring
 */
export interface EnhancedSearchResult {
  card: any; // ScryfallCard
  relevanceScore: number;
  matchType: 'name' | 'text' | 'type' | 'multiple';
  matchHighlights: string[];
}

/**
 * Search state for autocomplete and history
 */
export interface SearchState {
  query: string;
  suggestions: SearchSuggestion[];
  showSuggestions: boolean;
  recentSearches: string[];
  isSearching: boolean;
}

/**
 * Common search operators and their descriptions
 */
export const SEARCH_OPERATORS = {
  EXACT_PHRASE: { symbol: '""', description: 'Search for exact phrase', example: '"destroy target creature"' },
  EXCLUDE: { symbol: '-', description: 'Exclude cards containing term', example: '-flying' },
  WILDCARD: { symbol: '*', description: 'Wildcard matching', example: '*bolt' },
  FIELD_NAME: { symbol: 'name:', description: 'Search only card names', example: 'name:lightning' },
  FIELD_TEXT: { symbol: 'text:', description: 'Search only card text', example: 'text:flying' },
  FIELD_TYPE: { symbol: 'type:', description: 'Search only type lines', example: 'type:creature' },
} as const;

/**
 * Common Magic terms for autocomplete
 */
export const COMMON_MAGIC_TERMS = {
  ABILITIES: [
    'flying', 'trample', 'lifelink', 'deathtouch', 'vigilance', 'reach', 
    'first strike', 'double strike', 'haste', 'hexproof', 'indestructible',
    'menace', 'prowess', 'flash', 'defender'
  ],
  KEYWORDS: [
    'destroy', 'exile', 'draw', 'discard', 'counter', 'target', 'choose',
    'sacrifice', 'tap', 'untap', 'return', 'search', 'shuffle'
  ],
  TYPES: [
    'creature', 'instant', 'sorcery', 'artifact', 'enchantment', 'planeswalker',
    'land', 'tribal', 'legendary', 'basic'
  ],
  SUBTYPES: [
    'human', 'elf', 'goblin', 'wizard', 'soldier', 'beast', 'dragon',
    'equipment', 'aura', 'vehicle', 'plains', 'island', 'swamp', 'mountain', 'forest'
  ]
} as const;