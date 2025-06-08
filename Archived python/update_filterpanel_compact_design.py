#!/usr/bin/env python3

import os
import sys

def update_filterpanel_compact_design():
    """Implement Option B+C: Inline controls + accordion with mini previews for vertical space efficiency"""
    
    success = True
    
    # Update FilterPanel.tsx - Add preview text functionality to CollapsibleSection
    tsx_file = "src/components/FilterPanel.tsx"
    if os.path.exists(tsx_file):
        with open(tsx_file, 'r', encoding='utf-8') as f:
            tsx_content = f.read()
        
        # Add helper function for generating preview text
        helper_function = '''  // Helper function to generate preview text for collapsed sections
  const getPreviewText = useCallback((section: string) => {
    switch (section) {
      case 'colors':
        const colorPreviews = [];
        if (activeFilters.colors.length > 0) {
          colorPreviews.push(...activeFilters.colors);
        }
        if (activeFilters.isGoldMode) {
          colorPreviews.push('GOLD');
        }
        return colorPreviews.length > 0 ? `(${colorPreviews.join(', ')})` : '';
      
      case 'cmc':
        const cmcParts = [];
        if (activeFilters.cmc.min !== null) cmcParts.push(`${activeFilters.cmc.min}+`);
        if (activeFilters.cmc.max !== null) cmcParts.push(`≤${activeFilters.cmc.max}`);
        return cmcParts.length > 0 ? `(${cmcParts.join(', ')})` : '';
      
      case 'types':
        return activeFilters.types.length > 0 ? `(${activeFilters.types.slice(0, 2).join(', ')}${activeFilters.types.length > 2 ? '...' : ''})` : '';
      
      case 'subtypes':
        return activeFilters.subtypes.length > 0 ? `(${activeFilters.subtypes.slice(0, 2).join(', ')}${activeFilters.subtypes.length > 2 ? '...' : ''})` : '';
      
      case 'rarity':
        return activeFilters.rarity.length > 0 ? `(${activeFilters.rarity.join(', ').toUpperCase()})` : '';
      
      case 'stats':
        const statParts = [];
        if (activeFilters.power.min !== null || activeFilters.power.max !== null) {
          statParts.push('Power');
        }
        if (activeFilters.toughness.min !== null || activeFilters.toughness.max !== null) {
          statParts.push('Toughness');
        }
        return statParts.length > 0 ? `(${statParts.join(', ')})` : '';
      
      default:
        return '';
    }
  }, [activeFilters]);

'''
        
        # Insert helper function after the imports and before the first handler
        insert_point = "  // Color selection handler with gold button logic"
        if insert_point in tsx_content:
            tsx_content = tsx_content.replace(insert_point, helper_function + insert_point)
            print("✅ Added preview text helper function")
        else:
            print("❌ Could not find insertion point for helper function")
            success = False
        
        # Update CollapsibleSection calls to include preview text
        sections_to_update = [
            ('colors', 'COLORS'),
            ('cmc', 'MANA VALUE (MV)'),
            ('types', 'CARD TYPES'),
            ('subtypes', 'MORE TYPES'),
            ('sets', 'SETS'),
            ('rarity', 'RARITY'),
            ('stats', 'CREATURE STATS')
        ]
        
        for section_key, section_title in sections_to_update:
            old_section = f'''        <CollapsibleSection
          title="{section_title}"
          isExpanded={{getSectionState('{section_key}')}}'''
            
            new_section = f'''        <CollapsibleSection
          title="{section_title}"
          previewText={{getSectionState('{section_key}') ? '' : getPreviewText('{section_key}')}}
          isExpanded={{getSectionState('{section_key}')}}'''
            
            if old_section in tsx_content:
                tsx_content = tsx_content.replace(old_section, new_section)
                print(f"✅ Added preview text to {section_title} section")
            else:
                print(f"❌ Could not find {section_title} section to update")
                success = False
        
        with open(tsx_file, 'w', encoding='utf-8') as f:
            f.write(tsx_content)
    else:
        print(f"❌ {tsx_file} not found")
        success = False
    
    # Update CollapsibleSection.tsx - Add preview text support
    collapsible_file = "src/components/CollapsibleSection.tsx"
    if os.path.exists(collapsible_file):
        with open(collapsible_file, 'r', encoding='utf-8') as f:
            collapsible_content = f.read()
        
        # Update interface to include previewText
        old_interface = '''interface CollapsibleSectionProps {
  title: string;
  isExpanded: boolean;
  hasActiveFilters: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}'''
        
        new_interface = '''interface CollapsibleSectionProps {
  title: string;
  previewText?: string;
  isExpanded: boolean;
  hasActiveFilters: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}'''
        
        if old_interface in collapsible_content:
            collapsible_content = collapsible_content.replace(old_interface, new_interface)
            print("✅ Updated CollapsibleSection interface")
        else:
            print("❌ Could not find CollapsibleSection interface to update")
            success = False
        
        # Update component signature
        old_signature = '''const CollapsibleSection: React.FC<CollapsibleSectionProps> = ({
  title,
  isExpanded,
  hasActiveFilters,
  onToggle,
  children
}) => {'''
        
        new_signature = '''const CollapsibleSection: React.FC<CollapsibleSectionProps> = ({
  title,
  previewText = '',
  isExpanded,
  hasActiveFilters,
  onToggle,
  children
}) => {'''
        
        if old_signature in collapsible_content:
            collapsible_content = collapsible_content.replace(old_signature, new_signature)
            print("✅ Updated CollapsibleSection component signature")
        else:
            print("❌ Could not find CollapsibleSection signature to update")
            success = False
        
        # Update title display to include preview text
        old_title_display = '''      <span className="section-title">{title}</span>'''
        
        new_title_display = '''      <span className="section-title">
        {title} <span className="section-preview">{previewText}</span>
      </span>'''
        
        if old_title_display in collapsible_content:
            collapsible_content = collapsible_content.replace(old_title_display, new_title_display)
            print("✅ Updated title display to include preview text")
        else:
            print("❌ Could not find title display to update")
            success = False
        
        with open(collapsible_file, 'w', encoding='utf-8') as f:
            f.write(collapsible_content)
    else:
        print(f"❌ {collapsible_file} not found")
        success = False
    
    # Update FilterPanel.css - Implement compact design
    css_file = "src/components/FilterPanel.css"
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Fix 1: Gold button readability - change to black text
        old_gold_text = '''.color-gold {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  border: 2px solid #FFD700 !important;
  color: #000000;
  font-weight: bold;
  font-size: 11px;
  text-shadow: none;
  box-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
  transition: all 0.2s ease;
}'''
        
        new_gold_text = '''.color-gold {
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
  border: 2px solid #FFD700 !important;
  color: #000000;
  font-weight: 900;
  font-size: 10px;
  text-shadow: 1px 1px 1px rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
  transition: all 0.2s ease;
}'''
        
        if old_gold_text in css_content:
            css_content = css_content.replace(old_gold_text, new_gold_text)
            print("✅ Fixed gold button text readability")
        else:
            print("❌ Could not find gold button styling to fix")
            success = False
        
        # Fix 2: Compact color buttons - reduce size from 36px to 24px
        old_color_button = '''.color-button {
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 14px;
  font-weight: bold;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  text-shadow: none;
}'''
        
        new_color_button = '''.color-button {
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 11px;
  font-weight: bold;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  text-shadow: none;
}'''
        
        if old_color_button in css_content:
            css_content = css_content.replace(old_color_button, new_color_button)
            print("✅ Made color buttons more compact (36px → 24px)")
        else:
            print("❌ Could not find color button styling to compact")
            success = False
        
        # Fix 3: Compact section headers - reduce height
        old_section_header = '''.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #333333;
  border: 1px solid #404040;
  cursor: pointer;
  transition: background-color 0.2s ease;
  user-select: none;
}'''
        
        new_section_header = '''.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 8px;
  background: #333333;
  border: none;
  border-bottom: 1px solid #404040;
  cursor: pointer;
  transition: background-color 0.2s ease;
  user-select: none;
  min-height: 16px;
}'''
        
        if old_section_header in css_content:
            css_content = css_content.replace(old_section_header, new_section_header)
            print("✅ Made section headers more compact")
        else:
            print("❌ Could not find section header styling to compact")
            success = False
        
        # Fix 4: Add preview text styling
        preview_text_css = '''
/* Section Preview Text */
.section-preview {
  font-weight: 400;
  color: #3b82f6;
  font-size: 10px;
  margin-left: 4px;
}
'''
        
        if '.section-preview' not in css_content:
            css_content += preview_text_css
            print("✅ Added section preview text styling")
        
        # Fix 5: Compact section content
        old_section_content = '''.section-content {
  padding: 6px 12px;
  background: #2a2a2a;
  border-left: 1px solid #404040;
  border-right: 1px solid #404040;
  border-bottom: 1px solid #404040;
  animation: expandSection 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}'''
        
        new_section_content = '''.section-content {
  padding: 4px 8px;
  background: #2a2a2a;
  animation: expandSection 0.2s ease;
}'''
        
        if old_section_content in css_content:
            css_content = css_content.replace(old_section_content, new_section_content)
            print("✅ Made section content more compact")
        else:
            print("❌ Could not find section content styling to compact")
            success = False
        
        # Fix 6: Compact color filter grid spacing
        old_color_grid = '''.color-filter-grid-row1,
.color-filter-grid-row2 {
  display: flex;
  gap: 6px;
  margin-bottom: 6px;
  justify-content: center;
}'''
        
        new_color_grid = '''.color-filter-grid-row1,
.color-filter-grid-row2 {
  display: flex;
  gap: 4px;
  margin-bottom: 3px;
  justify-content: center;
}'''
        
        if old_color_grid in css_content:
            css_content = css_content.replace(old_color_grid, new_color_grid)
            print("✅ Made color grid more compact")
        else:
            print("❌ Could not find color grid styling to compact")
            success = False
        
        # Fix 7: Type buttons in 3-column grid
        old_type_grid = '''.multi-select-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 4px;
  margin-top: 6px;
}'''
        
        new_type_grid = '''.multi-select-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2px;
  margin-top: 3px;
}'''
        
        if old_type_grid in css_content:
            css_content = css_content.replace(old_type_grid, new_type_grid)
            print("✅ Changed type buttons to 3-column grid")
        else:
            print("❌ Could not find type grid styling to update")
            success = False
        
        # Fix 8: Compact type/rarity buttons
        old_type_buttons = '''.type-button,
.rarity-button {
  padding: 6px 8px;
  background: #333333;
  border: 1px solid #404040;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 11px;
  text-align: center;
  transition: all 0.2s ease;
}'''
        
        new_type_buttons = '''.type-button,
.rarity-button {
  padding: 3px 4px;
  background: #333333;
  border: 1px solid #404040;
  border-radius: 3px;
  color: white;
  cursor: pointer;
  font-size: 9px;
  text-align: center;
  transition: all 0.2s ease;
}'''
        
        if old_type_buttons in css_content:
            css_content = css_content.replace(old_type_buttons, new_type_buttons)
            print("✅ Made type/rarity buttons more compact")
        else:
            print("❌ Could not find type/rarity button styling to compact")
            success = False
        
        # Fix 9: Search container boundaries
        search_container_fix = '''
/* Search Container Boundary Fix */
.search-group {
  margin-bottom: 8px;
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
}

.search-group .search-autocomplete {
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}

.search-group .search-input {
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
}
'''
        
        if '.search-group .search-autocomplete' not in css_content:
            css_content += search_container_fix
            print("✅ Added search container boundary fixes")
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
    else:
        print(f"❌ {css_file} not found")
        success = False
    
    if success:
        print("\n🎉 COMPACT DESIGN IMPLEMENTATION COMPLETE!")
        print("   ✅ Smart accordion with active filter previews")
        print("   ✅ Compact 24px color buttons with better readability")
        print("   ✅ 3-column type button grid for space efficiency")
        print("   ✅ Reduced section heights and padding throughout")
        print("   ✅ Fixed search bar container boundaries")
        print("   ✅ Enhanced gold button text with white shadow")
        print("\n📊 Expected Results:")
        print("   • ~60% reduction in vertical space usage")
        print("   • Active filters visible when sections collapsed")
        print("   • Much more efficient visual design")
    else:
        print("❌ Some updates could not be applied - please check the output above")
    
    return success

if __name__ == "__main__":
    success = update_filterpanel_compact_design()
    sys.exit(0 if success else 1)