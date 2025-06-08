#!/usr/bin/env python3

import os
import sys

def update_filterpanel_final_polish():
    """Apply final polish fixes to FilterPanel.tsx and FilterPanel.css for production-ready appearance"""
    
    success = True
    
    # Update FilterPanel.tsx - Remove "Range" label from Mana Value section
    tsx_file = "src/components/FilterPanel.tsx"
    if os.path.exists(tsx_file):
        with open(tsx_file, 'r', encoding='utf-8') as f:
            tsx_content = f.read()
        
        # Remove the "Range" label from Mana Value section
        old_tsx = '''        <CollapsibleSection
          title="MANA VALUE (MV)"
          isExpanded={getSectionState('cmc')}
          hasActiveFilters={activeFilters.cmc.min !== null || activeFilters.cmc.max !== null}
          onToggle={() => updateSectionState('cmc', !getSectionState('cmc'))}
        >
          <div className="filter-group">
            <label>Range</label>
            <div className="range-filter">'''
        
        new_tsx = '''        <CollapsibleSection
          title="MANA VALUE (MV)"
          isExpanded={getSectionState('cmc')}
          hasActiveFilters={activeFilters.cmc.min !== null || activeFilters.cmc.max !== null}
          onToggle={() => updateSectionState('cmc', !getSectionState('cmc'))}
        >
          <div className="filter-group">
            <div className="range-filter">'''
        
        if old_tsx in tsx_content:
            tsx_content = tsx_content.replace(old_tsx, new_tsx)
            print("✅ Removed unnecessary 'Range' label from Mana Value section")
        else:
            print("❌ Could not find Mana Value 'Range' label to remove")
            success = False
        
        with open(tsx_file, 'w', encoding='utf-8') as f:
            f.write(tsx_content)
    else:
        print(f"❌ {tsx_file} not found")
        success = False
    
    # Update FilterPanel.css - Apply all visual polish fixes
    css_file = "src/components/FilterPanel.css"
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Fix 1: Enhanced blue glow effect for selected color buttons
        old_glow = '''.color-button.selected {
  border-color: #3b82f6;
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.8), inset 0 2px 4px rgba(0, 0, 0, 0.2);
}'''
        
        new_glow = '''.color-button.selected {
  border-color: #3b82f6;
  box-shadow: 0 0 16px rgba(59, 130, 246, 1.0), 0 0 8px rgba(59, 130, 246, 0.8), inset 0 2px 4px rgba(0, 0, 0, 0.2);
}'''
        
        if old_glow in css_content:
            css_content = css_content.replace(old_glow, new_glow)
            print("✅ Enhanced blue glow effect for selected color buttons")
        else:
            print("❌ Could not find color button glow effect to enhance")
            success = False
        
        # Fix 2: Compact vertical spacing for section content
        old_section_padding = '''.section-content {
  padding: 8px 12px;
  background: #2a2a2a;
  border-left: 1px solid #404040;
  border-right: 1px solid #404040;
  border-bottom: 1px solid #404040;
  animation: expandSection 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}'''
        
        new_section_padding = '''.section-content {
  padding: 6px 12px;
  background: #2a2a2a;
  border-left: 1px solid #404040;
  border-right: 1px solid #404040;
  border-bottom: 1px solid #404040;
  animation: expandSection 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}'''
        
        if old_section_padding in css_content:
            css_content = css_content.replace(old_section_padding, new_section_padding)
            print("✅ Reduced section content padding for more compact design")
        else:
            print("❌ Could not find section content padding to optimize")
            success = False
        
        # Fix 3: Stricter container constraints for subtype input
        old_subtype_container = '''.subtype-input-container {
  position: relative;
}'''
        
        new_subtype_container = '''.subtype-input-container {
  position: relative;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
  box-sizing: border-box;
}'''
        
        if old_subtype_container in css_content:
            css_content = css_content.replace(old_subtype_container, new_subtype_container)
            print("✅ Enhanced subtype input container boundaries")
        else:
            print("❌ Could not find subtype input container to enhance")
            success = False
        
        # Fix 4: Improved creature stats layout with better alignment
        old_stat_row = '''.stat-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-row span {
  font-size: 11px;
  color: #cccccc;
  min-width: 60px;
}'''
        
        new_stat_row = '''.stat-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-row span:first-child {
  font-size: 11px;
  color: #cccccc;
  min-width: 50px;
  text-align: left;
}

.stat-row span:nth-child(3) {
  font-size: 11px;
  color: #cccccc;
  min-width: 20px;
  text-align: center;
}'''
        
        if old_stat_row in css_content:
            css_content = css_content.replace(old_stat_row, new_stat_row)
            print("✅ Improved creature stats layout alignment")
        else:
            print("❌ Could not find creature stats layout to improve")
            success = False
        
        # Fix 5: Enhanced range filter layout for better spacing
        old_range_filter = '''.range-filter {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
}

.range-filter span {
  font-size: 11px;
  color: #cccccc;
}'''
        
        new_range_filter = '''.range-filter {
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
        
        if old_range_filter in css_content:
            css_content = css_content.replace(old_range_filter, new_range_filter)
            print("✅ Enhanced range filter layout spacing")
        else:
            print("❌ Could not find range filter layout to enhance")
            success = False
        
        # Additional enhancement: Ensure gold button blue glow is consistent
        old_gold_selected = '''.color-gold.selected {
  background: #FFD700;
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.8), 0 0 8px rgba(255, 215, 0, 0.6), inset 0 2px 4px rgba(0, 0, 0, 0.2);
  border-color: #3b82f6;
  color: #000000;
}'''
        
        new_gold_selected = '''.color-gold.selected {
  background: #FFD700;
  box-shadow: 0 0 16px rgba(59, 130, 246, 1.0), 0 0 8px rgba(59, 130, 246, 0.8), 0 0 4px rgba(255, 215, 0, 0.6), inset 0 2px 4px rgba(0, 0, 0, 0.2);
  border-color: #3b82f6;
  color: #000000;
}'''
        
        if old_gold_selected in css_content:
            css_content = css_content.replace(old_gold_selected, new_gold_selected)
            print("✅ Enhanced gold button blue glow consistency")
        else:
            print("❌ Could not find gold button selected state to enhance")
            success = False
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
    else:
        print(f"❌ {css_file} not found")
        success = False
    
    if success:
        print("✅ All Phase 4B final polish fixes applied successfully!")
        print("   • Enhanced color selection blue glow effect")
        print("   • Reduced vertical spacing for compact design")
        print("   • Improved subtype input container boundaries")
        print("   • Optimized creature stats layout alignment")
        print("   • Removed unnecessary 'Range' label from Mana Value")
        print("   • Enhanced gold button glow consistency")
    else:
        print("❌ Some fixes could not be applied - please check the output above")
    
    return success

if __name__ == "__main__":
    success = update_filterpanel_final_polish()
    sys.exit(0 if success else 1)