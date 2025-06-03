#!/usr/bin/env python3
"""
Update ScreenshotModal.tsx with dynamic sizing functionality
"""

import os
import re

def update_screenshot_modal():
    """Update ScreenshotModal.tsx with dynamic sizing functionality"""
    
    modal_path = "src/components/ScreenshotModal.tsx"
    
    if not os.path.exists(modal_path):
        print(f"❌ Error: {modal_path} not found!")
        return
    
    print(f"Reading {modal_path}...")
    with open(modal_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update imports
    old_import = "import React, { useState, useMemo } from 'react';"
    new_import = "import React, { useState, useMemo, useEffect, useCallback } from 'react';"
    content = content.replace(old_import, new_import)
    
    # Update utility imports
    old_utils = '''import { 
  arrangeCardsForScreenshot, 
  getCardQuantityInGroup
} from '../utils/screenshotUtils';'''
    
    new_utils = '''import { 
  arrangeCardsForScreenshot, 
  getCardQuantityInGroup,
  measureAvailableSpace,
  calculateOptimalCardSize,
  determineScrollingNeeded,
  ViewportDimensions,
  CardLayoutCalculation,
  SIZE_OVERRIDES
} from '../utils/screenshotUtils';'''
    
    content = content.replace(old_utils, new_utils)
    
    # 2. Add new state after existing state
    old_state = '''  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);'''
    
    new_state = '''  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Dynamic sizing state
  const [sizeMode, setSizeMode] = useState<'auto' | 'small' | 'medium' | 'large'>('auto');
  const [viewportDimensions, setViewportDimensions] = useState<ViewportDimensions | null>(null);
  const [cardLayout, setCardLayout] = useState<CardLayoutCalculation | null>(null);'''
    
    content = content.replace(old_state, new_state)
    
    # 3. Add calculation effect and helper functions after existing useMemo hooks
    insertion_point = '''  }, [sideboard]);'''
    
    new_code = '''  }, [sideboard]);
  
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
  }, [mainDeck.length, sideboard.length]);
  
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
    
    content = content.replace(insertion_point, new_code)
    
    # 4. Update MagicCard rendering to use dynamic props
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
    
    # 5. Add size controls after deck name
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
    
    size_controls = '''        <div style={{ 
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
        </div>
        
        {/* Size Controls */}
        <div style={{
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
    
    content = content.replace(deck_name_section, size_controls)
    
    # 6. Update preview container to support scrolling
    old_preview = '''      <div id="screenshot-preview" className="screenshot-preview">'''
    new_preview = '''      <div 
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
    
    content = content.replace(old_preview, new_preview)
    
    # Write updated content
    with open(modal_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Updated {modal_path} with dynamic sizing functionality")

def main():
    """Main execution function"""
    print("🔧 Updating ScreenshotModal.tsx with dynamic sizing...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: src directory not found!")
        print("Please run this script from your project root directory (mtg-deckbuilder)")
        return
    
    try:
        update_screenshot_modal()
        
        print("\n" + "=" * 60)
        print("✅ ScreenshotModal.tsx update complete!")
        print("\n🎯 Features Added:")
        print("   • Auto-sizing cards to fit deck on screen")
        print("   • S/M/L override controls")
        print("   • Scrolling fallback for large decks")
        print("   • Real-time scale percentage display")
        print("\n🔧 Next Steps:")
        print("   1. Run 'npm start' to test the changes")
        print("   2. Open screenshot modal and test dynamic sizing")
        print("   3. Try S/M/L controls with different deck sizes")
        
    except Exception as e:
        print(f"\n❌ Error during update: {str(e)}")
        print("Please check the error message and try again.")

if __name__ == "__main__":
    main()
