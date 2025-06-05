#!/usr/bin/env python3
"""
Panel Resizing Fix - Allow Near-Invisible Panel Sizes
Updates constraints in useLayout.ts and adds CSS for content hiding
"""

import os
import re

def update_useLayout_constraints():
    """Update panel constraints to allow much smaller minimum sizes"""
    
    file_path = "src/hooks/useLayout.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the CONSTRAINTS object
        old_constraints = """const CONSTRAINTS = {
  filterPanelWidth: { min: 200, max: 500 },
  deckAreaHeightPercent: { min: 25, max: 60 }, // 25% to 60% of screen height
  sideboardWidth: { min: 200, max: 1000 },"""
        
        new_constraints = """const CONSTRAINTS = {
  filterPanelWidth: { min: 20, max: 500 },     // Allow near-invisible (20px = resize handle only)
  deckAreaHeightPercent: { min: 8, max: 75 },  // Allow much smaller/larger ranges
  sideboardWidth: { min: 20, max: 1000 },      // Allow near-invisible (20px = resize handle only)"""
        
        if old_constraints in content:
            content = content.replace(old_constraints, new_constraints)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Updated useLayout.ts constraints for extended panel resizing")
            return True
        else:
            print("❌ Could not find CONSTRAINTS object pattern in useLayout.ts")
            return False
            
    except Exception as e:
        print(f"❌ Error updating useLayout.ts: {e}")
        return False

def add_content_hiding_css():
    """Add CSS rules to hide content when panels get very small"""
    
    file_path = "src/components/MTGOLayout.css"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # CSS rules to add at the end of the file
        new_css_rules = """

/* ===== EXTENDED PANEL RESIZING - CONTENT HIDING ===== */

/* Hide filter panel content when very narrow */
.mtgo-filter-panel {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mtgo-filter-panel[style*="width: 20px"],
.mtgo-filter-panel[style*="width: 21px"],
.mtgo-filter-panel[style*="width: 22px"],
.mtgo-filter-panel[style*="width: 23px"],
.mtgo-filter-panel[style*="width: 24px"],
.mtgo-filter-panel[style*="width: 25px"],
.mtgo-filter-panel[style*="width: 26px"],
.mtgo-filter-panel[style*="width: 27px"],
.mtgo-filter-panel[style*="width: 28px"],
.mtgo-filter-panel[style*="width: 29px"],
.mtgo-filter-panel[style*="width: 30px"],
.mtgo-filter-panel[style*="width: 31px"],
.mtgo-filter-panel[style*="width: 32px"],
.mtgo-filter-panel[style*="width: 33px"],
.mtgo-filter-panel[style*="width: 34px"],
.mtgo-filter-panel[style*="width: 35px"],
.mtgo-filter-panel[style*="width: 36px"],
.mtgo-filter-panel[style*="width: 37px"],
.mtgo-filter-panel[style*="width: 38px"],
.mtgo-filter-panel[style*="width: 39px"],
.mtgo-filter-panel[style*="width: 40px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 40px"] .filter-content {
  display: none !important;
}

/* Show only resize handle when filter panel is very narrow */
.mtgo-filter-panel[style*="width: 20px"],
.mtgo-filter-panel[style*="width: 21px"],
.mtgo-filter-panel[style*="width: 22px"],
.mtgo-filter-panel[style*="width: 23px"],
.mtgo-filter-panel[style*="width: 24px"],
.mtgo-filter-panel[style*="width: 25px"],
.mtgo-filter-panel[style*="width: 26px"],
.mtgo-filter-panel[style*="width: 27px"],
.mtgo-filter-panel[style*="width: 28px"],
.mtgo-filter-panel[style*="width: 29px"],
.mtgo-filter-panel[style*="width: 30px"],
.mtgo-filter-panel[style*="width: 31px"],
.mtgo-filter-panel[style*="width: 32px"],
.mtgo-filter-panel[style*="width: 33px"],
.mtgo-filter-panel[style*="width: 34px"],
.mtgo-filter-panel[style*="width: 35px"],
.mtgo-filter-panel[style*="width: 36px"],
.mtgo-filter-panel[style*="width: 37px"],
.mtgo-filter-panel[style*="width: 38px"],
.mtgo-filter-panel[style*="width: 39px"],
.mtgo-filter-panel[style*="width: 40px"] {
  background-color: #404040;
  border-right: 2px solid #666666;
}

/* Hide sideboard content when very narrow */
.mtgo-sideboard-panel[style*="width: 20px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 21px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 22px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 23px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 24px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 25px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 26px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 27px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 28px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 29px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 30px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 31px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 32px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 33px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 34px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 35px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 36px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 37px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 38px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 39px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 40px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 20px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 21px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 22px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 23px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 24px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 25px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 26px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 27px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 28px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 29px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 30px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 31px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 32px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 33px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 34px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 35px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 36px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 37px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 38px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 39px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 40px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 20px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 21px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 22px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 23px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 24px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 25px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 26px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 27px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 28px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 29px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 30px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 31px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 32px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 33px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 34px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 35px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 36px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 37px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 38px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 39px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 40px"] .sideboard-content {
  display: none !important;
}

/* Show only resize handle when sideboard is very narrow */
.mtgo-sideboard-panel[style*="width: 20px"],
.mtgo-sideboard-panel[style*="width: 21px"],
.mtgo-sideboard-panel[style*="width: 22px"],
.mtgo-sideboard-panel[style*="width: 23px"],
.mtgo-sideboard-panel[style*="width: 24px"],
.mtgo-sideboard-panel[style*="width: 25px"],
.mtgo-sideboard-panel[style*="width: 26px"],
.mtgo-sideboard-panel[style*="width: 27px"],
.mtgo-sideboard-panel[style*="width: 28px"],
.mtgo-sideboard-panel[style*="width: 29px"],
.mtgo-sideboard-panel[style*="width: 30px"],
.mtgo-sideboard-panel[style*="width: 31px"],
.mtgo-sideboard-panel[style*="width: 32px"],
.mtgo-sideboard-panel[style*="width: 33px"],
.mtgo-sideboard-panel[style*="width: 34px"],
.mtgo-sideboard-panel[style*="width: 35px"],
.mtgo-sideboard-panel[style*="width: 36px"],
.mtgo-sideboard-panel[style*="width: 37px"],
.mtgo-sideboard-panel[style*="width: 38px"],
.mtgo-sideboard-panel[style*="width: 39px"],
.mtgo-sideboard-panel[style*="width: 40px"] {
  background-color: #404040;
  border-left: 2px solid #666666;
  border-right: none;
}

/* Hide deck area content when very short (using CSS custom property) */
html[style*="--deck-area-height-percent: 8%"] .mtgo-bottom-area .panel-header h3,
html[style*="--deck-area-height-percent: 9%"] .mtgo-bottom-area .panel-header h3,
html[style*="--deck-area-height-percent: 10%"] .mtgo-bottom-area .panel-header h3,
html[style*="--deck-area-height-percent: 11%"] .mtgo-bottom-area .panel-header h3,
html[style*="--deck-area-height-percent: 12%"] .mtgo-bottom-area .panel-header h3,
html[style*="--deck-area-height-percent: 8%"] .mtgo-bottom-area .deck-controls,
html[style*="--deck-area-height-percent: 9%"] .mtgo-bottom-area .deck-controls,
html[style*="--deck-area-height-percent: 10%"] .mtgo-bottom-area .deck-controls,
html[style*="--deck-area-height-percent: 11%"] .mtgo-bottom-area .deck-controls,
html[style*="--deck-area-height-percent: 12%"] .mtgo-bottom-area .deck-controls,
html[style*="--deck-area-height-percent: 8%"] .mtgo-bottom-area .sideboard-controls,
html[style*="--deck-area-height-percent: 9%"] .mtgo-bottom-area .sideboard-controls,
html[style*="--deck-area-height-percent: 10%"] .mtgo-bottom-area .sideboard-controls,
html[style*="--deck-area-height-percent: 11%"] .mtgo-bottom-area .sideboard-controls,
html[style*="--deck-area-height-percent: 12%"] .mtgo-bottom-area .sideboard-controls,
html[style*="--deck-area-height-percent: 8%"] .deck-content,
html[style*="--deck-area-height-percent: 9%"] .deck-content,
html[style*="--deck-area-height-percent: 10%"] .deck-content,
html[style*="--deck-area-height-percent: 11%"] .deck-content,
html[style*="--deck-area-height-percent: 12%"] .deck-content,
html[style*="--deck-area-height-percent: 8%"] .sideboard-content,
html[style*="--deck-area-height-percent: 9%"] .sideboard-content,
html[style*="--deck-area-height-percent: 10%"] .sideboard-content,
html[style*="--deck-area-height-percent: 11%"] .sideboard-content,
html[style*="--deck-area-height-percent: 12%"] .sideboard-content {
  display: none !important;
}

/* Show thin border when deck area is very short */
html[style*="--deck-area-height-percent: 8%"] .mtgo-bottom-area,
html[style*="--deck-area-height-percent: 9%"] .mtgo-bottom-area,
html[style*="--deck-area-height-percent: 10%"] .mtgo-bottom-area,
html[style*="--deck-area-height-percent: 11%"] .mtgo-bottom-area,
html[style*="--deck-area-height-percent: 12%"] .mtgo-bottom-area {
  background-color: #404040;
  border-top: 2px solid #666666;
}

/* Enhanced resize handle visibility when panels are very small */
.mtgo-filter-panel[style*="width: 20px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 21px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 22px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 23px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 24px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 25px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 26px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 27px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 28px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 29px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 30px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 31px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 32px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 33px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 34px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 35px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 36px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 37px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 38px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 39px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 40px"] .resize-handle-right,
.mtgo-sideboard-panel[style*="width: 20px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 21px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 22px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 23px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 24px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 25px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 26px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 27px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 28px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 29px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 30px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 31px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 32px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 33px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 34px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 35px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 36px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 37px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 38px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 39px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 40px"] .resize-handle-left {
  background-color: rgba(59, 130, 246, 0.6) !important;
}

/* ===== END EXTENDED PANEL RESIZING ===== */
"""
        
        # Check if these rules are already present
        if "EXTENDED PANEL RESIZING" not in content:
            content += new_css_rules
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Added content hiding CSS rules to MTGOLayout.css")
            return True
        else:
            print("⚠️  Content hiding CSS rules already present in MTGOLayout.css")
            return True
            
    except Exception as e:
        print(f"❌ Error updating MTGOLayout.css: {e}")
        return False

def main():
    """Execute all panel resizing fixes"""
    print("🎯 Starting Panel Resizing Enhancement...")
    print("=" * 50)
    
    success_count = 0
    total_operations = 2
    
    # Update useLayout constraints
    if update_useLayout_constraints():
        success_count += 1
    
    # Add CSS content hiding rules
    if add_content_hiding_css():
        success_count += 1
    
    print("=" * 50)
    if success_count == total_operations:
        print("🎉 Panel Resizing Enhancement COMPLETE!")
        print("\n✅ IMPLEMENTED FEATURES:")
        print("   • Filter panel: Now resizes down to 20px (thin border only)")
        print("   • Sideboard: Now resizes down to 20px (thin border only)")  
        print("   • Deck area: Now resizes down to 8% of screen height")
        print("   • Content automatically hides when panels get very small")
        print("   • Resize handles remain visible for easy expansion")
        print("\n🎮 USAGE:")
        print("   • Drag resize handles to make panels near-invisible")
        print("   • Panels show as thin colored borders when minimized")
        print("   • Drag resize handles to expand panels back to normal")
        print("\n🚀 Ready to test extended panel resizing!")
    else:
        print(f"❌ Panel Resizing Enhancement FAILED: {success_count}/{total_operations} operations successful")
        print("   Please check error messages above and retry.")

if __name__ == "__main__":
    main()
