// src/utils/screenshotUtils.ts
// FIXED: Aggressive waste space detection for better card scaling

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
  maxScaleFactor: 4.0, // Allow up to 400% for very few cards
};

// Updated size overrides per user request
export const SIZE_OVERRIDES = {
  small: 0.8,   // 80% of normal card size
  medium: 1.6,  // 160% of normal card size  
  large: 2.4,   // 240% of normal card size
};

// Base card dimensions (normal size)
const BASE_CARD_WIDTH = 130;
const BASE_CARD_HEIGHT = 181;

/**
 * Measure available space in the screenshot modal
 */
export const measureAvailableSpace = (): ViewportDimensions => {
  const modalWidth = window.innerWidth;
  const modalHeight = window.innerHeight;
  const controlsHeight = 0;
  const marginsTotal = 40;
  
  return {
    modalWidth,
    modalHeight,
    availableWidth: modalWidth - marginsTotal,
    availableHeight: modalHeight - marginsTotal,
    headerHeight: 0,
    controlsHeight,
    marginsTotal
  };
};

/**
 * Calculate optimal card size with aggressive waste space detection
 */
export const calculateOptimalCardSize = (
  mainDeckCount: number,
  sideboardCount: number,
  availableSpace: ViewportDimensions,
  forcedScale?: number
): CardLayoutCalculation & { 
  mainDeckColumns: number; 
  sideboardColumns: number; 
  mainDeckSpaceRatio: number;
  sideboardSpaceRatio: number;
  mainDeckAbsoluteHeight: number;
  sideboardAbsoluteHeight: number;
} => {
  
  if (mainDeckCount === 0 && sideboardCount === 0) {
    return {
      cardsPerMainColumn: 0,
      cardsPerSideboardColumn: 0,
      maxCardsPerColumn: 0,
      optimalCardHeight: BASE_CARD_HEIGHT,
      optimalCardWidth: BASE_CARD_WIDTH,
      calculatedScale: 1.0,
      needsScrolling: false,
      mainDeckColumns: 12,
      sideboardColumns: 6,
      mainDeckSpaceRatio: 0.7,
      sideboardSpaceRatio: 0.3,
      mainDeckAbsoluteHeight: BASE_CARD_HEIGHT,
      sideboardAbsoluteHeight: BASE_CARD_HEIGHT
    };
  }

  if (forcedScale) {
    console.log(`Using forced scale: ${forcedScale}`);
    return calculateLayoutForOptimizedScale(forcedScale, mainDeckCount, sideboardCount, availableSpace);
  }

  console.log('=== AGGRESSIVE SPACE UTILIZATION OPTIMIZATION ===');
  return findOptimalLayoutBySpaceUtilization(mainDeckCount, sideboardCount, availableSpace);
};

/**
 * Find optimal layout with AGGRESSIVE waste space detection
 */
export const findOptimalLayoutBySpaceUtilization = (
  mainDeckCount: number,
  sideboardCount: number,
  availableSpace: ViewportDimensions
): CardLayoutCalculation & { 
  mainDeckColumns: number; 
  sideboardColumns: number; 
  mainDeckSpaceRatio: number;
  sideboardSpaceRatio: number;
  mainDeckAbsoluteHeight: number;
  sideboardAbsoluteHeight: number;
} => {
  
  // Estimate unique cards
  const estimatedUniqueMainDeck = Math.ceil(mainDeckCount * 0.6);
  const estimatedUniqueSideboard = Math.ceil(sideboardCount * 0.7);
  
  console.log(`🔥 HYBRID OPTIMIZATION: ${estimatedUniqueMainDeck} main, ${estimatedUniqueSideboard} sideboard unique cards`);
  
  const totalAvailableHeight = availableSpace.availableHeight - 40; // Minimal margins
  const totalAvailableWidth = availableSpace.availableWidth - 10;
  
  console.log(`🔥 Available space: ${totalAvailableWidth}w × ${totalAvailableHeight}h`);
  
  interface OptimalLayout {
    mainColumns: number;
    sideboardColumns: number;
    mainRows: number;
    sideboardRows: number;
    cardScale: number;
    utilization: number;
    cardSizeScore: number; // PRIMARY: Bigger cards win
    mainHeight: number;
    sideboardHeight: number;
  }
  
  let bestLayout: OptimalLayout | null = null;
  
  // Generate smart configurations
  const testConfigurations = generateSmartConfigurations(
    estimatedUniqueMainDeck, 
    estimatedUniqueSideboard
  );
  
  for (const config of testConfigurations) {
    // DIRECT APPROACH: Calculate the maximum scale that fits the screen for this layout
    const maxScaleByWidth = totalAvailableWidth / (Math.max(config.mainColumns, config.sideboardColumns) * BASE_CARD_WIDTH);
    
    // Calculate required height for each section at this scale
    const cardHeightAtMaxScale = BASE_CARD_HEIGHT * maxScaleByWidth;
    const mainHeightNeeded = (config.mainRows * cardHeightAtMaxScale) + (estimatedUniqueMainDeck > 0 ? 40 : 0);
    const sideboardHeightNeeded = (config.sideboardRows * cardHeightAtMaxScale) + (estimatedUniqueSideboard > 0 ? 40 : 0);
    const totalHeightNeeded = mainHeightNeeded + sideboardHeightNeeded + 10;
    
    // If it doesn't fit vertically, scale down to fit
    let finalScale = maxScaleByWidth;
    if (totalHeightNeeded > totalAvailableHeight) {
      const heightScaleFactor = totalAvailableHeight / totalHeightNeeded;
      finalScale = maxScaleByWidth * heightScaleFactor;
    }
    
    // Don't allow scales that are too small
    if (finalScale < 0.5) {
      console.log(`❌ ${config.mainColumns}×${config.mainRows} main, ${config.sideboardColumns}×${config.sideboardRows} SB: final scale ${finalScale.toFixed(2)} too small`);
      continue;
    }
    
    // Calculate final dimensions
    const finalCardWidth = BASE_CARD_WIDTH * finalScale;
    const finalCardHeight = BASE_CARD_HEIGHT * finalScale;
    const actualMainHeight = (config.mainRows * finalCardHeight) + (estimatedUniqueMainDeck > 0 ? 40 : 0);
    const actualSideboardHeight = (config.sideboardRows * finalCardHeight) + (estimatedUniqueSideboard > 0 ? 40 : 0);
    const actualTotalHeight = actualMainHeight + actualSideboardHeight + 10;
    
    // Calculate how much of the screen we're using
    const heightUtilization = actualTotalHeight / totalAvailableHeight;
    const widthUtilization = (Math.max(config.mainColumns, config.sideboardColumns) * finalCardWidth) / totalAvailableWidth;
    
    console.log(`🔥 ${config.mainColumns}×${config.mainRows} main, ${config.sideboardColumns}×${config.sideboardRows} SB: scale ${finalScale.toFixed(2)}, cards ${finalCardWidth.toFixed(0)}×${finalCardHeight.toFixed(0)}, height util ${(heightUtilization * 100).toFixed(1)}%, width util ${(widthUtilization * 100).toFixed(1)}%`);
    
    // PRIMARY METRIC: Card size (bigger cards always win)
    const cardSizeScore = finalScale * 1000;
    
    const layout: OptimalLayout = {
      mainColumns: config.mainColumns,
      sideboardColumns: config.sideboardColumns,
      mainRows: config.mainRows,
      sideboardRows: config.sideboardRows,
      cardScale: finalScale,
      utilization: heightUtilization * widthUtilization, // Overall screen utilization
      cardSizeScore,
      mainHeight: actualMainHeight,
      sideboardHeight: actualSideboardHeight
    };
    // CRITICAL: Reject any layout that causes scrolling (height utilization > 100%)
    if (heightUtilization > 1.0) {
      console.log(`❌ ${config.mainColumns}×${config.mainRows} main, ${config.sideboardColumns}×${config.sideboardRows} SB: REJECTED - height overflow ${(heightUtilization * 100).toFixed(1)}%`);
      continue; // Skip layouts that cause scrolling
    }
    
    // Choose layout with BIGGEST cards (among layouts that FIT without scrolling)
    if (!bestLayout || cardSizeScore > bestLayout.cardSizeScore) {
      bestLayout = layout;
      console.log(`✅ NEW BEST: ${config.mainColumns}×${config.mainRows} main, ${config.sideboardColumns}×${config.sideboardRows} SB: scale ${finalScale.toFixed(2)}, no overflow`);
    }
  }
  
  if (!bestLayout) {
    console.warn('❌ No layout found, using fallback');
    return calculateLayoutForOptimizedScale(1.0, mainDeckCount, sideboardCount, availableSpace);
  }
  
  console.log(`🔥 OPTIMAL HYBRID: ${bestLayout.mainColumns}×${bestLayout.mainRows} main, ${bestLayout.sideboardColumns}×${bestLayout.sideboardRows} SB`);
  console.log(`   Card scale: ${bestLayout.cardScale.toFixed(2)}x, Card size: ${(BASE_CARD_WIDTH * bestLayout.cardScale).toFixed(0)}×${(BASE_CARD_HEIGHT * bestLayout.cardScale).toFixed(0)} pixels`);
  
  // SAFETY CHECK: Ensure selected layout doesn't cause overflow
  const finalHeightUtil = (bestLayout.mainHeight + bestLayout.sideboardHeight) / totalAvailableHeight;
  if (finalHeightUtil > 1.0) {
    console.warn(`⚠️  SAFETY OVERRIDE: Selected layout causes ${(finalHeightUtil * 100).toFixed(1)}% height utilization - this should not happen!`);
  }
  
  // Calculate space ratios for layout
  const totalHeight = bestLayout.mainHeight + bestLayout.sideboardHeight;
  const mainDeckSpaceRatio = totalHeight > 0 ? bestLayout.mainHeight / totalHeight : 0.7;
  const sideboardSpaceRatio = totalHeight > 0 ? bestLayout.sideboardHeight / totalHeight : 0.3;
  
  return {
    cardsPerMainColumn: bestLayout.mainRows,
    cardsPerSideboardColumn: bestLayout.sideboardRows,
    maxCardsPerColumn: Math.max(bestLayout.mainRows, bestLayout.sideboardRows),
    optimalCardHeight: BASE_CARD_HEIGHT * bestLayout.cardScale,
    optimalCardWidth: BASE_CARD_WIDTH * bestLayout.cardScale,
    calculatedScale: bestLayout.cardScale,
    needsScrolling: false,
    mainDeckColumns: bestLayout.mainColumns,
    sideboardColumns: bestLayout.sideboardColumns,
    mainDeckSpaceRatio,
    sideboardSpaceRatio,
    mainDeckAbsoluteHeight: bestLayout.mainHeight,
    sideboardAbsoluteHeight: bestLayout.sideboardHeight
  };
};

/**
 * BINARY SEARCH for maximum scale
 */
function findMaxScaleWithBinarySearch(
  config: {mainColumns: number, mainRows: number, sideboardColumns: number, sideboardRows: number},
  availableWidth: number,
  availableHeight: number,
  mainDeckCards: number,
  sideboardCards: number
): number {
  
  const totalCards = mainDeckCards + sideboardCards;
  
  // MASSIVE scale ranges
  let maxTestScale: number;
  if (totalCards <= 8) maxTestScale = 12.0;      // Tiny decks can be HUGE
  else if (totalCards <= 15) maxTestScale = 8.0;  // Small decks can be very large  
  else if (totalCards <= 25) maxTestScale = 6.0;  // Medium decks still large
  else maxTestScale = 4.0;                         // Large decks reasonably sized
  
  let low = 0.5;
  let high = maxTestScale;
  let bestScale = 0.5;
  
  // Binary search for maximum fitting scale
  while (high - low > 0.02) { // Precision to 0.02x
    const mid = (low + high) / 2;
    
    if (canConfigFitWithScale(config, mid, availableWidth, availableHeight, mainDeckCards, sideboardCards)) {
      bestScale = mid;
      low = mid; // Can fit, try larger
    } else {
      high = mid; // Can't fit, try smaller
    }
  }
  
  return bestScale;
}

/**
 * Test if specific configuration fits with given scale
 */
function canConfigFitWithScale(
  config: {mainColumns: number, mainRows: number, sideboardColumns: number, sideboardRows: number},
  scale: number,
  availableWidth: number,
  availableHeight: number,
  mainDeckCards: number,
  sideboardCards: number
): boolean {
  
  const cardWidth = BASE_CARD_WIDTH * scale;
  const cardHeight = BASE_CARD_HEIGHT * scale;
  
  // Width check - use 99.9% of space (eliminate safety margins)
  const mainWidth = config.mainColumns * cardWidth;
  const sideboardWidth = config.sideboardColumns * cardWidth;
  const maxRequiredWidth = Math.max(mainWidth, sideboardWidth);
  
  if (maxRequiredWidth > availableWidth * 0.999) {
    return false;
  }
  
  // Height check
  const mainHeight = (config.mainRows * cardHeight) + (mainDeckCards > 0 ? 40 : 0);
  const sideboardHeight = (config.sideboardRows * cardHeight) + (sideboardCards > 0 ? 40 : 0);
  
  let totalRequiredHeight: number;
  
  if (sideboardCards === 0) {
    // NO SIDEBOARD: Main deck gets 95% of space
    const allocatedMainSpace = availableHeight * 0.95;
    totalRequiredHeight = mainHeight;
    
    if (totalRequiredHeight > allocatedMainSpace) {
      return false;
    }
  } else if (mainDeckCards === 0) {
    // NO MAIN DECK: Sideboard gets 95% of space  
    const allocatedSideboardSpace = availableHeight * 0.95;
    totalRequiredHeight = sideboardHeight;
    
    if (totalRequiredHeight > allocatedSideboardSpace) {
      return false;
    }
  } else {
    // BOTH SECTIONS: Use priority allocation logic
    const minSideboardSpace = sideboardHeight + 20;
    const remainingSpaceForMainDeck = availableHeight - minSideboardSpace;
    
    // Check if main deck fits in remaining space
    if (mainHeight > remainingSpaceForMainDeck) {
      return false;
    }
    
    totalRequiredHeight = mainHeight + sideboardHeight + 10;
    if (totalRequiredHeight > availableHeight * 0.999) {
      return false;
    }
  }
  
  return true;
}

/**
 * Generate smart configurations optimized for maximum card size
 */
function generateSmartConfigurations(
  mainDeckCards: number,
  sideboardCards: number
): Array<{mainColumns: number, mainRows: number, sideboardColumns: number, sideboardRows: number}> {
  
  const configurations: Array<{mainColumns: number, mainRows: number, sideboardColumns: number, sideboardRows: number}> = [];
  
  // MAIN DECK CONFIGURATIONS: Generate COMPREHENSIVE layouts for optimal width utilization
  const mainConfigs = [];
  if (mainDeckCards > 0) {
    console.log(`📊 Main deck has ${mainDeckCards} cards - generating comprehensive layouts`);
    
    // GENERATE ALL REASONABLE LAYOUT OPTIONS (prioritize fewer rows for width utilization)
    
    // PRIORITY 1: Single row layouts (MAXIMUM width utilization)
    if (mainDeckCards <= 16) { // Practical limit for single row
      mainConfigs.push({ columns: mainDeckCards, rows: 1 });
      console.log(`📊 Added single row: ${mainDeckCards}×1 (maximum width utilization)`);
    }
    
    // PRIORITY 2: Two row layouts (excellent width utilization)
    if (mainDeckCards >= 4) {
      const cols2Row = Math.ceil(mainDeckCards / 2);
      if (cols2Row <= 20) { // Allow wide layouts
        mainConfigs.push({ columns: cols2Row, rows: 2 });
        console.log(`📊 Added two row: ${cols2Row}×2 (excellent width utilization)`);
      }
    }
    
    // PRIORITY 3: Three row layouts (good width utilization)
    if (mainDeckCards >= 6) {
      const cols3Row = Math.ceil(mainDeckCards / 3);
      if (cols3Row >= 2 && cols3Row <= 15) { // Reasonable range
        mainConfigs.push({ columns: cols3Row, rows: 3 });
        console.log(`📊 Added three row: ${cols3Row}×3 (good width utilization)`);
      }
    }
    
    // PRIORITY 4: Four row layouts (moderate width utilization)
    if (mainDeckCards >= 8) {
      const cols4Row = Math.ceil(mainDeckCards / 4);
      if (cols4Row >= 2 && cols4Row <= 12) { // Reasonable range
        mainConfigs.push({ columns: cols4Row, rows: 4 });
        console.log(`📊 Added four row: ${cols4Row}×4 (moderate width utilization)`);
      }
    }
    
    // PRIORITY 5: Five row layouts (for larger decks)
    if (mainDeckCards >= 15) {
      const cols5Row = Math.ceil(mainDeckCards / 5);
      if (cols5Row >= 3 && cols5Row <= 10) {
        mainConfigs.push({ columns: cols5Row, rows: 5 });
        console.log(`📊 Added five row: ${cols5Row}×5 (larger deck layout)`);
      }
    }
    
    // PRIORITY 6: Six row layouts (for very large decks only)
    if (mainDeckCards >= 24) {
      const cols6Row = Math.ceil(mainDeckCards / 6);
      if (cols6Row >= 4 && cols6Row <= 8) {
        mainConfigs.push({ columns: cols6Row, rows: 6 });
        console.log(`📊 Added six row: ${cols6Row}×6 (very large deck layout)`);
      }
    }
    
    // Fallback: ensure we have at least one configuration
    if (mainConfigs.length === 0) {
      const fallbackCols = Math.min(Math.max(Math.ceil(Math.sqrt(mainDeckCards)), 2), 8);
      const fallbackRows = Math.ceil(mainDeckCards / fallbackCols);
      mainConfigs.push({ columns: fallbackCols, rows: fallbackRows });
      console.log(`📊 Added fallback: ${fallbackCols}×${fallbackRows}`);
    }
  } else {
    mainConfigs.push({ columns: 1, rows: 0 });
  }
  
  // SIDEBOARD CONFIGURATIONS: Generate comprehensive sideboard layouts
  const sideboardConfigs = [];
  if (sideboardCards > 0) {
    console.log(`📊 Sideboard has ${sideboardCards} cards - generating layouts`);
    
    // PRIORITY 1: Single row layouts (best for space efficiency)
    if (sideboardCards <= 12) {
      sideboardConfigs.push({ columns: sideboardCards, rows: 1 });
      console.log(`📊 Added SB single row: ${sideboardCards}×1`);
    }
    
    // PRIORITY 2: Two-row layouts
    if (sideboardCards >= 4) {
      const cols2Row = Math.ceil(sideboardCards / 2);
      if (cols2Row <= 10) {
        sideboardConfigs.push({ columns: cols2Row, rows: 2 });
        console.log(`📊 Added SB two row: ${cols2Row}×2`);
      }
    }
    
    // PRIORITY 3: Three-row layouts (for larger sideboards)
    if (sideboardCards >= 9) {
      const cols3Row = Math.ceil(sideboardCards / 3);
      if (cols3Row <= 6) {
        sideboardConfigs.push({ columns: cols3Row, rows: 3 });
        console.log(`📊 Added SB three row: ${cols3Row}×3`);
      }
    }
    
    // Fallback for sideboard
    if (sideboardConfigs.length === 0) {
      const fallbackCols = Math.min(sideboardCards, 6);
      const fallbackRows = Math.ceil(sideboardCards / fallbackCols);
      sideboardConfigs.push({ columns: fallbackCols, rows: fallbackRows });
      console.log(`📊 Added SB fallback: ${fallbackCols}×${fallbackRows}`);
    }
  } else {
    sideboardConfigs.push({ columns: 1, rows: 0 });
  }
  
  // COMBINE ALL CONFIGURATIONS
  console.log(`📊 Main deck configs: ${mainConfigs.length}, Sideboard configs: ${sideboardConfigs.length}`);
  console.log(`📊 Main configurations:`, mainConfigs);
  console.log(`📊 Sideboard configurations:`, sideboardConfigs);
  
  for (const mainConfig of mainConfigs) {
    for (const sideboardConfig of sideboardConfigs) {
      configurations.push({
        mainColumns: mainConfig.columns,
        mainRows: mainConfig.rows,
        sideboardColumns: sideboardConfig.columns,
        sideboardRows: sideboardConfig.rows
      });
    }
  }
  
  // Remove duplicates
  const uniqueConfigs = configurations.filter((config, index, self) => 
    index === self.findIndex(c => 
      c.mainColumns === config.mainColumns && 
      c.mainRows === config.mainRows && 
      c.sideboardColumns === config.sideboardColumns && 
      c.sideboardRows === config.sideboardRows
    )
  );
  
  // Sort by FEWER TOTAL ROWS (maximum width utilization priority)
  uniqueConfigs.sort((a, b) => {
    const totalRowsA = a.mainRows + a.sideboardRows;
    const totalRowsB = b.mainRows + b.sideboardRows;
    return totalRowsA - totalRowsB; // Fewer rows first = better width utilization
  });
  
  console.log(`🔥 Testing ${uniqueConfigs.length} comprehensive configurations (prioritized for maximum width utilization)`);
  return uniqueConfigs;
}

/**
 * Calculate layout for specific scale with optimized parameters
 */
export const calculateLayoutForOptimizedScale = (
  scale: number,
  mainDeckCount: number,
  sideboardCount: number,
  availableSpace: ViewportDimensions
): CardLayoutCalculation & { mainDeckColumns: number; sideboardColumns: number; mainDeckSpaceRatio: number; sideboardSpaceRatio: number; mainDeckAbsoluteHeight: number; sideboardAbsoluteHeight: number } => {
  
  const cardHeight = BASE_CARD_HEIGHT * scale;
  const cardWidth = BASE_CARD_WIDTH * scale;
  
  const estimatedUniqueMainDeck = Math.ceil(mainDeckCount * 0.6);
  const estimatedUniqueSideboard = Math.ceil(sideboardCount * 0.7);
  
  // Calculate optimal columns for this card size - prefer fewer columns for larger cards
  const maxPossibleColumns = Math.floor((availableSpace.availableWidth - 20) / (cardWidth + 4));
  
  const mainDeckColumns = Math.min(6, Math.max(1, 
    estimatedUniqueMainDeck > 0 ? Math.min(maxPossibleColumns, Math.ceil(estimatedUniqueMainDeck / 3)) : 1
  ));
  
  const sideboardColumns = Math.min(4, Math.max(1,
    estimatedUniqueSideboard > 0 ? Math.min(maxPossibleColumns, Math.ceil(Math.sqrt(estimatedUniqueSideboard))) : 1
  ));
  
  const cardsPerMainColumn = estimatedUniqueMainDeck > 0 ? Math.ceil(estimatedUniqueMainDeck / mainDeckColumns) : 0;
  const cardsPerSideboardColumn = estimatedUniqueSideboard > 0 ? Math.ceil(estimatedUniqueSideboard / sideboardColumns) : 0;
  
  const mainDeckHeight = (cardsPerMainColumn * cardHeight) + (cardsPerMainColumn > 0 ? 40 : 0);
  const sideboardHeight = (cardsPerSideboardColumn * cardHeight) + (cardsPerSideboardColumn > 0 ? 40 : 0);
  
  // Calculate space ratios
  const totalHeight = mainDeckHeight + sideboardHeight;
  const mainDeckSpaceRatio = totalHeight > 0 ? mainDeckHeight / totalHeight : 0.7;
  const sideboardSpaceRatio = totalHeight > 0 ? sideboardHeight / totalHeight : 0.3;
  
  return {
    cardsPerMainColumn,
    cardsPerSideboardColumn,
    maxCardsPerColumn: Math.max(cardsPerMainColumn, cardsPerSideboardColumn),
    optimalCardHeight: cardHeight,
    optimalCardWidth: cardWidth,
    calculatedScale: scale,
    needsScrolling: false,
    mainDeckColumns,
    sideboardColumns,
    mainDeckSpaceRatio,
    sideboardSpaceRatio,
    mainDeckAbsoluteHeight: mainDeckHeight,
    sideboardAbsoluteHeight: sideboardHeight
  };
};

/**
 * Check if layout actually fits in DOM (can be called after rendering)
 */
export const doesLayoutFit = (): boolean => {
  const previewElement = document.getElementById('screenshot-preview');
  if (!previewElement) {
    return false;
  }
  
  const widthOverflow = previewElement.scrollWidth > previewElement.clientWidth;
  const heightOverflow = previewElement.scrollHeight > previewElement.clientHeight;
  
  const fits = !widthOverflow && !heightOverflow;
  
  if (!fits) {
    console.warn(`DOM validation: Layout overflows - width: ${widthOverflow}, height: ${heightOverflow}`);
  } else {
    console.log('✅ DOM validation: Layout fits perfectly');
  }
  
  return fits;
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
        resolve();
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
  
  const sortedEntries = Array.from(groups.entries()).sort(([, instancesA], [, instancesB]) => {
    const cardA = instancesA[0];
    const cardB = instancesB[0];
    
    if (cardA.cmc !== cardB.cmc) {
      return cardA.cmc - cardB.cmc;
    }
    
    return cardA.name.localeCompare(cardB.name);
  });
  
  const sortedGroups = new Map<string, DeckCardInstance[]>();
  sortedEntries.forEach(([cardId, instances]) => {
    sortedGroups.set(cardId, instances);
  });
  
  return sortedGroups;
};

/**
 * Arrange cards for screenshot layout with dynamic column distribution
 */
export const arrangeCardsForScreenshot = (
  mainDeck: DeckCardInstance[], 
  sideboard: DeckCardInstance[],
  mainDeckColumns: number = 12,
  sideboardColumns: number = 6
): ScreenshotLayout => {
  const mainDeckGroups = groupUniqueCards(mainDeck);
  const mainDeckCards = Array.from(mainDeckGroups.values()).map(instances => instances[0]);
  
  const sideboardGroups = groupUniqueCards(sideboard);
  const sideboardCards = Array.from(sideboardGroups.values()).map(instances => instances[0]);
  
  const mainDeckColumnArray: DeckCardInstance[][] = Array.from({ length: mainDeckColumns }, () => []);
  mainDeckCards.forEach((card, index) => {
    const columnIndex = index % mainDeckColumns;
    mainDeckColumnArray[columnIndex].push(card);
  });
  
  const sideboardColumnArray: DeckCardInstance[][] = Array.from({ length: sideboardColumns }, () => []);
  sideboardCards.forEach((card, index) => {
    const columnIndex = index % sideboardColumns;
    sideboardColumnArray[columnIndex].push(card);
  });
  
  return {
    mainDeckColumns: mainDeckColumnArray,
    sideboardColumns: sideboardColumnArray
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
    
    const canvasOptions = [
      {
        background: '#1a1a1a',
        useCORS: true,
        allowTaint: false,
        logging: false,
        scale: 2,
        width: element.scrollWidth,
        height: element.scrollHeight,
      },
      {
        background: '#1a1a1a',
        useCORS: false,
        allowTaint: true,
        logging: false,
        scale: 2,
        width: element.scrollWidth,
        height: element.scrollHeight,
      },
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
    
    return new Promise((resolve) => {
      canvas!.toBlob(resolve, 'image/png', 1.0);
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
  const sanitized = deckName
    .replace(/[^a-zA-Z0-9\-_\s]/g, '')
    .replace(/\s+/g, '_')
    .toLowerCase();
    
  const timestamp = new Date().toISOString().slice(0, 10);
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