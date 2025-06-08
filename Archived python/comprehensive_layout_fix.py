#!/usr/bin/env python3

import os
import sys

def comprehensive_layout_fix():
    """Fix all layout issues including search bar, colors layout, and other refinements"""
    
    success = True
    
    # Fix SearchAutocomplete.css - THE ROOT CAUSE
    search_css_file = "src/components/SearchAutocomplete.css"
    if os.path.exists(search_css_file):
        with open(search_css_file, 'r', encoding='utf-8') as f:
            search_css_content = f.read()
        
        # Fix the search input width overflow issue
        old_search_input = '''.search-autocomplete-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #555;
  border-radius: 4px;
  background: #2a2a2a;
  color: #e0e0e0;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}'''
        
        new_search_input = '''.search-autocomplete-input {
  width: 100%;
  max-width: 100%;
  padding: 6px 8px;
  border: 1px solid #555;
  border-radius: 3px;
  background: #2a2a2a;
  color: #e0e0e0;
  font-size: 12px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box !important;
}'''
        
        if old_search_input in search_css_content:
            search_css_content = search_css_content.replace(old_search_input, new_search_input)
            print("✅ Fixed search input width overflow with box-sizing: border-box")
        else:
            print("❌ Could not find search input styles to fix")
            success = False
        
        with open(search_css_file, 'w', encoding='utf-8') as f:
            f.write(search_css_content)
    else:
        print(f"❌ {search_css_file} not found")
        success = False
    
    # Update FilterPanel.tsx - Layout changes
    tsx_file = "src/components/FilterPanel.tsx"
    if os.path.exists(tsx_file):
        with open(tsx_file, 'r', encoding='utf-8') as f:
            tsx_content = f.read()
        
        # Fix 1: Change colors to single row centered with dropdown below
        old_colors_layout = '''            <div className="color-layout-horizontal">
              <div className="color-buttons-left">
                <div className="color-filter-grid-row1">
                  {['W', 'U', 'B', 'R', 'G'].map((color: string) => (
                    <button
                      key={color}
                      className={`color-button color-${color.toLowerCase()} ${
                        activeFilters.colors.includes(color) ? 'selected' : ''
                      }`}
                      onClick={() => handleColorSelection(color)}
                      title={`Toggle ${color} color filter`}
                    >
                      {color}
                    </button>
                  ))}
                </div>
                <div className="color-filter-grid-row2">
                  {['C'].map((color: string) => (
                    <button
                      key={color}
                      className={`color-button color-${color.toLowerCase()} ${
                        activeFilters.colors.includes(color) ? 'selected' : ''
                      } ${
                        color === 'C' && activeFilters.isGoldMode ? 'disabled' : ''
                      }`}
                      onClick={() => handleColorSelection(color)}
                      disabled={color === 'C' && activeFilters.isGoldMode}
                      title={
                        color === 'C' && activeFilters.isGoldMode 
                          ? "Colorless cannot be used with multicolor filter" 
                          : `Toggle ${color} color filter`
                      }
                    >
                      {color}
                    </button>
                  ))}
                  <GoldButton
                    isSelected={activeFilters.isGoldMode}
                    onClick={() => handleColorSelection('GOLD')}
                    disabled={activeFilters.colors.includes('C')}
                  />
                </div>
              </div>
              <div className="color-dropdown-right">
                <select
                  value={activeFilters.colorIdentity}
                  onChange={(e) => onFilterChange('colorIdentity', e.target.value)}
                  className="color-mode-select"
                >
                  <option value="exact">Exactly these colors</option>
                  <option value="include">Include these colors</option>
                  <option value="subset">At most these colors</option>
                </select>
              </div>
            </div>'''
        
        new_colors_layout = '''            <div className="color-layout-vertical">
              <div className="color-buttons-row">
                {['W', 'U', 'B', 'R', 'G', 'C'].map((color: string) => (
                  <button
                    key={color}
                    className={`color-button color-${color.toLowerCase()} ${
                      activeFilters.colors.includes(color) ? 'selected' : ''
                    } ${
                      color === 'C' && activeFilters.isGoldMode ? 'disabled' : ''
                    }`}
                    onClick={() => handleColorSelection(color)}
                    disabled={color === 'C' && activeFilters.isGoldMode}
                    title={
                      color === 'C' && activeFilters.isGoldMode 
                        ? "Colorless cannot be used with multicolor filter" 
                        : `Toggle ${color} color filter`
                    }
                  >
                    {color}
                  </button>
                ))}
                <GoldButton
                  isSelected={activeFilters.isGoldMode}
                  onClick={() => handleColorSelection('GOLD')}
                  disabled={activeFilters.colors.includes('C')}
                />
              </div>
              <div className="color-dropdown-below">
                <select
                  value={activeFilters.colorIdentity}
                  onChange={(e) => onFilterChange('colorIdentity', e.target.value)}
                  className="color-mode-select"
                >
                  <option value="exact">Exactly these colors</option>
                  <option value="include">Include these colors</option>
                  <option value="subset">At most these colors</option>
                </select>
              </div>
            </div>'''
        
        if old_colors_layout in tsx_content:
            tsx_content = tsx_content.replace(old_colors_layout, new_colors_layout)
            print("✅ Changed colors to single row with dropdown below")
        else:
            print("❌ Could not find colors layout to change")
            success = False
        
        with open(tsx_file, 'w', encoding='utf-8') as f:
            f.write(tsx_content)
    else:
        print(f"❌ {tsx_file} not found")
        success = False
    
    # Update GoldButton.tsx - Remove "GOLD" text
    gold_file = "src/components/GoldButton.tsx"
    if os.path.exists(gold_file):
        with open(gold_file, 'r', encoding='utf-8') as f:
            gold_content = f.read()
        
        # Remove GOLD text content
        old_gold_content = '>GOLD<'
        new_gold_content = '><'
        
        if old_gold_content in gold_content:
            gold_content = gold_content.replace(old_gold_content, new_gold_content)
            print("✅ Removed GOLD text from gold button")
        else:
            # Try alternative pattern
            old_gold_alt = '>{children || "GOLD"}<'
            new_gold_alt = '><'
            if old_gold_alt in gold_content:
                gold_content = gold_content.replace(old_gold_alt, new_gold_alt)
                print("✅ Removed GOLD text from gold button (alternative pattern)")
            else:
                print("❌ Could not find GOLD text to remove")
                success = False
        
        with open(gold_file, 'w', encoding='utf-8') as f:
            f.write(gold_content)
    else:
        print(f"❌ {gold_file} not found")
        success = False
    
    # Update useCards.ts - Change default color mode and More Types state
    cards_file = "src/hooks/useCards.ts"
    if os.path.exists(cards_file):
        with open(cards_file, 'r', encoding='utf-8') as f:
            cards_content = f.read()
        
        # Change default colorIdentity to 'subset'
        old_color_default = "colorIdentity: 'exact'"
        new_color_default = "colorIdentity: 'subset'"
        
        if old_color_default in cards_content:
            cards_content = cards_content.replace(old_color_default, new_color_default)
            print("✅ Changed default color mode to 'subset' (At most these colors)")
        else:
            print("❌ Could not find color identity default to change")
            success = False
        
        # Change default subtypes section state to collapsed
        old_subtypes_state = "subtypes: true"
        new_subtypes_state = "subtypes: false"
        
        if old_subtypes_state in cards_content:
            cards_content = cards_content.replace(old_subtypes_state, new_subtypes_state)
            print("✅ Changed More Types to default collapsed")
        else:
            print("❌ Could not find subtypes section state to change")
            success = False
        
        with open(cards_file, 'w', encoding='utf-8') as f:
            f.write(cards_content)
    else:
        print(f"❌ {cards_file} not found")
        success = False
    
    # Update FilterPanel.css - Layout styling updates
    css_file = "src/components/FilterPanel.css"
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Add new color layout styles
        new_color_styles = '''
/* Color Layout - Single Row Vertical */
.color-layout-vertical {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.color-buttons-row {
  display: flex;
  gap: 3px;
  justify-content: center;
  flex-wrap: nowrap;
}

.color-dropdown-below {
  width: 100%;
  text-align: center;
}

.color-dropdown-below .color-mode-select {
  width: auto;
  min-width: 140px;
  padding: 3px 6px;
  background: #1a1a1a;
  border: 1px solid #404040;
  border-radius: 3px;
  color: white;
  font-size: 10px;
}
'''
        
        if '.color-layout-vertical' not in css_content:
            css_content += new_color_styles
            print("✅ Added single row color layout styles")
        
        # Fix creature stats alignment
        old_stat_row = '''.stat-row span:first-child {
  font-size: 11px;
  color: #cccccc;
  min-width: 50px;
  text-align: left;
}'''
        
        new_stat_row = '''.stat-row span:first-child {
  font-size: 11px;
  color: #cccccc;
  min-width: 65px;
  text-align: left;
}'''
        
        if old_stat_row in css_content:
            css_content = css_content.replace(old_stat_row, new_stat_row)
            print("✅ Fixed creature stats label alignment")
        else:
            print("❌ Could not find stat row styling to fix")
            success = False
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
    else:
        print(f"❌ {css_file} not found")
        success = False
    
    if success:
        print("\n🎉 COMPREHENSIVE LAYOUT FIX COMPLETE!")
        print("   ✅ FIXED SEARCH BAR: Added box-sizing: border-box to prevent overflow")
        print("   ✅ Colors: Single row centered with dropdown below")
        print("   ✅ Default color mode: 'At most these colors'")
        print("   ✅ More Types: Default collapsed")
        print("   ✅ Creature stats: Better label alignment")
        print("   ✅ Gold button: Removed text completely")
    else:
        print("❌ Some fixes could not be applied - please check the output above")
    
    return success

if __name__ == "__main__":
    success = comprehensive_layout_fix()
    sys.exit(0 if success else 1)