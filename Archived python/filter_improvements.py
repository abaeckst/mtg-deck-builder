# Phase 3C Filter Improvements
# 1. Change color default to "exactly these colors"
# 2. Add colorless option
# 3. Fix clear button to reset search results

import os
import re

def fix_color_default():
    """Change default color mode to 'exact' instead of 'include'"""
    
    # Read the current useCards.ts file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the initial state default
    old_initial_state = '''    activeFilters: {
      format: '',
      colors: [],
      colorIdentity: 'include',
      types: [],
      rarity: [],
      sets: [],
      cmc: { min: null, max: null },
      power: { min: null, max: null },
      toughness: { min: null, max: null },
    },'''
    
    new_initial_state = '''    activeFilters: {
      format: '',
      colors: [],
      colorIdentity: 'exact',
      types: [],
      rarity: [],
      sets: [],
      cmc: { min: null, max: null },
      power: { min: null, max: null },
      toughness: { min: null, max: null },
    },'''
    
    content = content.replace(old_initial_state, new_initial_state)
    
    # Fix the clearAllFilters function
    old_clear_filters = '''  const clearAllFilters = useCallback(() => {
    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'include',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
    }));
  }, []);'''
    
    new_clear_filters = '''  const clearAllFilters = useCallback(() => {
    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
    }));
  }, []);'''
    
    content = content.replace(old_clear_filters, new_clear_filters)
    
    # Fix the clearCards function
    old_clear_cards = '''      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'include',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },'''
    
    new_clear_cards = '''      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },'''
    
    content = content.replace(old_clear_cards, new_clear_cards)
    
    # Write the updated file
    with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Changed color default to 'exact'")

def add_colorless_option():
    """Add colorless option to the color filter"""
    
    # Read the current MTGOLayout.tsx file
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the color filter grid
    old_color_grid = '''              <div className="color-identity-controls">
                <div className="color-filter-grid">
                  {['W', 'U', 'B', 'R', 'G'].map((color: string) => (
                    <button
                      key={color}
                      className={`color-button color-${color.toLowerCase()} ${
                        activeFilters.colors.includes(color) ? 'selected' : ''
                      }`}
                      onClick={() => {
                        const newColors = activeFilters.colors.includes(color)
                          ? activeFilters.colors.filter((c: string) => c !== color)
                          : [...activeFilters.colors, color];
                        handleFilterChange('colors', newColors);
                      }}
                    >
                      {color}
                    </button>
                  ))}
                </div>'''
    
    new_color_grid = '''              <div className="color-identity-controls">
                <div className="color-filter-grid">
                  {['W', 'U', 'B', 'R', 'G', 'C'].map((color: string) => (
                    <button
                      key={color}
                      className={`color-button color-${color.toLowerCase()} ${
                        activeFilters.colors.includes(color) ? 'selected' : ''
                      }`}
                      onClick={() => {
                        const newColors = activeFilters.colors.includes(color)
                          ? activeFilters.colors.filter((c: string) => c !== color)
                          : [...activeFilters.colors, color];
                        handleFilterChange('colors', newColors);
                      }}
                    >
                      {color}
                    </button>
                  ))}
                </div>'''
    
    content = content.replace(old_color_grid, new_color_grid)
    
    # Update the color mode select default
    old_color_mode = '''                <select
                  value={activeFilters.colorIdentity}
                  onChange={(e) => handleFilterChange('colorIdentity', e.target.value)}
                  className="color-mode-select"
                >
                  <option value="include">Include these colors</option>
                  <option value="exact">Exactly these colors</option>
                  <option value="subset">At most these colors</option>
                </select>'''
    
    new_color_mode = '''                <select
                  value={activeFilters.colorIdentity}
                  onChange={(e) => handleFilterChange('colorIdentity', e.target.value)}
                  className="color-mode-select"
                >
                  <option value="exact">Exactly these colors</option>
                  <option value="include">Include these colors</option>
                  <option value="subset">At most these colors</option>
                </select>'''
    
    content = content.replace(old_color_mode, new_color_mode)
    
    # Write the updated file
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added colorless (C) option and reordered color mode select")

def add_colorless_css():
    """Add CSS styling for the colorless button"""
    
    # Read the current MTGOLayout.css file
    with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the mana color specific styling section and add colorless
    old_color_styles = '''/* Mana Color Specific Styling */
.color-button.color-w { background-color: #fffbd5; color: #000000; }
.color-button.color-u { background-color: #0e68ab; }
.color-button.color-b { background-color: #150b00; }
.color-button.color-r { background-color: #d3202a; }
.color-button.color-g { background-color: #00733e; }'''
    
    new_color_styles = '''/* Mana Color Specific Styling */
.color-button.color-w { background-color: #fffbd5; color: #000000; }
.color-button.color-u { background-color: #0e68ab; }
.color-button.color-b { background-color: #150b00; }
.color-button.color-r { background-color: #d3202a; }
.color-button.color-g { background-color: #00733e; }
.color-button.color-c { background-color: #ccc2c0; color: #000000; }'''
    
    content = content.replace(old_color_styles, new_color_styles)
    
    # Update the color filter grid to handle 6 colors instead of 5
    old_grid_style = '''.color-filter-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 4px;
}'''
    
    new_grid_style = '''.color-filter-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 4px;
}'''
    
    content = content.replace(old_grid_style, new_grid_style)
    
    # Write the updated file
    with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added colorless CSS styling")

def fix_colorless_api_handling():
    """Update the API to handle colorless properly"""
    
    # Read the current scryfallApi.ts file
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the color filter handling section
    old_color_handling = '''  // Add color identity filters with advanced logic
  if (filters.colors && filters.colors.length > 0) {
    const colorQuery = filters.colors.join('');
    const colorMode = filters.colorIdentity || 'include';
    
    switch (colorMode) {
      case 'exact':
        searchQuery += ` color=${colorQuery}`;
        break;
      case 'subset':
        searchQuery += ` color<=${colorQuery}`;
        break;
      case 'include':
      default:
        searchQuery += ` color:${colorQuery}`;
        break;
    }
  }'''
    
    new_color_handling = '''  // Add color identity filters with advanced logic
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
              searchQuery += ` (color=C OR color=${otherColors})`;
            } else {
              searchQuery += ` color=C`;
            }
            break;
          case 'subset':
            searchQuery += ` color<=${otherColors}C`;
            break;
          case 'include':
          default:
            searchQuery += ` (color:C OR color:${otherColors})`;
            break;
        }
      } else {
        // Only colorless selected
        searchQuery += ` color=C`;
      }
    } else {
      // No colorless, handle normally
      const colorQuery = filters.colors.join('');
      const colorMode = filters.colorIdentity || 'exact';
      
      switch (colorMode) {
        case 'exact':
          searchQuery += ` color=${colorQuery}`;
          break;
        case 'subset':
          searchQuery += ` color<=${colorQuery}`;
          break;
        case 'include':
        default:
          searchQuery += ` color:${colorQuery}`;
          break;
      }
    }
  }'''
    
    content = content.replace(old_color_handling, new_color_handling)
    
    # Write the updated file
    with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated API to handle colorless properly")

def fix_clear_button():
    """Fix the clear button to reset search results"""
    
    # Read the current useCards.ts file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the clearAllFilters function to also trigger a search reset
    old_clear_all = '''  const clearAllFilters = useCallback(() => {
    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
    }));
  }, []);'''
    
    new_clear_all = '''  const clearAllFilters = useCallback(() => {
    console.log('🧹 Clearing all filters and resetting search');
    setState(prev => ({
      ...prev,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },
    }));
    
    // Reset search results to popular cards after clearing filters
    setTimeout(() => {
      console.log('🧹 Loading popular cards after filter clear');
      loadPopularCards();
    }, 50);
  }, [loadPopularCards]);'''
    
    content = content.replace(old_clear_all, new_clear_all)
    
    # Write the updated file
    with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed clear button to reset search results")

def main():
    """Execute all filter improvements"""
    try:
        print("🔧 Applying Phase 3C Filter Improvements")
        print("=" * 50)
        
        print("\n📋 Fix 1: Changing color default to 'exact'...")
        fix_color_default()
        
        print("\n📋 Fix 2: Adding colorless (C) option...")
        add_colorless_option()
        
        print("\n📋 Fix 3: Adding colorless CSS styling...")
        add_colorless_css()
        
        print("\n📋 Fix 4: Updating API for colorless handling...")
        fix_colorless_api_handling()
        
        print("\n📋 Fix 5: Fixing clear button to reset results...")
        fix_clear_button()
        
        print("\n" + "=" * 50)
        print("✅ All Filter Improvements Complete!")
        print("\n🎯 Changes Made:")
        print("   • Color mode now defaults to 'Exactly these colors'")
        print("   • Added colorless (C) button with proper styling")
        print("   • Color grid now shows 6 buttons (W/U/B/R/G/C)")
        print("   • API properly handles colorless searches")
        print("   • Clear button now resets search results to popular cards")
        print("\n🧪 Test These:")
        print("   1. Click 'R' (Red) → should show only red cards")
        print("   2. Click 'C' (Colorless) → should show only colorless cards")
        print("   3. Click 'Clear' → should reset filters AND show popular cards")
        print("   4. Color mode should default to 'Exactly these colors'")
        
    except Exception as e:
        print(f"\n❌ Error during improvements: {e}")
        print("Please check the file paths and try again.")

if __name__ == "__main__":
    main()
