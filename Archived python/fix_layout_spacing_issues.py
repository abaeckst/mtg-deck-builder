#!/usr/bin/env python3

import os
import sys

def fix_layout_spacing_issues():
    """Fix the real layout and spacing issues based on user feedback"""
    
    success = True
    
    # Update FilterPanel.tsx - Fix colors section layout structure
    tsx_file = "src/components/FilterPanel.tsx"
    if os.path.exists(tsx_file):
        with open(tsx_file, 'r', encoding='utf-8') as f:
            tsx_content = f.read()
        
        # Fix colors section layout - color buttons left, dropdown right
        old_colors_layout = '''        <CollapsibleSection
          title="COLORS"
          previewText={getSectionState('colors') ? '' : getPreviewText('colors')}
          isExpanded={getSectionState('colors')}
          hasActiveFilters={activeFilters.colors.length > 0 || activeFilters.isGoldMode}
          onToggle={() => updateSectionState('colors', !getSectionState('colors'))}
        >
          <div className="filter-group">
            <div className="color-identity-controls">
              <div className="color-filter-grid-row1">
                {/* Row 1: W U B R G */}
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
                {/* Row 2: Colorless and Gold */}
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
          </div>
        </CollapsibleSection>'''
        
        new_colors_layout = '''        <CollapsibleSection
          title="COLORS"
          previewText={getSectionState('colors') ? '' : getPreviewText('colors')}
          isExpanded={getSectionState('colors')}
          hasActiveFilters={activeFilters.colors.length > 0 || activeFilters.isGoldMode}
          onToggle={() => updateSectionState('colors', !getSectionState('colors'))}
        >
          <div className="filter-group">
            <div className="color-layout-horizontal">
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
            </div>
          </div>
        </CollapsibleSection>'''
        
        if old_colors_layout in tsx_content:
            tsx_content = tsx_content.replace(old_colors_layout, new_colors_layout)
            print("✅ Restructured colors section layout")
        else:
            print("❌ Could not find colors section layout to restructure")
            success = False
        
        with open(tsx_file, 'w', encoding='utf-8') as f:
            f.write(tsx_content)
    else:
        print(f"❌ {tsx_file} not found")
        success = False
    
    # Update FilterPanel.css - Fix all the spacing and layout issues
    css_file = "src/components/FilterPanel.css"
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Fix 1: Search container - proper constraints
        old_search_styles = '''/* Search Group Enhanced Styling */
.search-group {
  margin-bottom: 12px;
}

.search-group .search-input {
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}'''
        
        new_search_styles = '''/* Search Group - Compact and Contained */
.search-group {
  margin-bottom: 4px;
  padding: 0 4px;
  box-sizing: border-box;
  width: 100%;
  overflow: hidden;
}

.search-group .search-autocomplete {
  width: 100% !important;
  max-width: calc(100% - 8px) !important;
  box-sizing: border-box !important;
}

.search-group .search-input {
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  padding: 6px 8px !important;
  font-size: 11px !important;
}'''
        
        if old_search_styles in css_content:
            css_content = css_content.replace(old_search_styles, new_search_styles)
            print("✅ Fixed search container width and spacing")
        else:
            print("❌ Could not find search styles to fix")
            success = False
        
        # Fix 2: Format group - remove excessive spacing
        old_format_styles = '''/* Format Group Styling */
.format-group select {
  width: 100%;
  padding: 6px 8px;
  background: #1a1a1a;
  border: 1px solid #404040;
  border-radius: 4px;
  color: white;
  font-size: 12px;
}'''
        
        new_format_styles = '''/* Format Group - Compact */
.format-group {
  margin-bottom: 4px;
}

.format-group select {
  width: 100%;
  padding: 4px 6px;
  background: #1a1a1a;
  border: 1px solid #404040;
  border-radius: 3px;
  color: white;
  font-size: 11px;
}'''
        
        if old_format_styles in css_content:
            css_content = css_content.replace(old_format_styles, new_format_styles)
            print("✅ Made format group more compact")
        else:
            print("❌ Could not find format styles to compact")
            success = False
        
        # Fix 3: Add new color layout styles
        color_layout_styles = '''
/* Color Layout - Horizontal Split */
.color-layout-horizontal {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  justify-content: space-between;
}

.color-buttons-left {
  flex-shrink: 0;
}

.color-dropdown-right {
  flex: 1;
  min-width: 120px;
}

.color-dropdown-right .color-mode-select {
  width: 100%;
  padding: 4px 6px;
  background: #1a1a1a;
  border: 1px solid #404040;
  border-radius: 3px;
  color: white;
  font-size: 10px;
}
'''
        
        if '.color-layout-horizontal' not in css_content:
            css_content += color_layout_styles
            print("✅ Added horizontal color layout styles")
        
        # Fix 4: Gold button - force actual black text
        old_gold_button = '''.color-gold {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  border: 2px solid #FFD700 !important;
  color: #000000;
  font-weight: 900;
  font-size: 10px;
  text-shadow: 1px 1px 1px rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
  transition: all 0.2s ease;
}'''
        
        new_gold_button = '''.color-gold {
  background: #FFD700 !important;
  border: 1px solid #B8860B !important;
  color: #000000 !important;
  font-weight: 900 !important;
  font-size: 9px !important;
  text-shadow: none !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
  transition: all 0.2s ease;
}'''
        
        if old_gold_button in css_content:
            css_content = css_content.replace(old_gold_button, new_gold_button)
            print("✅ Fixed gold button to use solid black text")
        else:
            print("❌ Could not find gold button styles to fix")
            success = False
        
        # Fix 5: Center mana value inputs
        old_range_filter = '''.range-filter {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
}

.range-filter span {
  font-size: 11px;
  color: #cccccc;
  min-width: 20px;
  text-align: center;
}'''
        
        new_range_filter = '''.range-filter {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 2px;
}

.range-filter span {
  font-size: 11px;
  color: #cccccc;
  min-width: 20px;
  text-align: center;
}'''
        
        if old_range_filter in css_content:
            css_content = css_content.replace(old_range_filter, new_range_filter)
            print("✅ Centered mana value input row")
        else:
            print("❌ Could not find range filter styles to center")
            success = False
        
        # Fix 6: Remove excessive spacing from filter groups
        filter_group_fix = '''
/* Filter Group Spacing Fix */
.filter-group {
  margin-bottom: 0 !important;
  padding: 0 !important;
}

.filter-group label {
  font-size: 10px !important;
  margin-bottom: 2px !important;
  display: block;
  color: #cccccc;
}

/* Collapsible section spacing */
.collapsible-section {
  border-bottom: none;
  margin-bottom: 2px;
}
'''
        
        if '/* Filter Group Spacing Fix */' not in css_content:
            css_content += filter_group_fix
            print("✅ Added filter group spacing fixes")
        
        # Fix 7: Update color grid to work with new layout
        old_color_grid_spacing = '''.color-filter-grid-row1,
.color-filter-grid-row2 {
  display: flex;
  gap: 4px;
  margin-bottom: 3px;
  justify-content: center;
}'''
        
        new_color_grid_spacing = '''.color-filter-grid-row1,
.color-filter-grid-row2 {
  display: flex;
  gap: 3px;
  margin-bottom: 2px;
  justify-content: flex-start;
}

.color-filter-grid-row2 {
  margin-bottom: 0;
}'''
        
        if old_color_grid_spacing in css_content:
            css_content = css_content.replace(old_color_grid_spacing, new_color_grid_spacing)
            print("✅ Updated color grid spacing for horizontal layout")
        else:
            print("❌ Could not find color grid spacing to update")
            success = False
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
    else:
        print(f"❌ {css_file} not found")
        success = False
    
    if success:
        print("\n🎉 LAYOUT AND SPACING FIXES COMPLETE!")
        print("   ✅ Fixed search bar width constraints properly")
        print("   ✅ Streamlined Search/Format/Colors sections spacing")
        print("   ✅ Restructured colors: buttons left, dropdown right")
        print("   ✅ Fixed gold button to solid black text")
        print("   ✅ Centered mana value Min/Max inputs")
        print("   ✅ Removed excessive vertical spacing throughout")
    else:
        print("❌ Some fixes could not be applied - please check the output above")
    
    return success

if __name__ == "__main__":
    success = fix_layout_spacing_issues()
    sys.exit(0 if success else 1)