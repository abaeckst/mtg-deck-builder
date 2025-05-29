// src/types/card.ts
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
 * Simplified card interface for our deck builder internal use
 * Contains only essential fields plus quantity tracking
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
 * Utility function to check if a card is a basic land
 */
export const isBasicLand = (card: ScryfallCard | DeckCard): boolean => {
  const basicLandNames = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest'];
  return basicLandNames.includes(card.name);
};

/**
 * Utility function to get the appropriate image URI from a Scryfall card
 */
export const getCardImageUri = (card: ScryfallCard, size: 'small' | 'normal' | 'large' = 'normal'): string => {
  // Handle double-faced cards
  if (card.card_faces && card.card_faces.length > 0) {
    const face = card.card_faces[0];
    if (face.image_uris) {
      return face.image_uris[size];
    }
  }
  
  // Handle normal cards
  if (card.image_uris) {
    return card.image_uris[size];
  }
  
  // Fallback - this shouldn't happen with valid Scryfall data
  return '';
};

/**
 * Convert a ScryfallCard to a DeckCard for internal use
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
  };
};