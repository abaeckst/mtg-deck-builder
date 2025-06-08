#!/usr/bin/env python3

import os
import sys

def update_scryfall_api_enhanced_filters(filename):
    """Update scryfallApi.ts with enhanced filter support for Phase 4B"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements with exact string matching
    updates = [
        # 1. Add enhanced filter types to SearchFilters interface
        (
            """export interface SearchFilters {
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
}""",
            """export interface SearchFilters {
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
}""",
            "Enhanced SearchFilters interface"
        ),
        
        # 2. Add gold mode and subtype filtering to searchCardsWithFilters
        (
            """  // Add color identity filters with advanced logic
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
  }""",
            """  // Phase 4B: Enhanced color and gold mode filtering
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
  }""",
            "Enhanced color and gold mode filtering"
        ),
        
        # 3. Add subtype filtering after type filters
        (
            """  // Add type filters
  if (filters.types && filters.types.length > 0) {
    const typeQuery = filters.types.map(type => `type:${type}`).join(' OR ');
    searchQuery += ` (${typeQuery})`;
  }""",
            """  // Add type filters
  if (filters.types && filters.types.length > 0) {
    const typeQuery = filters.types.map(type => `type:${type}`).join(' OR ');
    searchQuery += ` (${typeQuery})`;
  }
  
  // Phase 4B: Add subtype filters
  if (filters.subtypes && filters.subtypes.length > 0) {
    const subtypeQuery = filters.subtypes.map(subtype => `type:${subtype}`).join(' OR ');
    searchQuery += ` (${subtypeQuery})`;
  }""",
            "Subtype filtering support"
        ),
        
        # 4. Update the isFilterActive function to include new filter types
        (
            """      case 'colors':
      case 'types':
      case 'rarity':
      case 'sets':
      case 'keywords':
        return Array.isArray(value) && value.length > 0;""",
            """      case 'colors':
      case 'types':
      case 'rarity':
      case 'sets':
      case 'keywords':
      case 'subtypes':
        return Array.isArray(value) && value.length > 0;""",
            "Update isFilterActive for subtypes"
        ),
        
        # 5. Add isGoldMode to isFilterActive function
        (
            """      case 'colorIdentity':
        return typeof value === 'string' && value !== 'exact'; // 'exact' is default""",
            """      case 'colorIdentity':
        return typeof value === 'string' && value !== 'exact'; // 'exact' is default
      case 'isGoldMode':
        return typeof value === 'boolean' && value === true;""",
            "Update isFilterActive for gold mode"
    