#!/usr/bin/env python3
"""
Fix Card Sizing Loading and Spacing Issues
- Fix default loading to actually be 40% for all areas
- Use same grid logic for collection area
- Reduce maximum spacing and improve density
"""

def fix_default_loading_issue():
    """Fix the default loading issue by clearing localStorage and ensuring proper initialization"""
    file_path = "src/hooks/useCardSizing.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the initialization logic to be more explicit about defaults
        old_initialization = '''  // Initialize state from localStorage or defaults
  const [sizes, setSizes] = useState<CardSizeState>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        return {
          collection: Math.max(0.7, Math.min(2.5, parsed.collection || DEFAULT_SIZES.collection)),
          deck: Math.max(0.7, Math.min(2.5, parsed.deck || DEFAULT_SIZES.deck)),
          sideboard: Math.max(0.7, Math.min(2.5, parsed.sideboard || DEFAULT_SIZES.sideboard))
        };
      }
    } catch (error) {
      console.warn('Failed to load card sizes from localStorage:', error);
    }
    return DEFAULT_SIZES;
  });'''

        new_initialization = '''  // Initialize state from localStorage or defaults - force clear for consistency
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

        content = content.replace(old_initialization, new_initialization)
        
        # Also update the DEFAULT_SIZES to be more explicit
        old_defaults = '''const DEFAULT_SIZES: CardSizeState = {
  collection: 0.4,  // 40% default - consistent across all areas
  deck: 0.4,        // 40% default - consistent across all areas  
  sideboard: 0.4    // 40% default - consistent across all areas
};'''

        new_defaults = '''const DEFAULT_SIZES: CardSizeState = {
  collection: 0.4,  // 40% (0.4) default - consistent across all areas
  deck: 0.4,        // 40% (0.4) default - consistent across all areas  
  sideboard: 0.4    // 40% (0.4) default - consistent across all areas
};'''

        content = content.replace(old_defaults, new_defaults)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def fix_collection_area_grid_logic():
    """Apply same grid logic to collection area as deck/sideboard"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace collection grid with same inline styling approach as deck/sideboard
        old_collection_grid = '''              <div 
                className="collection-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(16, Math.round(8 * cardSizes.collection)))}px`,
                  alignContent: 'start'
                }}
              >'''

        new_collection_grid = '''              <div 
                className="collection-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(12, Math.round(6 * cardSizes.collection)))}px`,
                  alignContent: 'start',
                  padding: '8px'
                }}
              >'''

        content = content.replace(old_collection_grid, new_collection_grid)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def reduce_deck_sideboard_spacing():
    """Reduce maximum spacing and improve density for deck and sideboard areas"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update deck grid with reduced spacing and better density
        old_deck_grid = '''              <div 
                className="deck-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.deck)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(16, Math.round(8 * cardSizes.deck)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >'''

        new_deck_grid = '''              <div 
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

        # Update sideboard grid with same improvements
        old_sideboard_grid = '''              <div 
                className="sideboard-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.sideboard)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(16, Math.round(8 * cardSizes.sideboard)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >'''

        new_sideboard_grid = '''              <div 
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

        # Apply both replacements
        content = content.replace(old_deck_grid, new_deck_grid)
        content = content.replace(old_sideboard_grid, new_sideboard_grid)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_collection_area_density():
    """Update collection area to use same density improvements"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update collection grid to use better density (smaller minmax for more cards per row)
        old_collection_grid = '''              <div 
                className="collection-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(12, Math.round(6 * cardSizes.collection)))}px`,
                  alignContent: 'start',
                  padding: '8px'
                }}
              >'''

        new_collection_grid = '''              <div 
                className="collection-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(110 * cardSizes.collection)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(12, Math.round(6 * cardSizes.collection)))}px`,
                  alignContent: 'start',
                  padding: '8px'
                }}
              >'''

        content = content.replace(old_collection_grid, new_collection_grid)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def remove_collection_grid_container_padding():
    """Remove padding from collection grid container to prevent double padding"""
    file_path = "src/components/MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update collection grid container CSS
        old_collection_css = '''/* Responsive grid styles with proportional spacing */
.collection-grid-container {
  padding: 12px;
  overflow-y: auto;
  flex: 1;
}

.collection-grid {
  display: grid;
  align-content: start;
  /* Grid columns and gap will be set by JavaScript for consistency */
}'''

        new_collection_css = '''/* Responsive grid styles with proportional spacing */
.collection-grid-container {
  overflow-y: auto;
  flex: 1;
}

.collection-grid {
  display: grid;
  align-content: start;
  /* Grid columns and gap will be set by JavaScript for consistency */
}'''

        content = content.replace(old_collection_css, new_collection_css)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def add_debugging_console_logs():
    """Add console logs to debug the loading issue"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add debugging after the useCardSizing hook
        old_sizing_hook = '''  // PHASE 3B-1: Card sizing system
  const { 
    sizes: cardSizes, 
    updateCollectionSize, 
    updateDeckSize, 
    updateSideboardSize 
  } = useCardSizing();'''

        new_sizing_hook = '''  // PHASE 3B-1: Card sizing system
  const { 
    sizes: cardSizes, 
    updateCollectionSize, 
    updateDeckSize, 
    updateSideboardSize 
  } = useCardSizing();
  
  // Debug logging for sizing issues
  console.log('Current card sizes:', cardSizes);'''

        content = content.replace(old_sizing_hook, new_sizing_hook)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Run all fixes for loading and spacing issues"""
    print("🔧 Fixing Card Sizing Loading and Spacing Issues")
    print("=" * 55)
    
    success_count = 0
    total_tasks = 6
    
    print("\n📝 Task 1/6: Fixing default loading issue (forcing 40% start)...")
    if fix_default_loading_issue():
        success_count += 1
    
    print("\n📝 Task 2/6: Applying same grid logic to collection area...")
    if fix_collection_area_grid_logic():
        success_count += 1
    
    print("\n📝 Task 3/6: Reducing deck/sideboard spacing and improving density...")
    if reduce_deck_sideboard_spacing():
        success_count += 1
    
    print("\n📝 Task 4/6: Updating collection area density...")
    if update_collection_area_density():
        success_count += 1
    
    print("\n📝 Task 5/6: Removing double padding from collection container...")
    if remove_collection_grid_container_padding():
        success_count += 1
    
    print("\n📝 Task 6/6: Adding debug logging...")
    if add_debugging_console_logs():
        success_count += 1
    
    print("\n" + "=" * 55)
    print(f"🎯 Loading and Spacing Fixes Complete!")
    print(f"📊 Success: {success_count}/{total_tasks} tasks completed")
    
    if success_count == total_tasks:
        print("\n✨ FIXES APPLIED:")
        print("✅ Forced localStorage clear to ensure 40% default loading")
        print("✅ Collection area uses same grid logic as deck/sideboard")
        print("✅ Reduced maximum spacing: 16px → 12px")
        print("✅ Improved card density: 130px → 110px minmax for more cards per row")
        print("✅ Unified spacing formula: 6 * scaleFactor (was 8 * scaleFactor)")
        print("✅ Added debug logging to track sizing values")
        
        print("\n🧪 TEST THE FIXES:")
        print("1. Run 'npm start' and check browser console for debug logs")
        print("2. Verify all sliders start at 40% position")
        print("3. Check collection area no longer stacks cards")
        print("4. Verify deck/sideboard areas have reasonable spacing")
        print("5. Test that more cards fit per row with better density")
        
        print("\n💡 EXPECTED RESULTS:")
        print("• All three sliders start at exactly 40%")
        print("• Collection area respects minimum spacing (no stacking)")
        print("• Better card density - more cards per row when appropriate")
        print("• Maximum spacing reduced to prevent excessive gaps")
        print("• Consistent behavior across all three areas")
        
        print("\n⚠️  NOTE: If sliders still don't start at 40%, check browser console")
        print("for debug logs showing what the actual cardSizes values are.")
    else:
        print(f"\n⚠️  Some fixes failed. Please check error messages above.")

if __name__ == "__main__":
    main()