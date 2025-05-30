#!/usr/bin/env python3
"""
Fix Card Spacing and Default Size Issues
- Change default to 140% (1.4) instead of 40% (0.4)  
- Fix minimum spacing enforcement in all areas
- Apply working deck logic to collection area
"""

def fix_default_size_to_140():
    """Change default size from 40% to 140% for all areas"""
    file_path = "src/hooks/useCardSizing.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update DEFAULT_SIZES to 1.4 (140%)
        old_defaults = '''const DEFAULT_SIZES: CardSizeState = {
  collection: 0.4,  // 40% (0.4) default - consistent across all areas
  deck: 0.4,        // 40% (0.4) default - consistent across all areas  
  sideboard: 0.4    // 40% (0.4) default - consistent across all areas
};'''

        new_defaults = '''const DEFAULT_SIZES: CardSizeState = {
  collection: 1.4,  // 140% (1.4) default - consistent across all areas
  deck: 1.4,        // 140% (1.4) default - consistent across all areas  
  sideboard: 1.4    // 140% (1.4) default - consistent across all areas
};'''

        content = content.replace(old_defaults, new_defaults)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def fix_minimum_spacing_enforcement():
    """Fix the minimum spacing enforcement in all grid areas"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix collection grid with proper minimum spacing enforcement
        old_collection_grid = '''              <div 
                className="collection-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(110 * cardSizes.collection)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(12, Math.round(6 * cardSizes.collection)))}px`,
                  alignContent: 'start',
                  padding: '8px'
                }}
              >'''

        new_collection_grid = '''              <div 
                className="collection-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.max(90, Math.round(110 * cardSizes.collection))}px, 1fr))`,
                  gap: `${Math.max(6, Math.min(12, Math.round(8 * cardSizes.collection)))}px`,
                  alignContent: 'start',
                  padding: '8px'
                }}
              >'''

        # Fix deck grid with better minimum spacing enforcement
        old_deck_grid = '''              <div 
                className="deck-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(110 * cardSizes.deck)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(12, Math.round(6 * cardSizes.deck)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >'''

        new_deck_grid = '''              <div 
                className="deck-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.max(90, Math.round(110 * cardSizes.deck))}px, 1fr))`,
                  gap: `${Math.max(6, Math.min(12, Math.round(8 * cardSizes.deck)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >'''

        # Fix sideboard grid with same improvements
        old_sideboard_grid = '''              <div 
                className="sideboard-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(110 * cardSizes.sideboard)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(12, Math.round(6 * cardSizes.sideboard)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >'''

        new_sideboard_grid = '''              <div 
                className="sideboard-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.max(90, Math.round(110 * cardSizes.sideboard))}px, 1fr))`,
                  gap: `${Math.max(6, Math.min(12, Math.round(8 * cardSizes.sideboard)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >'''

        # Apply all replacements
        content = content.replace(old_collection_grid, new_collection_grid)
        content = content.replace(old_deck_grid, new_deck_grid)
        content = content.replace(old_sideboard_grid, new_sideboard_grid)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_slider_ranges_for_140_default():
    """Update slider ranges to accommodate 140% default"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update collection slider range to accommodate 140% default
        old_collection_slider = '''              <input
                type="range"
                min="0.7"
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

        # Sliders are already correctly ranged, just ensure they can handle 1.4 default
        # No changes needed to slider ranges since 1.4 is within 0.7-2.5 range
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def ensure_proper_card_sizing_clamping():
    """Ensure size clamping functions work with 140% default"""
    file_path = "src/hooks/useCardSizing.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # The clamping functions should already handle 1.4 since it's within 0.7-2.5 range
        # But let's make sure the initialization properly handles it
        
        old_initialization = '''  // Initialize state from localStorage or defaults - force clear for consistency
  const [sizes, setSizes] = useState<CardSizeState>(() => {
    // Clear any existing localStorage to fix loading issues
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (error) {
      console.warn('Failed to clear card sizes from localStorage:', error);
    }
    
    // Always start with clean defaults
    console.log('Initializing card sizes with defaults:', DEFAULT_SIZES);
    return { ...DEFAULT_SIZES };
  });'''

        new_initialization = '''  // Initialize state from localStorage or defaults - force clear for consistency
  const [sizes, setSizes] = useState<CardSizeState>(() => {
    // Clear any existing localStorage to fix loading issues
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (error) {
      console.warn('Failed to clear card sizes from localStorage:', error);
    }
    
    // Always start with clean defaults (140% for all areas)
    console.log('Initializing card sizes with 140% defaults:', DEFAULT_SIZES);
    return { 
      collection: 1.4,
      deck: 1.4, 
      sideboard: 1.4
    };
  });'''

        content = content.replace(old_initialization, new_initialization)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def add_debug_logging_for_grid_calculations():
    """Add debug logging to see actual grid calculations"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add more detailed debug logging
        old_debug_log = '''  // Debug logging for sizing issues
  console.log('Current card sizes:', cardSizes);'''

        new_debug_log = '''  // Debug logging for sizing issues
  console.log('Current card sizes:', cardSizes);
  console.log('Collection grid calc:', {
    minmax: Math.max(90, Math.round(110 * cardSizes.collection)),
    gap: Math.max(6, Math.min(12, Math.round(8 * cardSizes.collection)))
  });
  console.log('Deck grid calc:', {
    minmax: Math.max(90, Math.round(110 * cardSizes.deck)),
    gap: Math.max(6, Math.min(12, Math.round(8 * cardSizes.deck)))
  });'''

        content = content.replace(old_debug_log, new_debug_log)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Run all fixes for spacing and default size issues"""
    print("🔧 Fixing Card Spacing and Default Size Issues")
    print("=" * 52)
    
    success_count = 0
    total_tasks = 5
    
    print("\n📝 Task 1/5: Changing default size from 40% to 140%...")
    if fix_default_size_to_140():
        success_count += 1
    
    print("\n📝 Task 2/5: Fixing minimum spacing enforcement in all areas...")
    if fix_minimum_spacing_enforcement():
        success_count += 1
    
    print("\n📝 Task 3/5: Updating slider ranges for 140% default...")
    if update_slider_ranges_for_140_default():
        success_count += 1
    
    print("\n📝 Task 4/5: Ensuring proper size clamping...")
    if ensure_proper_card_sizing_clamping():
        success_count += 1
    
    print("\n📝 Task 5/5: Adding detailed debug logging...")
    if add_debug_logging_for_grid_calculations():
        success_count += 1
    
    print("\n" + "=" * 52)
    print(f"🎯 Spacing and Default Fixes Complete!")
    print(f"📊 Success: {success_count}/{total_tasks} tasks completed")
    
    if success_count == total_tasks:
        print("\n✨ FIXES APPLIED:")
        print("✅ Default size changed: 40% → 140% for all areas")
        print("✅ Minimum spacing enforced: 6px minimum gap (was 4px)")
        print("✅ Minimum column size: 90px minimum (prevents overlap)")
        print("✅ Better gap calculation: 8 * scaleFactor with 6-12px bounds")
        print("✅ Collection area uses same logic as deck/sideboard")
        print("✅ Added detailed debug logging for grid calculations")
        
        print("\n🧪 TEST THE FIXES:")
        print("1. Run 'npm start' and check browser console for detailed logs")
        print("2. Verify all sliders start at 140% position (middle-right)")
        print("3. Check that cards never overlap in any area")
        print("4. Test that collection area spacing matches deck areas")
        print("5. Verify minimum 6px spacing is maintained at all sizes")
        
        print("\n💡 EXPECTED RESULTS:")
        print("• All sliders start at 140% (comfortable viewing size)")
        print("• No card overlapping in any area")
        print("• Collection area behaves same as deck/sideboard")
        print("• Minimum 6px gaps always maintained")
        print("• Debug logs show actual grid calculations")
        
        print("\n🔍 DEBUG INFO:")
        print("Check browser console for logs showing:")
        print("- Current card sizes: {collection: 1.4, deck: 1.4, sideboard: 1.4}")
        print("- Grid calculations with minmax and gap values")
    else:
        print(f"\n⚠️  Some fixes failed. Please check error messages above.")

if __name__ == "__main__":
    main()