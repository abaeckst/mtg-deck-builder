#!/usr/bin/env python3
"""
Slim Headers Update: Make headers more compact and ensure consistent height
- Reduce header padding and spacing for slimmer appearance
- Ensure DeckArea and SideboardArea headers have identical height
- Maintain professional MTGO styling and responsive functionality
- Optimize control sizing for compact layout
"""

import os
import shutil

def backup_file(file_path):
    """Create a backup of the original file"""
    backup_path = f"{file_path}.slim_backup"
    if os.path.exists(file_path):
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
    return backup_path

def update_deckarea_slim_header():
    """Update DeckArea.tsx with slimmer header styling"""
    file_path = "src/components/DeckArea.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Create backup
    backup_file(file_path)
    
    # Read current content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update header styling for slimmer appearance
        # Find and replace the header style section
        old_header_style = '''        style={{
          background: 'linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%)',
          border: '1px solid #444',
          borderTop: '1px solid #666',
          boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
          padding: '12px 16px',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '16px',
          fontSize: '14px',
          position: 'relative'
        }}'''
        
        new_header_style = '''        style={{
          background: 'linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%)',
          border: '1px solid #444',
          borderTop: '1px solid #666',
          boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
          padding: '8px 12px',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
          fontSize: '13px',
          position: 'relative',
          minHeight: '40px'
        }}'''
        
        content = content.replace(old_header_style, new_header_style)
        
        # Update title section styling for slimmer fit
        old_title_style = '''          style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '8px',
            minWidth: '150px',
            maxWidth: '300px'
          }}'''
        
        new_title_style = '''          style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '6px',
            minWidth: '140px',
            maxWidth: '280px'
          }}'''
        
        content = content.replace(old_title_style, new_title_style)
        
        # Update title font sizes for slimmer header
        old_title_font = '''            fontSize: '16px','''
        new_title_font = '''            fontSize: '15px','''
        content = content.replace(old_title_font, new_title_font)
        
        old_count_font = '''            fontSize: '14px','''
        new_count_font = '''            fontSize: '13px','''
        content = content.replace(old_count_font, new_count_font)
        
        # Update controls container for slimmer header
        old_controls_style = '''            gap: '12px',
            fontSize: '13px','''
        
        new_controls_style = '''            gap: '10px',
            fontSize: '12px','''
        
        content = content.replace(old_controls_style, new_controls_style)
        
        # Update control groups for slimmer fit
        old_group_padding = '''              padding: '4px 8px','''
        new_group_padding = '''              padding: '3px 6px','''
        content = content.replace(old_group_padding, new_group_padding)
        
        # Update control group gaps
        old_group_gap = '''              gap: '8px','''
        new_group_gap = '''              gap: '6px','''
        content = content.replace(old_group_gap, new_group_gap)
        
        # Update button padding for slimmer fit
        old_button_padding = '''                      padding: '4px 8px','''
        new_button_padding = '''                      padding: '3px 6px','''
        content = content.replace(old_button_padding, new_button_padding)
        
        # Update slider width for slimmer header
        old_slider_width = '''                  width: '80px','''
        new_slider_width = '''                  width: '70px','''
        content = content.replace(old_slider_width, new_slider_width)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {file_path} with slimmer header styling")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_sideboardarea_slim_header():
    """Update SideboardArea.tsx with slimmer header styling matching DeckArea"""
    file_path = "src/components/SideboardArea.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Create backup
    backup_file(file_path)
    
    # Read current content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update header styling to match slimmer DeckArea
        old_header_style = '''        style={{
          background: 'linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%)',
          border: '1px solid #444',
          borderTop: '1px solid #666',
          boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
          padding: '12px 16px',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          fontSize: '14px'
        }}'''
        
        new_header_style = '''        style={{
          background: 'linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%)',
          border: '1px solid #444',
          borderTop: '1px solid #666',
          boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
          padding: '8px 12px',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          fontSize: '13px',
          minHeight: '40px'
        }}'''
        
        content = content.replace(old_header_style, new_header_style)
        
        # Update title section styling to match DeckArea
        old_title_style = '''        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>'''
        new_title_style = '''        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>'''
        content = content.replace(old_title_style, new_title_style)
        
        # Update title font sizes to match DeckArea
        old_title_font = '''            fontSize: '16px','''
        new_title_font = '''            fontSize: '15px','''
        content = content.replace(old_title_font, new_title_font)
        
        old_count_font = '''            fontSize: '14px'''
        new_count_font = '''            fontSize: '13px'''
        content = content.replace(old_count_font, new_count_font)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {file_path} with slimmer header styling")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_collectionarea_slim_header():
    """Update CollectionArea.tsx with slimmer header styling for consistency"""
    file_path = "src/components/CollectionArea.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Create backup
    backup_file(file_path)
    
    # Read current content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update header styling to match other slim headers
        old_header_style = '''        style={{
          background: 'linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%)',
          border: '1px solid #444',
          borderTop: '1px solid #666',
          boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
          padding: '12px 16px',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '16px',
          fontSize: '14px'
        }}'''
        
        new_header_style = '''        style={{
          background: 'linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%)',
          border: '1px solid #444',
          borderTop: '1px solid #666',
          boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
          padding: '8px 12px',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
          fontSize: '13px',
          minHeight: '40px'
        }}'''
        
        content = content.replace(old_header_style, new_header_style)
        
        # Update title font size
        old_h3_style = '''          fontSize: '16px','''
        new_h3_style = '''          fontSize: '15px','''
        content = content.replace(old_h3_style, new_h3_style)
        
        # Update controls styling
        old_controls_style = '''            gap: '12px',
            fontSize: '13px'''
        
        new_controls_style = '''            gap: '10px',
            fontSize: '12px'''
        
        content = content.replace(old_controls_style, new_controls_style)
        
        # Update slider width
        old_slider_width = '''              width: '80px','''
        new_slider_width = '''              width: '70px','''
        content = content.replace(old_slider_width, new_slider_width)
        
        # Update button padding
        old_button_padding = '''              padding: '4px 8px','''
        new_button_padding = '''              padding: '3px 6px','''
        content = content.replace(old_button_padding, new_button_padding)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {file_path} with slimmer header styling")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_css_for_slim_headers():
    """Update CSS to support slimmer headers and ensure consistent height"""
    css_file_path = "src/components/MTGOLayout.css"
    
    if not os.path.exists(css_file_path):
        print(f"❌ File not found: {css_file_path}")
        return False
    
    # Create backup
    backup_file(css_file_path)
    
    # CSS updates for slim headers
    slim_header_css = '''

/* ===== SLIM HEADERS UPDATE: Consistent compact styling ===== */

/* Ensure all MTGO headers have consistent slim height */
.mtgo-header {
  min-height: 40px !important;
  max-height: 40px !important;
  padding: 8px 12px !important;
  gap: 10px !important;
  font-size: 13px !important;
}

/* Responsive control groups for slim headers */
.control-group-1,
.control-group-2,
.control-group-3 {
  padding: 3px 6px !important;
  gap: 6px !important;
  border-radius: 3px !important;
}

/* Compact button styling for slim headers */
.mtgo-button,
.mtgo-button-enhanced,
.sort-toggle-btn,
.overflow-menu-toggle {
  padding: 3px 6px !important;
  font-size: 11px !important;
  border-radius: 2px !important;
  min-height: 24px !important;
}

/* Compact slider styling */
.mtgo-slider,
.mtgo-slider-enhanced,
.size-slider {
  width: 70px !important;
  height: 4px !important;
}

.mtgo-slider-enhanced::-webkit-slider-thumb {
  width: 14px !important;
  height: 14px !important;
}

.mtgo-slider-enhanced::-moz-range-thumb {
  width: 14px !important;
  height: 14px !important;
}

/* ViewModeDropdown compact styling */
.view-dropdown-button {
  min-width: 75px !important;
  padding: 3px 6px !important;
  font-size: 11px !important;
  min-height: 24px !important;
}

/* Sort menu compact styling */
.sort-menu,
.overflow-menu {
  min-width: 110px !important;
}

.sort-menu button,
.overflow-menu-item {
  padding: 4px 8px !important;
  font-size: 11px !important;
}

/* Title section responsive for slim headers */
.title-section {
  min-width: 140px !important;
  max-width: 280px !important;
  gap: 6px !important;
}

.title-section span:first-child {
  font-size: 15px !important;
}

.title-section span:last-child {
  font-size: 13px !important;
}

/* Responsive adjustments for slim headers */
@media (max-width: 1200px) {
  .mtgo-header {
    padding: 6px 10px !important;
    gap: 8px !important;
  }
  
  .control-group-1,
  .control-group-2,
  .control-group-3 {
    padding: 2px 4px !important;
    gap: 4px !important;
  }
  
  .title-section {
    max-width: 240px !important;
  }
}

@media (max-width: 900px) {
  .mtgo-header {
    padding: 6px 8px !important;
    gap: 6px !important;
  }
  
  .title-section {
    max-width: 200px !important;
  }
  
  .title-section span:first-child {
    font-size: 14px !important;
  }
  
  .title-section span:last-child {
    font-size: 12px !important;
  }
}

/* Ensure consistent height across all panels */
.panel-header {
  height: 40px !important;
  min-height: 40px !important;
  max-height: 40px !important;
  padding: 0 12px !important;
}

.panel-header h3 {
  font-size: 15px !important;
  margin: 0 !important;
}

/* Collection header specific adjustments */
.mtgo-collection-area .mtgo-header h3 {
  font-size: 15px !important;
  margin: 0 !important;
}

/* Overflow menu compact styling */
.overflow-menu-item {
  padding: 6px 10px !important;
}

.overflow-menu-item input[type="range"] {
  width: 60px !important;
}

.overflow-menu-item select {
  font-size: 11px !important;
  padding: 2px 4px !important;
}

/* ===== END SLIM HEADERS UPDATE ===== */'''
    
    try:
        # Read existing content
        with open(css_file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Append slim header styles
        updated_content = existing_content + slim_header_css
        
        # Write updated content
        with open(css_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Added slim header styles to {css_file_path}")
        return True
    except Exception as e:
        print(f"❌ Error updating {css_file_path}: {e}")
        return False

def main():
    """Main implementation function for slim headers"""
    print("🎯 Updating Headers: Making them slimmer with consistent height")
    print("=" * 70)
    
    # Implementation steps
    success_count = 0
    total_steps = 4
    
    print("\n📋 Step 1: Updating DeckArea.tsx with slim header styling...")
    if update_deckarea_slim_header():
        success_count += 1
    
    print("\n📋 Step 2: Updating SideboardArea.tsx with matching slim header...")
    if update_sideboardarea_slim_header():
        success_count += 1
    
    print("\n📋 Step 3: Updating CollectionArea.tsx for consistency...")
    if update_collectionarea_slim_header():
        success_count += 1
    
    print("\n📋 Step 4: Adding CSS styles for slim headers...")
    if update_css_for_slim_headers():
        success_count += 1
    
    # Summary
    print("\n" + "=" * 70)
    print(f"🎯 Slim Headers Update Summary: {success_count}/{total_steps} steps completed")
    
    if success_count == total_steps:
        print("✅ SUCCESS: All headers updated to slim, consistent styling!")
        print("\n🎨 Changes Applied:")
        print("   • Reduced header padding from 12px to 8px")
        print("   • Consistent 40px header height across all areas")
        print("   • Smaller font sizes (15px titles, 13px counts)")
        print("   • Compact control spacing and button sizing")
        print("   • Responsive adjustments maintained")
        
        print("\n🧪 Testing Instructions:")
        print("   1. Run `npm start` to see the slimmer headers")
        print("   2. Check that deck and sideboard headers are same height")
        print("   3. Verify responsive functionality still works")
        print("   4. Test overflow menu in narrow layouts")
        
        print("\n📏 Header Specifications:")
        print("   • Height: 40px (consistent across all areas)")
        print("   • Padding: 8px vertical, 12px horizontal")
        print("   • Title font: 15px (down from 16px)")
        print("   • Control font: 11-13px (compact sizing)")
        print("   • Button padding: 3px×6px (down from 4px×8px)")
        
        print("\n🎯 Professional slim design achieved!")
    else:
        print("⚠️  PARTIAL SUCCESS: Some steps failed - check errors above")
        print("💡 Restore backups if needed: .slim_backup files created")

if __name__ == "__main__":
    main()
