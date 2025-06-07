// src/types/card.ts - Added pagination interfaces for progressive loading
// TypeScript interfaces for Magic: The Gathering card data from Scryfall API

/**
 * Main card interface based on Scryfall API response
 * Includes only the fields we'll actually use in our deck builder
 */
export interface ScryfallCard {
  // Core identifiers
  id: string;
  oracle_id: string;
  name: string;
  
  // Card images
  image_uris?: {
    small: string;
    normal: string;
    large: string;
    png: string;
    art_crop: string;
    border_crop: string;
  };
  
  // Mana and casting
  mana_cost?: string;
  cmc: number; // Converted mana cost
  colors: string[]; // Array of color letters: ['W', 'U', 'B', 'R', 'G']
  color_identity: string[];
  
  // Card details
  type_line: string;
  oracle_text?: string;
  power?: string;
  toughness?: string;
  loyalty?: string;
  
  // Set information
  set: string;
  set_name: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'mythic' | 'special' | 'bonus';
  
  // Legality in formats
  legalities: {
    standard: LegalityStatus;
    pioneer: LegalityStatus;
    modern: LegalityStatus;
    legacy: LegalityStatus;
    vintage: LegalityStatus;
    commander: LegalityStatus;
    brawl: LegalityStatus;
    historic: LegalityStatus;
    timeless: LegalityStatus;
    pauper: LegalityStatus;
  };
  
  // Additional useful fields
  keywords: string[];
  layout: string;
  card_faces?: CardFace[]; // For double-faced cards
}

/**
 * Pagination state interface for progressive loading
 */
export interface PaginatedSearchState {
  initialResults: ScryfallCard[];
  totalCards: number;
  loadedCards: number;
  hasMore: boolean;
  isLoadingMore: boolean;
  currentPage: number;
  lastQuery: string;
  lastFilters: any;
  lastSort: { order: string; dir: 'asc' | 'desc' };
  // Partial page consumption tracking
  currentScryfallPage: number;        // Actual Scryfall page number (1-based)
  cardsConsumedFromCurrentPage: number; // How many cards used from current Scryfall page
  currentPageCards: ScryfallCard[];   // Full current page data from Scryfall
  scryfallPageSize: number;           // Scryfall page size (175)
  displayBatchSize: number;           // User display batch size (75)
}

/**
 * Progressive loading configuration
 */
export interface ProgressiveLoadingConfig {
  initialPageSize: number;    // 75 cards initially
  loadMorePageSize: number;   // 175 cards per batch
  maxTotalCards?: number;     // Optional limit on total cards to load
}

/**
 * Legality status for different formats
 */
export type LegalityStatus = 'legal' | 'not_legal' | 'restricted' | 'banned';

/**
 * Card face interface for double-faced cards (like Transform cards)
 */
export interface CardFace {
  name: string;
  mana_cost?: string;
  type_line: string;
  oracle_text?: string;
  colors: string[];
  power?: string;
  toughness?: string;
  loyalty?: string;
  image_uris?: {
    small: string;
    normal: string;
    large: string;
    png: string;
    art_crop: string;
    border_crop: string;
  };
}

/**
 * DEPRECATED: Legacy card interface for backward compatibility only
 * Will be removed in future versions - use DeckCardInstance instead
 */
export interface DeckCard {
  // Card identification
  id: string;
  name: string;
  
  // Display information
  image_uri: string;
  mana_cost?: string;
  cmc: number;
  type_line: string;
  
  // Colors for filtering
  colors: string[];
  color_identity: string[];
  
  // Set and rarity for display
  set: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'mythic' | 'special' | 'bonus';
  
  // Deck building
  quantity: number; // How many copies in deck/sideboard
  maxQuantity: number; // Usually 4, unlimited for basic lands
  
  // Format legality
  legal_in_format?: boolean; // Will be set based on selected format
  
  // Card text and stats (from Scryfall)
  oracle_text?: string;
  power?: string;
  toughness?: string;
  loyalty?: string;
}

/**
 * Individual deck card instance with unique ID for proper selection
 * Each physical card copy in deck/sideboard gets its own instance
 */
export interface DeckCardInstance {
  instanceId: string;        // Unique: "cardId-zone-timestamp-random"
  cardId: string;           // Original Scryfall ID (for grouping, limits, etc.)
  name: string;
  image_uri: string;
  mana_cost?: string;
  cmc: number;
  type_line: string;
  colors: string[];
  color_identity: string[];
  set: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'mythic' | 'special' | 'bonus';
  zone: 'deck' | 'sideboard';  // Track which zone this instance belongs to
  addedAt: number;             // Timestamp for ordering/history
  
  // Card text and stats
  oracle_text?: string;
  power?: string;
  toughness?: string;
  loyalty?: string;
  
  // Format legality (inherited from original card)
  legal_in_format?: boolean;
}

/**
 * API search response from Scryfall
 */
export interface ScryfallSearchResponse {
  object: 'list';
  total_cards: number;
  has_more: boolean;
  next_page?: string;
  data: ScryfallCard[];
}

/**
 * Search parameters for Scryfall API
 */
export interface SearchParams {
  q: string; // Search query
  order?: 'name' | 'released' | 'set' | 'rarity' | 'color' | 'usd' | 'tix' | 'eur' | 'cmc' | 'power' | 'toughness' | 'edhrec' | 'artist';
  dir?: 'asc' | 'desc';
  unique?: 'cards' | 'art' | 'prints';
  page?: number;
  format?: 'json' | 'csv';
}

/**
 * Error response from Scryfall API
 */
export interface ScryfallError {
  object: 'error';
  code: string;
  status: number;
  warnings?: string[];
  details: string;
}

/**
 * Rate limiting information
 */
export interface RateLimitInfo {
  lastRequestTime: number;
  requestCount: number;
  resetTime: number;
}

/**
 * Supported Magic formats for deck building
 */
export type MagicFormat = 
  | 'standard'
  | 'pioneer'
  | 'modern'
  | 'legacy'
  | 'vintage'
  | 'commander'
  | 'brawl'
  | 'historic'
  | 'timeless'
  | 'pauper';

/**
 * Magic colors as constants
 */
export const MAGIC_COLORS = {
  WHITE: 'W',
  BLUE: 'U',
  BLACK: 'B',
  RED: 'R',
  GREEN: 'G'
} as const;

export type MagicColor = typeof MAGIC_COLORS[keyof typeof MAGIC_COLORS];

/**
 * Instance ID generation utility
 * Creates unique identifiers for individual card instances
 */
export const generateInstanceId = (cardId: string, zone: string): string => {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substr(2, 5);
  return `${cardId}-${zone}-${timestamp}-${random}`;
};

/**
 * Parse instance ID to extract original card ID and zone
 */
export const parseInstanceId = (instanceId: string): { cardId: string; zone: string; } => {
  const parts = instanceId.split('-');
  if (parts.length >= 2) {
    return {
      cardId: parts[0],
      zone: parts[1]
    };
  }
  // Fallback for old IDs
  return {
    cardId: instanceId,
    zone: 'unknown'
  };
};

/**
 * Convert a ScryfallCard to a DeckCardInstance for deck/sideboard use
 */
export const scryfallToDeckInstance = (
  scryfallCard: ScryfallCard, 
  zone: 'deck' | 'sideboard'
): DeckCardInstance => {
  return {
    instanceId: generateInstanceId(scryfallCard.id, zone),
    cardId: scryfallCard.id,
    name: scryfallCard.name,
    image_uri: getCardImageUri(scryfallCard),
    mana_cost: scryfallCard.mana_cost,
    cmc: scryfallCard.cmc,
    type_line: scryfallCard.type_line,
    colors: scryfallCard.colors,
    color_identity: scryfallCard.color_identity,
    set: scryfallCard.set,
    rarity: scryfallCard.rarity,
    zone,
    addedAt: Date.now(),
    oracle_text: scryfallCard.oracle_text,
    power: scryfallCard.power,
    toughness: scryfallCard.toughness,
    loyalty: scryfallCard.loyalty,
  };
};

/**
 * Convert a DeckCard to a DeckCardInstance for deck/sideboard use
 * DEPRECATED: For backward compatibility only
 */
export const deckCardToDeckInstance = (
  deckCard: DeckCard, 
  zone: 'deck' | 'sideboard'
): DeckCardInstance => {
  return {
    instanceId: generateInstanceId(deckCard.id, zone),
    cardId: deckCard.id,
    name: deckCard.name,
    image_uri: deckCard.image_uri,
    mana_cost: deckCard.mana_cost,
    cmc: deckCard.cmc,
    type_line: deckCard.type_line,
    colors: deckCard.colors,
    color_identity: deckCard.color_identity,
    set: deckCard.set,
    rarity: deckCard.rarity,
    zone,
    addedAt: Date.now(),
    oracle_text: deckCard.oracle_text,
    power: deckCard.power,
    toughness: deckCard.toughness,
    loyalty: deckCard.loyalty,
    legal_in_format: deckCard.legal_in_format,
  };
};

/**
 * ARCHITECTURAL BRIDGE UTILITIES
 * These utilities handle the dual identity system cleanly
 */

/**
 * Get the appropriate card ID for any card type
 * - ScryfallCard/DeckCard: returns .id
 * - DeckCardInstance: returns .cardId (original card ID)
 */
export const getCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
  if ('cardId' in card) {
    return card.cardId; // DeckCardInstance
  }
  return card.id; // ScryfallCard or DeckCard
};

/**
 * Get the appropriate selection ID for any card type
 * - ScryfallCard/DeckCard: returns .id (for card-based selection)
 * - DeckCardInstance: returns .instanceId (for instance-based selection)
 */
export const getSelectionId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
  if ('instanceId' in card) {
    return card.instanceId; // DeckCardInstance
  }
  return card.id; // ScryfallCard or DeckCard
};

/**
 * Check if a card is a DeckCardInstance
 */
export const isCardInstance = (card: ScryfallCard | DeckCard | DeckCardInstance): card is DeckCardInstance => {
  return 'instanceId' in card;
};

/**
 * Check if a card is a ScryfallCard
 */
export const isScryfallCard = (card: ScryfallCard | DeckCard | DeckCardInstance): card is ScryfallCard => {
  return 'oracle_id' in card;
};

/**
 * Utility functions for instance management
 */

/**
 * Get the count of instances for a specific card ID in a zone
 */
export const getCardQuantityInZone = (instances: DeckCardInstance[], cardId: string): number => {
  return instances.filter(instance => instance.cardId === cardId).length;
};

/**
 * Get total count of instances for a specific card ID across all zones
 */
export const getTotalCardQuantity = (
  deckInstances: DeckCardInstance[], 
  sideboardInstances: DeckCardInstance[], 
  cardId: string
): number => {
  const deckCount = getCardQuantityInZone(deckInstances, cardId);
  const sideboardCount = getCardQuantityInZone(sideboardInstances, cardId);
  return deckCount + sideboardCount;
};

/**
 * Group instances by their original card ID
 */
export const groupInstancesByCardId = (instances: DeckCardInstance[]): Map<string, DeckCardInstance[]> => {
  const groups = new Map<string, DeckCardInstance[]>();
  
  instances.forEach(instance => {
    const cardId = instance.cardId;
    if (!groups.has(cardId)) {
      groups.set(cardId, []);
    }
    groups.get(cardId)!.push(instance);
  });
  
  return groups;
};

/**
 * Get instances for a specific card ID
 */
export const getInstancesForCard = (instances: DeckCardInstance[], cardId: string): DeckCardInstance[] => {
  return instances.filter(instance => instance.cardId === cardId);
};

/**
 * Remove a specific number of instances for a card ID (removes oldest first)
 */
export const removeInstancesForCard = (
  instances: DeckCardInstance[], 
  cardId: string, 
  quantity: number
): DeckCardInstance[] => {
  const cardInstances = instances.filter(i => i.cardId === cardId);
  const otherInstances = instances.filter(i => i.cardId !== cardId);
  
  // Sort by addedAt timestamp (oldest first) and remove the requested quantity
  cardInstances.sort((a, b) => a.addedAt - b.addedAt);
  const remainingInstances = cardInstances.slice(quantity);
  
  return [...otherInstances, ...remainingInstances];
};

/**
 * Remove specific instances by their instance IDs
 */
export const removeSpecificInstances = (
  instances: DeckCardInstance[], 
  instanceIds: string[]
): DeckCardInstance[] => {
  const instanceIdSet = new Set(instanceIds);
  return instances.filter(instance => !instanceIdSet.has(instance.instanceId));
};

/**
 * Utility function to check if a card is a basic land
 * Includes snow-covered basics, Wastes, and any card with basic land type
 */
export const isBasicLand = (card: ScryfallCard | DeckCard | DeckCardInstance): boolean => {
  // Check for exact basic land names
  const basicLandNames = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest', 'Wastes'];
  if (basicLandNames.includes(card.name)) {
    return true;
  }
  
  // Check for snow-covered basics
  const snowBasics = ['Snow-Covered Plains', 'Snow-Covered Island', 'Snow-Covered Swamp', 
                     'Snow-Covered Mountain', 'Snow-Covered Forest'];
  if (snowBasics.includes(card.name)) {
    return true;
  }
  
  // Check if type line contains "Basic Land"
  if (card.type_line && card.type_line.includes('Basic Land')) {
    return true;
  }
  
  return false;
};

/**
 * Utility function to get the appropriate image URI from a Scryfall card
 * Updated to use PNG format for highest quality (745×1040)
 */
export const getCardImageUri = (card: ScryfallCard, size: 'small' | 'normal' | 'large' = 'normal'): string => {
  // Handle double-faced cards
  if (card.card_faces && card.card_faces.length > 0) {
    const face = card.card_faces[0];
    if (face.image_uris) {
      // Use PNG format for highest quality, fallback to requested size
      return face.image_uris.png || face.image_uris[size];
    }
  }
  
  // Handle normal cards
  if (card.image_uris) {
    // Use PNG format for highest quality (745×1040), fallback to requested size
    return card.image_uris.png || card.image_uris[size];
  }
  
  // Fallback - this shouldn't happen with valid Scryfall data
  return '';
};

/**
 * Convert a ScryfallCard to a DeckCard for internal use
 * DEPRECATED: Use scryfallToDeckInstance instead
 */
export const scryfallToDeckCard = (scryfallCard: ScryfallCard): DeckCard => {
  return {
    id: scryfallCard.id,
    name: scryfallCard.name,
    image_uri: getCardImageUri(scryfallCard),
    mana_cost: scryfallCard.mana_cost,
    cmc: scryfallCard.cmc,
    type_line: scryfallCard.type_line,
    colors: scryfallCard.colors,
    color_identity: scryfallCard.color_identity,
    set: scryfallCard.set,
    rarity: scryfallCard.rarity,
    quantity: 0, // Initially not in deck
    maxQuantity: isBasicLand(scryfallCard) ? Infinity : 4,
    // Copy card text and stats
    oracle_text: scryfallCard.oracle_text,
    power: scryfallCard.power,
    toughness: scryfallCard.toughness,
    loyalty: scryfallCard.loyalty,
  };
};