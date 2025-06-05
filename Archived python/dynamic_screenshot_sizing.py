#!/usr/bin/env python3
"""
Dynamic Screenshot Layout Implementation Script
Updates ScreenshotModal.tsx and screenshotUtils.ts to add dynamic sizing functionality
"""

import os
import re

def update_screenshot_utils():
    """Add dynamic sizing utilities to screenshotUtils.ts"""
    
    utils_path = "src/utils/screenshotUtils.ts"
    
    if not os.path.exists(utils_path):
        print(f"Creating new {utils_path} file...")
        content = ""
    else:
        print(f"Reading existing {utils_path}...")
        with open(utils_path, 'r', encoding='utf-8') as f:
            content = f.read()
    
    # Add new interfaces and constants at the top
    new_interfaces = '''import { DeckCardInstance } from '../types/card';

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

'''
    
    # Add new utility functions
    new_functions = '''
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

'''
    
    # If file doesn't exist or is empty, create it with full content
    if not content.strip():
        content = new_interfaces + new_functions
    else:
        # Add interfaces at the top if not already present
        if 'ViewportDimensions' not in content:
            # Find the first import or add at the beginning
            import_match = re.search(r'^import.*?;', content, re.MULTILINE)
            if import_match:
                insert_pos = import_match.end()
                content = content[:insert_pos] + '\n\n' + new_interfaces + content[insert_pos:]
            else:
                content = new_interfaces + '\n' + content
        
        # Add functions if not already present
        if 'measureAvailableSpace' not in content:
            content += new_functions
    
    # Write updated content
    with open(utils_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Updated {utils_path} with dynamic sizing utilities")

def update_screenshot_modal():
    """Update ScreenshotModal.tsx with dynamic sizing functionality"""
    
    modal_path = "src/components/ScreenshotModal.tsx"
    
    if not os.path.exists(modal_path):
        print(f"❌ Error: {modal_path} not found!")
        return
    
    print(f"Reading {modal_path}...")
    with open(modal_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add new imports
    import_section = "import React, { useState, useMemo } from 'react';"
    new_import_section = "import React, { useState, useMemo, useEffect, useCallback } from 'react';"
    
    content = content.replace(import_section, new_import_section)
    
    # Add new utility imports
    utils_import_old = '''import { 
  arrangeCardsForScreenshot, 
  getCardQuantityInGroup
} from '../utils/screenshotUtils';'''
    
    utils_import_new = '''import { 
  arrangeCardsForScreenshot, 
  getCardQuantityInGroup,
  measureAvailableSpace,
  calculateOptimalCardSize,
  determineScrollingNeeded,
  ViewportDimensions,
  CardLayoutCalculation,
  SizeOverride,
  SIZE_OVERRIDES
} from '../utils/screenshotUtils';'''
    
    content = content.replace(utils_import_old, utils_import_new)
    
    # 2. Add new state variables after existing state
    state_section = '''  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);'''
    
    new_state_section = '''  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Dynamic sizing state
  const [sizeMode, setSizeMode] = useState<'auto' | 'small' | 'medium' | 'large'>('auto');
  const [viewportDimensions, setViewportDimensions] = useState<ViewportDimensions | null>(null);
  const [cardLayout, setCardLayout] = useState<CardLayoutCalculation | null>(null);'''
    
    content = content.replace(state_section, new_state_section)
    
    # 3. Add calculation useEffect after existing useMemo hooks
    effect_insertion_point = '''  }, [sideboard]);'''
    
    calculation_effect = '''  }, [sideboard]);
  
  // Dynamic size calculation effect
  useEffect(() => {
    const handleResize = () => {
      const dimensions = measureAvailableSpace();
      const layout = calculateOptimalCardSize(mainDeck.length, sideboard.length, dimensions);
      setViewportDimensions(dimensions);
      setCardLayout(layout);
    };
    
    // Calculate on mount and when deck changes
    handleResize();
    
    // Recalculate on window resize
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [mainDeck.length, sideboard.length]);'''
    
    content = content.replace(effect_insertion_point, calculation_effect)
    
    # 4. Add final card props calculation function
    card_props_function = '''
  // Calculate final card props based on auto calculation and user override
  const getFinalCardProps = useCallback(() => {
    if (!cardLayout) return { size: 'normal' as const, scaleFactor: 1.0 };
    
    let finalScale = cardLayout.calculatedScale;
    
    if (sizeMode !== 'auto') {
      finalScale = SIZE_OVERRIDES[sizeMode];
    }
    
    return {
      size: finalScale > 0.8 ? 'normal' as const : 'small' as const,
      scaleFactor: finalScale
    };
  }, [cardLayout, sizeMode]);
  
  const cardProps = getFinalCardProps();
  const needsScrolling = cardLayout ? determineScrollingNeeded(
    cardLayout.calculatedScale, 
    sizeMode !== 'auto' ? SIZE_OVERRIDES[sizeMode] : null
  ) : false;'''
    
    # Insert before handleSaveImage function
    handle_save_insertion = '''  const handleSaveImage = async () => {'''
    content = content.replace(handle_save_insertion, card_props_function + '\n\n  ' + handle_save_insertion)
    
    # 5. Update card rendering to use dynamic props
    old_magic_card = '''        <MagicCard
          card={cardForMagicCard}
          size="small"
          scaleFactor={0.8}
          showQuantity={quantity > 1}
          quantity={quantity}
          // Use undefined for availableQuantity to only show orange deck quantity badges
          availableQuantity={undefined}
          selectable={false}
          selected={false}
          disabled={false}
        />'''
    
    new_magic_card = '''        <MagicCard
          card={cardForMagicCard}
          size={cardProps.size}
          scaleFactor={cardProps.scaleFactor}
          showQuantity={quantity > 1}
          quantity={quantity}
          // Use undefined for availableQuantity to only show orange deck quantity badges
          availableQuantity={undefined}
          selectable={false}
          selected={false}
          disabled={false}
        />'''
    
    content = content.replace(old_magic_card, new_magic_card)
    
    # 6. Add size controls after deck name but before main deck section
    size_controls_html = '''        
        {/* Size Controls */}
        <div className="screenshot-size-controls" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginBottom: '12px',
          fontSize: '14px',
          color: '#e0e0e0',
          padding: '8px 12px',
          background: '#2a2a2a',
          borderRadius: '4px',
          border: '1px solid #444'
        }}>
          <span>Size:</span>
          <button 
            className={sizeMode === 'auto' ? 'active' : ''}
            onClick={() => setSizeMode('auto')}
            style={{
              padding: '4px 8px',
              background: sizeMode === 'auto' ? '#3b82f6' : '#2a2a2a',
              border: `1px solid ${sizeMode === 'auto' ? '#3b82f6' : '#444'}`,
              borderRadius: '4px',
              color: '#e0e0e0',
              cursor: 'pointer'
            }}
          >
            Auto
          </button>
          <button 
            className={sizeMode === 'small' ? 'active' : ''}
            onClick={() => setSizeMode('small')}
            style={{
              padding: '4px 8px',
              background: sizeMode === 'small' ? '#3b82f6' : '#2a2a2a',
              border: `1px solid ${sizeMode === 'small' ? '#3b82f6' : '#444'}`,
              borderRadius: '4px',
              color: '#e0e0e0',
              cursor: 'pointer'
            }}
          >
            S
          </button>
          <button 
            className={sizeMode === 'medium' ? 'active' : ''}
            onClick={() => setSizeMode('medium')}
            style={{
              padding: '4px 8px',
              background: sizeMode === 'medium' ? '#3b82f6' : '#2a2a2a',
              border: `1px solid ${sizeMode === 'medium' ? '#3b82f6' : '#444'}`,
              borderRadius: '4px',
              color: '#e0e0e0',
              cursor: 'pointer'
            }}
          >
            M
          </button>
          <button 
            className={sizeMode === 'large' ? 'active' : ''}
            onClick={() => setSizeMode('large')}
            style={{
              padding: '4px 8px',
              background: sizeMode === 'large' ? '#3b82f6' : '#2a2a2a',
              border: `1px solid ${sizeMode === 'large' ? '#3b82f6' : '#444'}`,
              borderRadius: '4px',
              color: '#e0e0e0',
              cursor: 'pointer'
            }}
          >
            L
          </button>
          {cardLayout && (
            <span style={{ marginLeft: '12px', fontSize: '12px', color: '#999' }}>
              Scale: {Math.round(cardProps.scaleFactor * 100)}%
              {needsScrolling && ' (Scrolling enabled)'}
            </span>
          )}
        </div>'''
    
    # Insert size controls after deck name
    deck_name_end = '''        </div>'''
    deck_name_section = '''        <div style={{ 
          color: '#e0e0e0', 
          fontSize: '24px', 
          fontWeight: 'bold', 
          marginBottom: '16px',
          textAlign: 'center',
          background: '#1a1a1a',
          padding: '12px',
          borderRadius: '6px',
          border: '1px solid #333'
        }}>
          {deckName}
        </div>'''
    
    replacement = deck_name_section + size_controls_html
    content = content.replace(deck_name_section, replacement)
    
    # 7. Update preview container to support scrolling
    old_preview_start = '''      <div id="screenshot-preview" className="screenshot-preview">'''
    new_preview_start = '''      <div 
        id="screenshot-preview" 
        className="screenshot-preview"
        style={{
          maxHeight: needsScrolling ? '90vh' : 'auto',
          overflowY: needsScrolling ? 'auto' : 'hidden',
          padding: needsScrolling ? '12px' : '8px',
          background: '#1a1a1a',
          borderRadius: '8px',
          border: '1px solid #333'
        }}
      >'''
    
    content = content.replace(old_preview_start, new_preview_start)
    
    # 8. Update layout containers to be more flexible
    old_deck_layout = '''            <div className="screenshot-deck-layout" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(5, 1fr)',
              gap: '4px',
              marginBottom: '20px',
              padding: '8px',
              background: '#1e1e1e',
              borderRadius: '6px',
              border: '1px solid #333',
              maxHeight: '60vh',
              overflow: 'hidden'
            }}>'''
    
    new_deck_layout = '''            <div className="screenshot-deck-layout" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(5, 1fr)',
              gap: '4px',
              marginBottom: '20px',
              padding: '8px',
              background: '#1e1e1e',
              borderRadius: '6px',
              border: '1px solid #333',
              maxHeight: needsScrolling ? 'none' : '60vh',
              overflow: 'visible'
            }}>'''
    
    content = content.replace(old_deck_layout, new_deck_layout)
    
    old_sideboard_layout = '''            <div className="screenshot-sideboard-layout" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(2, 1fr)',
              gap: '4px',
              padding: '8px',
              background: '#1e1e1e',
              borderRadius: '6px',
              border: '1px solid #333',
              maxHeight: '25vh',
              overflow: 'hidden'
            }}>'''
    
    new_sideboard_layout = '''            <div className="screenshot-sideboard-layout" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(2, 1fr)',
              gap: '4px',
              padding: '8px',
              background: '#1e1e1e',
              borderRadius: '6px',
              border: '1px solid #333',
              maxHeight: needsScrolling ? 'none' : '25vh',
              overflow: 'visible'
            }}>'''
    
    content = content.replace(old_sideboard_layout, new_sideboard_layout)
    
    # Write updated content
    with open(modal_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Updated {modal_path} with dynamic sizing functionality")

def update_modal_css():
    """Add scrollbar styling for screenshot modal"""
    
    css_path = "src/components/modal.css"
    
    if not os.path.exists(css_path):
        print(f"❌ Error: {css_path} not found!")
        return
    
    print(f"Reading {css_path}...")
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add scrollbar styles if not already present
    scrollbar_css = '''
/* Screenshot modal scrollbar styling */
.screenshot-preview::-webkit-scrollbar {
  width: 8px;
}

.screenshot-preview::-webkit-scrollbar-track {
  background: #2a2a2a;
  border-radius: 4px;
}

.screenshot-preview::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.screenshot-preview::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Size controls styling */
.screenshot-size-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #e0e0e0;
}

.screenshot-size-controls button {
  padding: 4px 8px;
  background: #2a2a2a;
  border: 1px solid #444;
  border-radius: 4px;
  color: #e0e0e0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.screenshot-size-controls button:hover {
  background: #333;
  border-color: #555;
}

.screenshot-size-controls button.active {
  background: #3b82f6;
  border-color: #3b82f6;
}
'''
    
    if '.screenshot-preview::-webkit-scrollbar' not in content:
        content += scrollbar_css
        
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated {css_path} with screenshot scrollbar styling")
    else:
        print(f"ℹ️ {css_path} already contains screenshot styling")

def main():
    """Main execution function"""
    print("🚀 Starting Dynamic Screenshot Layout Implementation...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: src directory not found!")
        print("Please run this script from your project root directory (mtg-deckbuilder)")
        return
    
    try:
        # Update files in order
        update_screenshot_utils()
        update_screenshot_modal()
        update_modal_css()
        
        print("\n" + "=" * 60)
        print("✅ Dynamic Screenshot Layout Implementation Complete!")
        print("\n🎯 New Features Added:")
        print("   • Auto-sizing cards to fit all deck cards on screen")
        print("   • S/M/L override controls for manual fine-tuning")
        print("   • Scrolling fallback when cards would be too small")
        print("   • Responsive behavior for different screen sizes")
        print("   • Real-time scale percentage display")
        print("\n🔧 Next Steps:")
        print("   1. Run 'npm start' to test the changes")
        print("   2. Open screenshot modal and verify dynamic sizing")
        print("   3. Test with different deck sizes (empty, partial, full)")
        print("   4. Test S/M/L override controls")
        print("   5. Test window resizing behavior")
        
    except Exception as e:
        print(f"\n❌ Error during implementation: {str(e)}")
        print("Please check the error message and try again.")

if __name__ == "__main__":
    main()
