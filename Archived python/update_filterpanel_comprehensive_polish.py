#!/usr/bin/env python3

import os
import sys

def update_filterpanel_comprehensive_polish():
    """Polish FilterPanel.tsx for professional MTGO appearance and enhanced functionality"""
    
    filename = "src/components/FilterPanel.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Updates for comprehensive polish
    updates = [
        # 1. Update terminology from CMC to Mana Value (MV)
        (
            '        {/* CMC Group - Always Visible */}\n        <div className="filter-group">\n          <label>Mana Cost (CMC)</label>',
            '        {/* Mana Value Group - Collapsible */}\n        <CollapsibleSection\n          title="MANA VALUE (MV)"\n          isExpanded={getSectionState(\'cmc\')}\n          hasActiveFilters={activeFilters.cmc.min !== null || activeFilters.cmc.max !== null}\n          onToggle={() => updateSectionState(\'cmc\', !getSectionState(\'cmc\'))}\n        >\n          <div className="filter-group">\n            <label>Range</label>',
            "Change CMC to Mana Value (MV) and make it collapsible"
        ),
        
        # 2. Close the CMC/Mana Value collapsible section
        (
            '            />\n          </div>\n        </div>',
            '            />\n          </div>\n          </div>\n        </CollapsibleSection>',
            "Close Mana Value collapsible section"
        ),
        
        # 3. Make Colors section collapsible
        (
            '        {/* Colors Group - Always Visible */}\n        <div className="filter-group">\n          <label>Colors</label>',
            '        {/* Colors Group - Collapsible */}\n        <CollapsibleSection\n          title="COLORS"\n          isExpanded={getSectionState(\'colors\')}\n          hasActiveFilters={activeFilters.colors.length > 0 || activeFilters.isGoldMode}\n          onToggle={() => updateSectionState(\'colors\', !getSectionState(\'colors\'))}\n        >\n          <div className="filter-group">',
            "Make Colors section collapsible"
        ),
        
        # 4. Update color grid layout for proper 2-row arrangement
        (
            '            <div className="color-filter-grid">',
            '            <div className="color-filter-grid-row1">\n              {/* Row 1: W U B R G */}',
            "Start first row of colors"
        ),
        
        # 5. Add second row for colorless and gold
        (
            '              ))}',
            '              ).slice(0, 5)}\n            </div>\n            <div className="color-filter-grid-row2">\n              {/* Row 2: Colorless and Gold */}\n              {[\'C\'].map((color: string) =>',
            "Split colors into two rows"
        ),
        
        # 6. Move gold button to second row and close colors section
        (
            '              <GoldButton\n                isSelected={activeFilters.isGoldMode}\n                onClick={() => handleColorSelection(\'GOLD\')}\n                disabled={activeFilters.colors.includes(\'C\')}\n              />\n            </div>',
            '              )}\n              <GoldButton\n                isSelected={activeFilters.isGoldMode}\n                onClick={() => handleColorSelection(\'GOLD\')}\n                disabled={activeFilters.colors.includes(\'C\')}\n              />\n            </div>',
            "Complete second row structure"
        ),
        
        # 7. Close colors collapsible section
        (
            '            </select>\n          </div>\n        </div>',
            '            </select>\n          </div>\n        </CollapsibleSection>',
            "Close Colors collapsible section"
        ),
        
        # 8. Make Card Types section collapsible
        (
            '        {/* Card Types Group - Always Visible */}\n        <div className="filter-group">\n          <label>Card Types</label>',
            '        {/* Card Types Group - Collapsible */}\n        <CollapsibleSection\n          title="CARD TYPES"\n          isExpanded={getSectionState(\'types\')}\n          hasActiveFilters={activeFilters.types.length > 0}\n          onToggle={() => updateSectionState(\'types\', !getSectionState(\'types\'))}\n        >\n          <div className="filter-group">',
            "Make Card Types section collapsible"
        ),
        
        # 9. Close card types collapsible section
        (
            '            })}\n          </div>\n        </div>',
            '            })}\n          </div>\n        </CollapsibleSection>',
            "Close Card Types collapsible section"
        ),
        
        # 10. Make More Types section collapsible
        (
            '        {/* More Types (Subtypes) Group - Always Visible */}\n        <div className="filter-group">\n          <label>More Types</label>',
            '        {/* More Types (Subtypes) Group - Collapsible */}\n        <CollapsibleSection\n          title="MORE TYPES"\n          isExpanded={getSectionState(\'subtypes\')}\n          hasActiveFilters={activeFilters.subtypes.length > 0}\n          onToggle={() => updateSectionState(\'subtypes\', !getSectionState(\'subtypes\'))}\n        >\n          <div className="filter-group">',
            "Make More Types section collapsible"
        ),
        
        # 11. Close more types collapsible section
        (
            '          />\n        </div>',
            '          />\n          </div>\n        </CollapsibleSection>',
            "Close More Types collapsible section"
        ),
        
        # 12. Add minimum width constraint to prevent horizontal scrolling
        (
            '    <div className="mtgo-filter-panel" style={{ width }}>',
            '    <div className="mtgo-filter-panel" style={{ width, minWidth: \'280px\' }}>',
            "Add minimum width to prevent horizontal scrolling"
        ),
        
        # 13. Improve search bar container
        (
            '        <div className="filter-group">\n          <label>Search</label>',
            '        <div className="filter-group search-group">\n          <label>Search</label>',
            "Add search-group class for better styling"
        ),
        
        # 14. Update class names for better organization
        (
            '        {/* Format Group - Always Visible */}\n        <div className="filter-group">',
            '        {/* Format Group - Always Visible */}\n        <div className="filter-group format-group">',
            "Add format-group class"
        ),
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_filterpanel_comprehensive_polish()
    sys.exit(0 if success else 1)