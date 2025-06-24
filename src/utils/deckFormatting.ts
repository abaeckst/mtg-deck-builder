// src/utils/deckFormatting.ts
// Utilities for formatting deck data for text export

import { DeckCardInstance } from '../types/card';

export interface DeckExportData {
  deckName: string;
  format: string;
  mainDeck: DeckCardInstance[];
  sideboard: DeckCardInstance[];
}

export interface CardTypeCounts {
  creatures: number;
  instants: number;
  sorceries: number;
  artifacts: number;
  enchantments: number;
  planeswalkers: number;
  lands: number;
  other: number;
}

/**
 * Group cards by name and count quantities
 */
export const groupCardsByName = (cards: DeckCardInstance[]): Map<string, number> => {
  const grouped = new Map<string, number>();
  
  cards.forEach(card => {
    const current = grouped.get(card.name) || 0;
    grouped.set(card.name, current + 1);
  });
  
  return grouped;
};

/**
 * Calculate card type counts for deck overview
 */
export const calculateCardTypeCounts = (cards: DeckCardInstance[]): CardTypeCounts => {
  const counts: CardTypeCounts = {
    creatures: 0,
    instants: 0,
    sorceries: 0,
    artifacts: 0,
    enchantments: 0,
    planeswalkers: 0,
    lands: 0,
    other: 0
  };
  
  cards.forEach(card => {
    const typeLine = card.type_line.toLowerCase();
    
    if (typeLine.includes('creature')) {
      counts.creatures++;
    } else if (typeLine.includes('instant')) {
      counts.instants++;
    } else if (typeLine.includes('sorcery')) {
      counts.sorceries++;
    } else if (typeLine.includes('artifact')) {
      counts.artifacts++;
    } else if (typeLine.includes('enchantment')) {
      counts.enchantments++;
    } else if (typeLine.includes('planeswalker')) {
      counts.planeswalkers++;
    } else if (typeLine.includes('land')) {
      counts.lands++;
    } else {
      counts.other++;
    }
  });
  
  return counts;
};

/**
 * Format deck data into MTGO-compatible text format
 */
export const formatDeckForMTGO = (data: DeckExportData): string => {
  const { deckName, format, mainDeck, sideboard } = data;
  
  // Calculate card type counts
  const typeCounts = calculateCardTypeCounts(mainDeck);
  
  // Group cards by name and quantity
  const mainDeckGroups = groupCardsByName(mainDeck);
  const sideboardGroups = groupCardsByName(sideboard);
  
  // Sort cards alphabetically within each group
  const sortedMainDeck = Array.from(mainDeckGroups.entries()).sort(([a], [b]) => a.localeCompare(b));
  const sortedSideboard = Array.from(sideboardGroups.entries()).sort(([a], [b]) => a.localeCompare(b));
  
  // Build the formatted string
  const lines: string[] = [];
  
  // Header information
  lines.push(`// Deck Name: ${deckName}`);
  lines.push(`// Format: ${format}`);
  
  // Card type summary
  const typeStrings: string[] = [];
  if (typeCounts.creatures > 0) typeStrings.push(`Creatures: ${typeCounts.creatures}`);
  if (typeCounts.instants > 0) typeStrings.push(`Instants: ${typeCounts.instants}`);
  if (typeCounts.sorceries > 0) typeStrings.push(`Sorceries: ${typeCounts.sorceries}`);
  if (typeCounts.artifacts > 0) typeStrings.push(`Artifacts: ${typeCounts.artifacts}`);
  if (typeCounts.enchantments > 0) typeStrings.push(`Enchantments: ${typeCounts.enchantments}`);
  if (typeCounts.planeswalkers > 0) typeStrings.push(`Planeswalkers: ${typeCounts.planeswalkers}`);
  if (typeCounts.lands > 0) typeStrings.push(`Lands: ${typeCounts.lands}`);
  if (typeCounts.other > 0) typeStrings.push(`Other: ${typeCounts.other}`);
  
  if (typeStrings.length > 0) {
    lines.push(`// ${typeStrings.join(', ')}`);
  }
  
  lines.push('');
  
  // Main deck
  if (sortedMainDeck.length > 0) {
    sortedMainDeck.forEach(([cardName, quantity]) => {
      lines.push(`${quantity} ${cardName}`);
    });
  } else {
    lines.push('// Empty deck');
  }
  
  // Sideboard
  if (sortedSideboard.length > 0) {
    lines.push('');
    lines.push('Sideboard:');
    sortedSideboard.forEach(([cardName, quantity]) => {
      lines.push(`${quantity} ${cardName}`);
    });
  }
  
  return lines.join('\n');
};

/**
 * Get a formatted display name for the current format
 */
export const getFormatDisplayName = (format: string): string => {
  const formatNames: Record<string, string> = {
    'standard': 'Standard',
    'custom-standard': 'Custom Standard (Standard + Unreleased)',
    'pioneer': 'Pioneer',
    'modern': 'Modern',
    'legacy': 'Legacy',
    'vintage': 'Vintage',
    'commander': 'Commander',
    'pauper': 'Pauper',
    '': 'All Formats'
  };
  
  return formatNames[format] || format;
};

/**
 * Copy text to clipboard with fallback support
 */
export const copyToClipboard = async (text: string): Promise<boolean> => {
  try {
    // Modern clipboard API
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    }
    
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    const success = document.execCommand('copy');
    document.body.removeChild(textArea);
    
    return success;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    return false;
  }
};
