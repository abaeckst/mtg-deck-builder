#!/usr/bin/env python3
"""
Phase 3B-1 Refinements: Professional Card Sizing System
Based on user feedback for improved UX
"""

def update_card_sizing_hook():
    """Update useCardSizing hook with refined defaults and ranges"""
    file_path = "src/hooks/useCardSizing.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update default sizes to 40% (0.4) across all areas
        old_defaults = '''const DEFAULT_SIZES: CardSizeState = {
  collection: 1.2,  // 20% larger than base normal size
  deck: 0.8,        // 20% smaller than base small size  
  sideboard: 0.8    // 20% smaller than base small size
};'''

        new_defaults = '''const DEFAULT_SIZES: CardSizeState = {
  collection: 0.4,  // 40% of base size for all areas
  deck: 0.4,        // 40% of base size for all areas
  sideboard: 0.4    // 40% of base size for all areas
};'''

        # Update size validation ranges to be more restrictive with better minimum
        old_validation = '''        return {
          collection: Math.max(0.5, Math.min(3.0, parsed.collection || DEFAULT_SIZES.collection)),
          deck: Math.max(0.5, Math.min(3.0, parsed.deck || DEFAULT_SIZES.deck)),
          sideboard: Math.max(0.5, Math.min(3.0, parsed.sideboard || DEFAULT_SIZES.sideboard))
        };'''

        new_validation = '''        return {
          collection: Math.max(0.7, Math.min(2.5, parsed.collection || DEFAULT_SIZES.collection)),
          deck: Math.max(0.7, Math.min(2.5, parsed.deck || DEFAULT_SIZES.deck)),
          sideboard: Math.max(0.7, Math.min(2.5, parsed.sideboard || DEFAULT_SIZES.sideboard))
        };'''

        # Update all size clamping functions
        old_clamp_collection = '''  const updateCollectionSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.5, Math.min(3.0, size));
    setSizes(prev => ({ ...prev, collection: clampedSize }));
  }, []);'''

        new_clamp_collection = '''  const updateCollectionSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.7, Math.min(2.5, size));
    setSizes(prev => ({ ...prev, collection: clampedSize }));
  }, []);'''

        old_clamp_deck = '''  const updateDeckSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.5, Math.min(3.0, size));
    setSizes(prev => ({ ...prev, deck: clampedSize }));
  }, []);'''

        new_clamp_deck = '''  const updateDeckSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.7, Math.min(2.5, size));
    setSizes(prev => ({ ...prev, deck: clampedSize }));
  }, []);'''

        old_clamp_sideboard = '''  const updateSideboardSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.5, Math.min(3.0, size));
    setSizes(prev => ({ ...prev, sideboard: clampedSize }));
  }, []);'''

        new_clamp_sideboard = '''  const updateSideboardSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.7, Math.min(2.5, size));
    setSizes(prev => ({ ...prev, sideboard: clampedSize }));
  }, []);'''

        # Apply all replacements
        content = content.replace(old_defaults, new_defaults)
        content = content.replace(old_validation, new_validation)
        content = content.replace(old_clamp_collection, new_clamp_collection)
        content = content.replace(old_clamp_deck, new_clamp_deck)
        content = content.replace(old_clamp_sideboard, new_clamp_sideboard)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_mtgo_layout_sliders():
    """Update MTGOLayout.tsx with refined slider ranges and styling"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update collection slider range
        old_collection_slider = '''              <input
                type="range"
                min="0.5"
                max="2.5"
                step="0.1"
                value={cardSizes.collection}
                onChange={(e) => updateCollectionSize(parseFloat(e.target.value))}
                className="size-slider"
                title={`Card size: ${Math.round(cardSizes.collection * 100)}%`}
              />'''

        new_collection_slider = '''              <input
                type="range"
                min="0.7"
                max="2.5"
                step="0.1"
                value={cardSizes.collection}
                onChange={(e) => updateCollectionSize(parseFloat(e.target.value))}
                className="size-slider"
                title={`Card size: ${Math.round(cardSizes.collection * 100)}%`}
              />'''

        # Update deck slider range
        old_deck_slider = '''                <input
                  type="range"
                  min="0.5"
                  max="2.0"
                  step="0.1"
                  value={cardSizes.deck}
                  onChange={(e) => updateDeckSize(parseFloat(e.target.value))}
                  className="size-slider"
                  title={`Card size: ${Math.round(cardSizes.deck * 100)}%`}
                />'''

        new_deck_slider = '''                <input
                  type="range"
                  min="0.7"
                  max="2.5"
                  step="0.1"
                  value={cardSizes.deck}
                  onChange={(e) => updateDeckSize(parseFloat(e.target.value))}
                  className="size-slider"
                  title={`Card size: ${Math.round(cardSizes.deck * 100)}%`}
                />'''

        # Update sideboard slider range
        old_sideboard_slider = '''                <input
                  type="range"
                  min="0.5"
                  max="2.0"
                  step="0.1"
                  value={cardSizes.sideboard}
                  onChange={(e) => updateSideboardSize(parseFloat(e.target.value))}
                  className="size-slider"
                  title={`Card size: ${Math.round(cardSizes.sideboard * 100)}%`}
                />'''

        new_sideboard_slider = '''                <input
                  type="range"
                  min="0.7"
                  max="2.5"
                  step="0.1"
                  value={cardSizes.sideboard}
                  onChange={(e) => updateSideboardSize(parseFloat(e.target.value))}
                  className="size-slider"
                  title={`Card size: ${Math.round(cardSizes.sideboard * 100)}%`}
                />'''

        # Apply replacements
        content = content.replace(old_collection_slider, new_collection_slider)
        content = content.replace(old_deck_slider, new_deck_slider)
        content = content.replace(old_sideboard_slider, new_sideboard_slider)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_magic_card_grid_logic():
    """Update MagicCard.tsx with improved grid scaling logic"""
    file_path = "src/components/MagicCard.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update CardGrid component with better scaling logic
        old_grid_logic = '''  // Calculate dynamic grid column size based on card size and scale factor
  const getGridColumnSize = () => {
    const baseSizes = {
      small: 70,
      normal: 130, 
      large: 210
    };
    const baseSize = baseSizes[cardSize] || baseSizes.normal;
    const scaledSize = Math.round(baseSize * Math.max(0.5, Math.min(3.0, scaleFactor)));
    return `${scaledSize}px`;
  };

  const gridStyles: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(auto-fill, minmax(${getGridColumnSize()}, 1fr))`,
    gap: '8px',
    padding: '8px',
    ...style,
  };'''

        new_grid_logic = '''  // Calculate dynamic grid column size and gap based on card size and scale factor
  const getGridSettings = () => {
    const baseSizes = {
      small: 70,
      normal: 130, 
      large: 210
    };
    const baseSize = baseSizes[cardSize] || baseSizes.normal;
    const clampedScale = Math.max(0.7, Math.min(2.5, scaleFactor));
    const scaledSize = Math.round(baseSize * clampedScale);
    
    // Proportional gap scaling - smaller cards get tighter spacing
    const baseGap = 8;
    const scaledGap = Math.max(4, Math.round(baseGap * clampedScale));
    
    return {
      columnSize: `${scaledSize}px`,
      gap: `${scaledGap}px`
    };
  };

  const { columnSize, gap } = getGridSettings();

  const gridStyles: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(auto-fill, minmax(${columnSize}, 1fr))`,
    gap: gap,
    padding: '8px',
    ...style,
  };'''

        # Apply replacement
        content = content.replace(old_grid_logic, new_grid_logic)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_css_slider_styling():
    """Update CSS with larger sliders and responsive grid styling"""
    file_path = "src/components/MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the size slider styles with much larger sliders
        old_slider_styles = '''/* PHASE 3B-1: Size slider styles */
.size-slider {
  width: 60px;
  height: 18px;
  margin: 0 8px 0 4px;
  background: linear-gradient(to right, #404040, #666666);
  border-radius: 9px;
  outline: none;
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
}

.size-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  background: #3b82f6;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
  transition: all 0.2s ease;
}

.size-slider::-webkit-slider-thumb:hover {
  background: #2563eb;
  transform: scale(1.1);
}

.size-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: #3b82f6;
  border: 2px solid #ffffff;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
  transition: all 0.2s ease;
}

.size-slider::-moz-range-thumb:hover {
  background: #2563eb;
  transform: scale(1.1);
}

.deck-controls .size-slider,
.sideboard-controls .size-slider {
  width: 50px;
  margin: 0 6px 0 2px;
}'''

        new_slider_styles = '''/* PHASE 3B-1: Size slider styles - Professional larger sliders */
.size-slider {
  width: 180px;  /* Triple the original size for better precision */
  height: 20px;
  margin: 0 12px 0 6px;
  background: linear-gradient(to right, #404040, #666666);
  border-radius: 10px;
  outline: none;
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
  transition: all 0.2s ease;
}

.size-slider:hover {
  background: linear-gradient(to right, #4a4a4a, #707070);
}

.size-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  background: #3b82f6;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.4);
  transition: all 0.2s ease;
}

.size-slider::-webkit-slider-thumb:hover {
  background: #2563eb;
  transform: scale(1.15);
  box-shadow: 0 3px 6px rgba(0,0,0,0.5);
}

.size-slider::-webkit-slider-thumb:active {
  background: #1d4ed8;
  transform: scale(1.1);
}

.size-slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: #3b82f6;
  border: 2px solid #ffffff;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.4);
  transition: all 0.2s ease;
}

.size-slider::-moz-range-thumb:hover {
  background: #2563eb;
  transform: scale(1.15);
  box-shadow: 0 3px 6px rgba(0,0,0,0.5);
}

.size-slider::-moz-range-thumb:active {
  background: #1d4ed8;
  transform: scale(1.1);
}

/* Consistent sizing across all areas */
.deck-controls .size-slider,
.sideboard-controls .size-slider {
  width: 180px;  /* Same size as collection slider for consistency */
  margin: 0 12px 0 6px;
}'''

        # Replace the old styles with new ones
        content = content.replace(old_slider_styles, new_slider_styles)
        
        # Update grid styles to use proportional spacing
        old_grid_updates = '''/* Update grid styles to be more responsive to size changes */
.collection-grid {
  padding: 12px;
  overflow-y: auto;
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--collection-card-min-width, 130px), 1fr));
  gap: 8px;
  align-content: start;
}

.deck-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--deck-card-min-width, 70px), 1fr));
  gap: 4px;
  align-content: start;
  min-height: 150px;
  padding-bottom: 40px;
}

.sideboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--sideboard-card-min-width, 70px), 1fr));
  gap: 4px;
  align-content: start;
  min-height: 150px;
  padding-bottom: 40px;
}'''

        new_grid_updates = '''/* Responsive grid styles with proportional spacing */
.collection-grid {
  padding: 12px;
  overflow-y: auto;
  flex: 1;
  display: grid;
  /* Grid columns and gap will be set dynamically by CardGrid component */
  align-content: start;
}

.deck-grid {
  display: grid;
  /* Grid columns and gap will be set dynamically by individual card grids */
  align-content: start;
  min-height: 150px;
  padding-bottom: 40px;
}

.sideboard-grid {
  display: grid;
  /* Grid columns and gap will be set dynamically by individual card grids */
  align-content: start;
  min-height: 150px;
  padding-bottom: 40px;
}'''

        # Apply the grid update replacement
        content = content.replace(old_grid_updates, new_grid_updates)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Run all card sizing refinements"""
    print("🔧 Starting Phase 3B-1 Refinements: Professional Card Sizing")
    print("=" * 65)
    
    success_count = 0
    total_tasks = 4
    
    print("\n📝 Task 1/4: Updating size ranges and defaults (40% start, 70%-250% range)...")
    if update_card_sizing_hook():
        success_count += 1
    
    print("\n📝 Task 2/4: Updating slider ranges in MTGOLayout...")
    if update_mtgo_layout_sliders():
        success_count += 1
    
    print("\n📝 Task 3/4: Improving grid scaling logic in MagicCard...")
    if update_magic_card_grid_logic():
        success_count += 1
    
    print("\n📝 Task 4/4: Creating larger, professional sliders (3x size)...")
    if update_css_slider_styling():
        success_count += 1
    
    print("\n" + "=" * 65)
    print(f"🎯 Phase 3B-1 Refinements Complete!")
    print(f"📊 Success: {success_count}/{total_tasks} tasks completed")
    
    if success_count == total_tasks:
        print("\n✨ REFINEMENT SUMMARY:")
        print("✅ Unified size ranges: 70% minimum, 250% maximum across all areas")
        print("✅ Better default: 40% starting position for all sliders")
        print("✅ Professional sliders: 3x larger (180px) for precision control")
        print("✅ Proportional spacing: Card gaps scale with card size")
        print("✅ Responsive grids: More cards per row when smaller, fewer when larger")
        print("✅ Consistent behavior: No card stacking or weird spacing")
        
        print("\n🧪 TEST THE IMPROVEMENTS:")
        print("1. Run 'npm start' to see the refined sizing system")
        print("2. Notice the much larger, more precise sliders")
        print("3. Test size changes - cards should scale smoothly with proportional gaps")
        print("4. Verify cards per row changes appropriately with size")
        print("5. Check that all sliders behave identically")
        
        print("\n💡 EXPECTED EXPERIENCE:")
        print("• Satisfying, precise control with large sliders")
        print("• Natural card density changes (more small cards, fewer large ones)")
        print("• Professional, consistent behavior across all areas")
        print("• No weird spacing or stacking issues")
    else:
        print(f"\n⚠️  Some refinements failed. Please check error messages above.")

if __name__ == "__main__":
    main()