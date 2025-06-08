#!/usr/bin/env python3
"""
Overflow Menu Z-Index Fix: Fix ViewModeDropdown appearing behind overflow items
and resize handle appearing over overflow menu
"""

import os
import shutil

def backup_file(file_path):
    """Create a backup of the original file"""
    backup_path = f"{file_path}.zindex_backup"
    if os.path.exists(file_path):
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
    return backup_path

def fix_zindex_hierarchy():
    """Fix z-index hierarchy for overflow menu and nested dropdowns"""
    css_file_path = "src/components/MTGOLayout.css"
    
    if not os.path.exists(css_file_path):
        print(f"❌ File not found: {css_file_path}")
        return False
    
    # Create backup
    backup_file(css_file_path)
    
    # Enhanced z-index fixes
    zindex_fixes = '''

/* ===== OVERFLOW MENU Z-INDEX FIXES ===== */

/* Fix 1: Resize handle should be BELOW overflow menu */
.resize-handle,
.resize-handle-left,
.resize-handle-right,
.resize-handle-bottom {
  z-index: 999 !important; /* Well below overflow menu */
}

/* Make resize handle thicker and more visible */
.mtgo-sideboard-panel .resize-handle-left {
  width: 20px !important; /* Even thicker - was 12px */
  left: -10px !important; /* Center the thicker handle */
  background: linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%) !important;
  opacity: 0.7 !important;
}

.mtgo-sideboard-panel .resize-handle-left:hover {
  width: 24px !important; /* Very thick on hover */
  left: -12px !important; /* Re-center for hover */
  background: linear-gradient(90deg, transparent 0%, #3b82f6 50%, transparent 100%) !important;
  opacity: 1 !important;
}

/* Fix 2: Overflow menu hierarchy - MUCH higher z-index */
.overflow-menu-container {
  z-index: 15000 !important; /* Very high */
  position: relative !important;
}

.overflow-menu {
  z-index: 15001 !important; /* Higher than container */
  position: fixed !important;
  backdrop-filter: blur(8px) !important;
  background: rgba(42, 42, 42, 0.95) !important; /* Semi-transparent for blur effect */
}

/* Fix 3: ViewModeDropdown in overflow context - HIGHEST z-index */
.overflow-menu .view-mode-dropdown {
  position: relative !important;
  z-index: 15002 !important;
}

.overflow-menu .view-dropdown-button {
  z-index: 15003 !important;
  position: relative !important;
}

/* CRITICAL: ViewModeDropdown menu when inside overflow - HIGHEST PRIORITY */
.overflow-menu .view-dropdown-menu {
  z-index: 20000 !important; /* Maximum priority */
  position: fixed !important;
  background: #2a2a2a !important;
  border: 1px solid #555555 !important;
  box-shadow: 0 4px 20px rgba(0,0,0,0.8) !important; /* Strong shadow for visibility */
  backdrop-filter: none !important; /* No blur for nested dropdown */
}

/* Ensure overflow menu items don't interfere with nested dropdown */
.overflow-menu-item {
  position: relative !important;
  z-index: 15001 !important; /* Lower than ViewModeDropdown */
  overflow: visible !important; /* Allow nested dropdown to escape */
}

/* Fix 4: Ensure all headers are below overflow elements */
.mtgo-header {
  z-index: 100 !important; /* Much lower than overflow */
}

.mtgo-deck-area .mtgo-header {
  z-index: 101 !important; /* Slightly higher than sideboard but much lower than overflow */
}

.mtgo-sideboard-panel .mtgo-header {
  z-index: 100 !important; /* Lower than deck */
}

/* Fix 5: Ensure proper stacking for the entire layout */
.mtgo-layout {
  z-index: 1 !important;
}

.mtgo-main-content {
  z-index: 2 !important;
}

.mtgo-bottom-area {
  z-index: 3 !important;
}

/* Fix 6: Collection area should not interfere */
.mtgo-collection-area {
  z-index: 50 !important;
}

.mtgo-collection-area .mtgo-header {
  z-index: 51 !important;
}

/* Fix 7: Standard dropdowns (not in overflow) should be high but not highest */
.view-dropdown-menu {
  z-index: 10001 !important; /* High for normal context */
}

.sort-menu {
  z-index: 10001 !important; /* Same level as normal dropdowns */
}

/* Fix 8: Ensure overflow menu positioning context */
.deck-controls-responsive {
  position: relative !important;
  z-index: 102 !important; /* Higher than headers but much lower than overflow */
}

/* ===== END OVERFLOW MENU Z-INDEX FIXES ===== */'''
    
    try:
        # Read existing content
        with open(css_file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Remove any existing similar fixes to avoid conflicts
        lines = existing_content.split('\n')
        cleaned_lines = []
        skip_section = False
        
        for line in lines:
            if '/* ===== HEADER ISSUES FIXES =====' in line:
                skip_section = True
            elif '/* ===== END HEADER ISSUES FIXES =====' in line:
                skip_section = False
                continue
            elif not skip_section:
                cleaned_lines.append(line)
        
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Append new fixes
        updated_content = cleaned_content + zindex_fixes
        
        # Write updated content
        with open(css_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Applied z-index hierarchy fixes to {css_file_path}")
        return True
    except Exception as e:
        print(f"❌ Error updating {css_file_path}: {e}")
        return False

def main():
    """Main fix function"""
    print("🔧 Fixing Overflow Menu Z-Index Issues")
    print("=" * 50)
    
    print("Issues to fix:")
    print("1. ViewModeDropdown appearing behind overflow menu items")
    print("2. Resize handle appearing over overflow menu")
    print("3. Make resize handle thicker and more grabbable")
    print()
    
    print("📋 Applying z-index hierarchy fixes...")
    if fix_zindex_hierarchy():
        print("✅ SUCCESS: Z-index issues should be resolved!")
        print("\n🔧 Fixes Applied:")
        print("   • ViewModeDropdown in overflow: z-index 20000 (highest priority)")
        print("   • Overflow menu: z-index 15001 (very high)")
        print("   • Resize handle: z-index 999 (below overflow menu)")
        print("   • Resize handle width: 20px (was 12px), 24px on hover")
        print("   • Headers: z-index 100-101 (much lower)")
        
        print("\n🧪 Testing Instructions:")
        print("   1. Run `npm start` to test the fixes")
        print("   2. Open overflow menu → Should appear above everything")
        print("   3. Click View dropdown in overflow → Should appear above other items")
        print("   4. Try resizing deck/sideboard → Handle should be thicker and not cover overflow")
        
        print("\n🎯 Z-Index Hierarchy:")
        print("   • ViewModeDropdown in overflow: 20000 (HIGHEST)")
        print("   • Overflow menu: 15001")
        print("   • Normal dropdowns: 10001")
        print("   • Resize handles: 999")
        print("   • Headers: 100-101 (LOWEST)")
        
        print("\n✨ Overflow menu should work perfectly now!")
    else:
        print("❌ FAILED: Could not apply fixes")
        print("💡 Check file paths and permissions")

if __name__ == "__main__":
    main()
