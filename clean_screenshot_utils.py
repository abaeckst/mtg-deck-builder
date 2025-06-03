#!/usr/bin/env python3
"""
Clean up screenshotUtils.ts - Fix duplicate imports and organize properly
"""

import os

def clean_screenshot_utils():
    """Create a clean version of screenshotUtils.ts with all necessary functionality"""
    
    utils_path = "src/utils/screenshotUtils.ts"
    
    clean_content = '''// src/utils/screenshotUtils.ts
// Utilities for screenshot generation and deck image layout

import html2canvas from 'html2canvas';
import { DeckCardInstance, groupInstancesByCardId } from '../types/card';

export interface ViewportDimensions {
  modalWidth: number;
  modalHeight: number;
  availableWidth: number;
  availableHeight: number;
  headerHeight: number;
  controlsHeight: number;
  marginsTotal: number;
}

export interface CardLayoutCalculation {
  cardsPerMainColumn: number;
  cardsPerSideboardColumn: number;
  maxCardsPerColumn: number;
  optimalCardHeight: number;
  optimalCardWidth: number;
  calculatedScale: number;
  needsScrolling: boolean;
}

export interface SizeOverride {
  mode: 'auto' | 'small' | 'medium' | 'large';
  scaleFactor: number;
}

export interface ScreenshotLayout {
  mainDeckColumns: DeckCardInstance[][];
  sideboardColumns: DeckCardInstance[][];
}

export interface CardStackInfo {
  card: DeckCardInstance;
  quantity: number;
}

export const READABILITY_CONSTRAINTS = {
  minCardWidth: 100,   // Minimum width for readable card names
  minCardHeight: 140,  // Minimum height for readable card names
  minScaleFactor: 0.5, // Never go below 50% of normal size
  maxScaleFactor: 2.0, // Never go above 200% of normal size
};

export const SIZE_OVERRIDES = {
  small: 0.6,   // 60% of normal card size
  medium: 0.8,  // 80% of normal card size  
  large: 1.0,   // 100% of normal card size
};

// Base card dimensions (normal size)
const BASE_CARD_WIDTH = 130;
const BASE_CARD_HEIGHT = 181;

/**
 * Measure available space in the screenshot modal
 */
export const measureAvailableSpace = (): ViewportDimensions => {
  const modalElement = document.querySelector('.modal-fullscreen .modal-body');
  const headerElement = document.querySelector('.modal-fullscreen .modal-header');
  
  if (!modalElement) {
    // Fallback dimensions
    return {
      modalWidth: window.innerWidth * 0.95,
      modalHeight: window.innerHeight * 0.95,
      availableWidth: window.innerWidth * 0.85,
      availableHeight: window.innerHeight * 0.75,
      headerHeight: 60,
      controlsHeight: 80,
      marginsTotal: 40
    };
  }
  
  const modalRect = modalElement.getBoundingClientRect();
  const headerHeight = headerElement ? headerElement.getBoundingClientRect().height : 60;
  const controlsHeight = 80; // Size controls + margins
  const marginsTotal = 40; // Padding and margins
  
  return {
    modalWidth: modalRect.width,
    modalHeight: modalRect.height,
    availableWidth: modalRect.width - marginsTotal,
    availableHeight: modalRect.height - headerHeight - controlsHeight - marginsTotal,
    headerHeight,
    controlsHeight,
    marginsTotal
  };
};

/**
 * Calculate optimal card size to fit all cards without scrolling
 */
export const calculateOptimalCardSize = (
  mainDeckCount: number,
  sideboardCount: number,
  availableSpace: ViewportDimensions
): CardLayoutCalculation => {
  // Calculate cards per column
  const cardsPerMainColumn = Math.ceil(mainDeckCount / 5);
  const cardsPerSideboardColumn = Math.ceil(sideboardCount / 2);
  const maxCardsPerColumn = Math.max(cardsPerMainColumn, cardsPerSideboardColumn);
  
  // If no cards, return default
  if (maxCardsPerColumn === 0) {
    return {
      cardsPerMainColumn: 0,
      cardsPerSideboardColumn: 0,
      maxCardsPerColumn: 0,
      optimalCardHeight: BASE_CARD_HEIGHT,
      optimalCardWidth: BASE_CARD_WIDTH,
      calculatedScale: 1.0,
      needsScrolling: false
    };
  }
  
  // Calculate space needed for both main deck and sideboard
  const sectionSpacing = 60; // Space between main deck and sideboard sections
  const titleSpacing = 40;   // Space for section titles
  const cardGap = 4;         // Gap between cards
  
  // Available height for cards (accounting for section spacing)
  const availableCardHeight = availableSpace.availableHeight - sectionSpacing - titleSpacing;
  
  // Calculate optimal card height based on tallest column
  const totalGapsPerColumn = Math.max(0, maxCardsPerColumn - 1) * cardGap;
  const optimalCardHeight = (availableCardHeight - totalGapsPerColumn) / maxCardsPerColumn;
  
  // Calculate optimal card width (5 columns for main deck)
  const mainDeckGaps = 4 * cardGap; // Gaps between 5 columns
  const optimalCardWidth = (availableSpace.availableWidth - mainDeckGaps) / 5;
  
  // Calculate scale factor based on aspect ratio
  const heightScale = optimalCardHeight / BASE_CARD_HEIGHT;
  const widthScale = optimalCardWidth / BASE_CARD_WIDTH;
  const calculatedScale = Math.min(heightScale, widthScale);
  
  // Check if scrolling is needed
  const needsScrolling = calculatedScale < READABILITY_CONSTRAINTS.minScaleFactor;
  
  // Constrain scale factor
  const constrainedScale = Math.max(
    READABILITY_CONSTRAINTS.minScaleFactor,
    Math.min(READABILITY_CONSTRAINTS.maxScaleFactor, calculatedScale)
  );
  
  return {
    cardsPerMainColumn,
    cardsPerSideboardColumn,
    maxCardsPerColumn,
    optimalCardHeight: BASE_CARD_HEIGHT * constrainedScale,
    optimalCardWidth: BASE_CARD_WIDTH * constrainedScale,
    calculatedScale: constrainedScale,
    needsScrolling
  };
};

/**
 * Determine if scrolling is needed based on scale factors
 */
export const determineScrollingNeeded = (
  calculatedScale: number,
  overrideScale: number | null
): boolean => {
  const finalScale = overrideScale || calculatedScale;
  return finalScale < READABILITY_CONSTRAINTS.minScaleFactor;
};

/**
 * Wait for all images in an element to load completely
 */
export const waitForImages = async (element: HTMLElement): Promise<void> => {
  const images = element.querySelectorAll('img');
  const promises = Array.from(images).map(img => {
    if (img.complete) {
      return Promise.resolve();
    }
    return new Promise<void>((resolve) => {
      const onLoad = () => {
        img.removeEventListener('load', onLoad);
        img.removeEventListener('error', onError);
        resolve();
      };
      const onError = () => {
        img.removeEventListener('load', onLoad);
        img.removeEventListener('error', onError);
        console.warn('Image failed to load:', img.src);
        resolve(); // Resolve anyway to not block the process
      };
      img.addEventListener('load', onLoad);
      img.addEventListener('error', onError);
    });
  });
  
  console.log(`Waiting for ${promises.length} images to load...`);
  await Promise.all(promises);
  console.log('All images loaded successfully');
};

/**
 * Group unique cards and sort by mana cost for screenshot layout
 */
export const groupUniqueCards = (cards: DeckCardInstance[]): Map<string, DeckCardInstance[]> => {
  const groups = groupInstancesByCardId(cards);
  
  // Convert to array and sort by mana cost, then name
  const sortedEntries = Array.from(groups.entries()).sort(([, instancesA], [, instancesB]) => {
    const cardA = instancesA[0];
    const cardB = instancesB[0];
    
    // Sort by mana cost first
    if (cardA.cmc !== cardB.cmc) {
      return cardA.cmc - cardB.cmc;
    }
    
    // Then by name alphabetically
    return cardA.name.localeCompare(cardB.name);
  });
  
  // Convert back to Map with sorted order
  const sortedGroups = new Map<string, DeckCardInstance[]>();
  sortedEntries.forEach(([cardId, instances]) => {
    sortedGroups.set(cardId, instances);
  });
  
  return sortedGroups;
};

/**
 * Arrange cards for screenshot layout with round-robin distribution
 */
export const arrangeCardsForScreenshot = (
  mainDeck: DeckCardInstance[], 
  sideboard: DeckCardInstance[]
): ScreenshotLayout => {
  // Group and sort main deck cards
  const mainDeckGroups = groupUniqueCards(mainDeck);
  const mainDeckCards = Array.from(mainDeckGroups.values()).map(instances => instances[0]);
  
  // Group and sort sideboard cards
  const sideboardGroups = groupUniqueCards(sideboard);
  const sideboardCards = Array.from(sideboardGroups.values()).map(instances => instances[0]);
  
  // Distribute main deck across 5 columns (round-robin)
  const mainDeckColumns: DeckCardInstance[][] = [[], [], [], [], []];
  mainDeckCards.forEach((card, index) => {
    const columnIndex = index % 5;
    mainDeckColumns[columnIndex].push(card);
  });
  
  // Distribute sideboard across 2 columns (round-robin)
  const sideboardColumns: DeckCardInstance[][] = [[], []];
  sideboardCards.forEach((card, index) => {
    const columnIndex = index % 2;
    sideboardColumns[columnIndex].push(card);
  });
  
  return {
    mainDeckColumns,
    sideboardColumns
  };
};

/**
 * Generate deck image using html2canvas with enhanced options for CORS handling
 */
export const generateDeckImage = async (elementId: string): Promise<Blob | null> => {
  try {
    const element = document.getElementById(elementId);
    if (!element) {
      throw new Error(`Element with ID '${elementId}' not found`);
    }
    
    console.log('Starting screenshot generation...');
    
    // Multiple configuration attempts for better CORS handling
    const canvasOptions = [
      // Option 1: Standard configuration with CORS
      {
        background: '#1a1a1a',
        useCORS: true,
        allowTaint: false,
        logging: false,
        scale: 2,
        width: element.scrollWidth,
        height: element.scrollHeight,
      },
      // Option 2: Allow taint for CORS issues
      {
        background: '#1a1a1a',
        useCORS: false,
        allowTaint: true,
        logging: false,
        scale: 2,
        width: element.scrollWidth,
        height: element.scrollHeight,
      },
      // Option 3: Simplified fallback
      {
        background: '#1a1a1a',
        useCORS: false,
        allowTaint: true,
        logging: true,
        scale: 1,
      }
    ];
    
    let canvas: HTMLCanvasElement | null = null;
    let lastError: Error | null = null;
    
    // Try each configuration until one works
    for (let i = 0; i < canvasOptions.length; i++) {
      try {
        console.log(`Attempting screenshot with configuration ${i + 1}...`);
        canvas = await html2canvas(element, canvasOptions[i]);
        console.log('Canvas generated successfully:', {
          width: canvas.width,
          height: canvas.height,
          scale: canvasOptions[i].scale || 1,
          configUsed: i + 1
        });
        break;
      } catch (configError) {
        console.warn(`Configuration ${i + 1} failed:`, configError);
        lastError = configError instanceof Error ? configError : new Error(String(configError));
        continue;
      }
    }
    
    if (!canvas) {
      throw lastError || new Error('All canvas configurations failed');
    }
    
    // Convert canvas to blob with high quality
    return new Promise((resolve) => {
      canvas!.toBlob(resolve, 'image/png', 1.0); // Maximum quality PNG
    });
  } catch (error) {
    console.error('Failed to generate deck image:', error);
    return null;
  }
};

/**
 * Download image blob as file
 */
export const downloadImage = (blob: Blob, filename: string): void => {
  try {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Clean up the object URL
    setTimeout(() => URL.revokeObjectURL(url), 100);
    
    console.log('Image download initiated:', filename);
  } catch (error) {
    console.error('Failed to download image:', error);
  }
};

/**
 * Generate a filename for the deck image
 */
export const generateDeckImageFilename = (deckName: string = 'deck'): string => {
  // Sanitize deck name for filename
  const sanitized = deckName
    .replace(/[^a-zA-Z0-9\\-_\\s]/g, '') // Remove invalid characters
    .replace(/\\s+/g, '_') // Replace spaces with underscores
    .toLowerCase();
    
  const timestamp = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  return `${sanitized}_${timestamp}.png`;
};

/**
 * Get card quantity for a specific card in a group
 */
export const getCardQuantityInGroup = (
  groups: Map<string, DeckCardInstance[]>, 
  cardId: string
): number => {
  const instances = groups.get(cardId);
  return instances ? instances.length : 0;
};

/**
 * Create card stack information for display
 */
export const createCardStackInfo = (
  cards: DeckCardInstance[],
  groups: Map<string, DeckCardInstance[]>
): CardStackInfo[] => {
  return cards.map(card => ({
    card,
    quantity: getCardQuantityInGroup(groups, card.cardId)
  }));
};
'''
    
    # Write the clean content
    with open(utils_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    print(f"✅ Cleaned and fixed {utils_path}")
    print("   • Removed duplicate imports")
    print("   • Added dynamic sizing functions")
    print("   • Preserved all existing functionality")

def main():
    """Main execution function"""
    print("🧹 Cleaning up screenshotUtils.ts...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: src directory not found!")
        print("Please run this script from your project root directory (mtg-deckbuilder)")
        return
    
    try:
        clean_screenshot_utils()
        
        print("\n" + "=" * 50)
        print("✅ screenshotUtils.ts cleanup complete!")
        print("\n🔧 Next Steps:")
        print("   1. Run 'npm start' to verify compilation")
        print("   2. Test screenshot modal for basic functionality")
        print("   3. Run the full dynamic sizing update if needed")
        
    except Exception as e:
        print(f"\n❌ Error during cleanup: {str(e)}")
        print("Please check the error message and try again.")

if __name__ == "__main__":
    main()
