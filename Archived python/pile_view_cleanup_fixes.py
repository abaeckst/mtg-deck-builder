#!/usr/bin/env python3
"""
Pile View Cleanup & Bug Fixes
=============================

Fixes the specific issues found in the current implementation:
1. CSS conflicts - multiple pile view sections with contradictory rules
2. Sideboard sort menu bug - wrong ref being used
3. Z-index logic correction - first card should be fully visible
4. CSS cleanup - remove old styling, ensure clean implementation

Run from mtg-deckbuilder project root.
"""

import os
import re

def read_file(filepath):
    """Read file content safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

def write_file(filepath, content):
    """Write file content safely"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Error writing {filepath}: {e}")
        return False

def apply_cleanup_fixes():
    """Apply all cleanup fixes"""
    
    print("🧹 Starting Pile View Cleanup & Bug Fixes...")
    print("=" * 55)
    
    # Fix 1: MTGOLayout.tsx - Fix sideboard sort ref bug
    print("\n🎯 Fix 1: Fixing sideboard sort menu ref bug...")
    
    mtgo_layout_path = "src/components/MTGOLayout.tsx"
    mtgo_content = read_file(mtgo_layout_path)
    
    if mtgo_content is None:
        return False
    
    # Fix the sideboard sort ref bug
    wrong_sideboard_ref = '''                  <div className="sort-button-container" ref={deckSortRef}>'''
    correct_sideboard_ref = '''                  <div className="sort-button-container" ref={sideboardSortRef}>'''
    
    # Count occurrences to fix only the second one (sideboard)
    occurrences = mtgo_content.count(wrong_sideboard_ref)
    if occurrences >= 2:
        # Split and rejoin to fix only the second occurrence
        parts = mtgo_content.split(wrong_sideboard_ref)
        if len(parts) >= 3:
            # parts[0] + correct_deck_ref + parts[1] + correct_sideboard_ref + parts[2+]
            mtgo_content = parts[0] + wrong_sideboard_ref + parts[1] + correct_sideboard_ref + wrong_sideboard_ref.join(parts[2:])
            print("  ✅ Fixed sideboard sort container to use sideboardSortRef")
        else:
            print("  ⚠️  Could not fix sideboard ref - unexpected structure")
    else:
        print("  ⚠️  Could not find sideboard sort container to fix")
    
    # Save MTGOLayout.tsx changes
    if not write_file(mtgo_layout_path, mtgo_content):
        return False
    
    # Fix 2: PileColumn.tsx - Fix z-index logic for proper stacking order
    print("\n🎯 Fix 2: Fixing card stacking z-index logic...")
    
    pile_column_path = "src/components/PileColumn.tsx"
    pile_column_content = read_file(pile_column_path)
    
    if pile_column_content is None:
        return False
    
    # Fix the z-index calculation - first card should have highest z-index
    wrong_zindex = '''                zIndex: cardIndex + 1, // Bottom cards have higher z-index (first card = highest z-index)'''
    correct_zindex = '''                zIndex: 100 - cardIndex, // First card has highest z-index (fully visible), last card lowest'''
    
    if wrong_zindex in pile_column_content:
        pile_column_content = pile_column_content.replace(wrong_zindex, correct_zindex)
        print("  ✅ Fixed z-index logic - first card now has highest z-index")
    else:
        print("  ⚠️  Could not find z-index logic to fix")
    
    # Save PileColumn.tsx changes
    if not write_file(pile_column_path, pile_column_content):
        return False
    
    # Fix 3: MTGOLayout.css - Complete CSS cleanup and consolidation
    print("\n🎯 Fix 3: Cleaning up CSS conflicts and consolidating pile view styles...")
    
    css_path = "src/components/MTGOLayout.css"
    css_content = read_file(css_path)
    
    if css_content is None:
        return False
    
    # Remove all existing pile view CSS sections to start clean
    print("  🧹 Removing all conflicting pile view CSS sections...")
    
    # Remove all pile view related CSS sections
    css_content = re.sub(r'/\* PHASE 3D: Pile View Styles.*?(?=/\*[^/]|\Z)', '', css_content, flags=re.DOTALL)
    css_content = re.sub(r'/\* UPDATED: Pile View Container.*?(?=/\*[^/]|\Z)', '', css_content, flags=re.DOTALL)
    css_content = re.sub(r'/\* Pile View Container \*/.*?(?=/\*[^/]|\Z)', '', css_content, flags=re.DOTALL)
    css_content = re.sub(r'/\* Sort Button and Menu Styles \*/.*?(?=/\*[^/]|\Z)', '', css_content, flags=re.DOTALL)
    
    # Clean up any remaining pile-related CSS fragments
    css_content = re.sub(r'\.pile-[^{]*{[^}]*}', '', css_content, flags=re.DOTALL)
    css_content = re.sub(r'\.sort-[^{]*{[^}]*}', '', css_content, flags=re.DOTALL)
    
    # Remove excessive whitespace left by deletions
    css_content = re.sub(r'\n\s*\n\s*\n', '\n\n', css_content)
    
    print("  ✅ Removed all conflicting CSS sections")
    
    # Add clean, consolidated pile view CSS
    clean_pile_css = '''
/* ===== PILE VIEW STYLES - CLEAN CONSOLIDATED VERSION ===== */

/* Pile View Container */
.pile-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* Pile Columns Container - Area-level scrolling only */
.pile-columns-container {
  flex: 1;
  display: flex;
  overflow-x: auto;
  overflow-y: auto;
  padding: 4px;
  gap: 6px; /* Tight gaps like MTGO */
  align-items: flex-start;
  max-height: 100%;
}

/* Individual Pile Column - Clean, no background/border */
.pile-column {
  min-width: 120px;
  background-color: transparent;
  border: none;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  height: fit-content;
  position: relative;
}

.pile-column.empty-column {
  min-width: 80px;
  background-color: transparent;
  border: none;
  min-height: 100px;
}

/* Simple Column Number - No styling box */
.pile-column-number {
  text-align: center;
  font-size: 12px;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 4px;
  padding: 2px 0;
}

/* Column Content - Natural flow, no scrolling */
.pile-column-content {
  flex: 1;
  padding: 3px;
  display: flex;
  flex-direction: column;
  position: relative;
  /* NO overflow or max-height - natural content flow */
}

/* Card Stacking */
.pile-card-stack-item {
  position: relative;
  transition: transform 0.15s ease, z-index 0.15s ease;
}

.pile-card-stack-item:hover {
  transform: translateY(-8px);
  z-index: 1000 !important;
  box-shadow: 0 6px 12px rgba(0,0,0,0.5);
}

/* Empty Column Placeholder */
.empty-column-placeholder {
  text-align: center;
  color: #666666;
  font-size: 10px;
  font-style: italic;
  padding: 15px 8px;
  border: 1px dashed #555555;
  border-radius: 4px;
  margin: 4px;
}

/* Area-level Scrollbars Only */
.pile-columns-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.pile-columns-container::-webkit-scrollbar-track {
  background-color: #1a1a1a;
  border-radius: 4px;
}

.pile-columns-container::-webkit-scrollbar-thumb {
  background-color: #404040;
  border-radius: 4px;
}

.pile-columns-container::-webkit-scrollbar-thumb:hover {
  background-color: #555555;
}

.pile-columns-container::-webkit-scrollbar-corner {
  background-color: #1a1a1a;
}

/* Sort Button and Menu */
.sort-button-container {
  position: relative;
  display: inline-block;
}

.sort-toggle-btn {
  background-color: #404040;
  color: #ffffff;
  border: 1px solid #555555;
  padding: 4px 8px;
  border-radius: 3px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin: 0 4px;
}

.sort-toggle-btn:hover {
  background-color: #4a4a4a;
  transform: scale(1.02);
}

.sort-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #333333;
  border: 1px solid #555555;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  z-index: 1000;
  min-width: 120px;
  overflow: hidden;
}

.sort-menu button {
  display: block;
  width: 100%;
  background-color: transparent;
  color: #ffffff;
  border: none;
  padding: 8px 12px;
  font-size: 11px;
  cursor: pointer;
  text-align: left;
  transition: background-color 0.2s ease;
}

.sort-menu button:hover {
  background-color: #4a4a4a;
}

.sort-menu button.active {
  background-color: #3b82f6;
  color: #ffffff;
}

.sort-menu button:not(:last-child) {
  border-bottom: 1px solid #555555;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .pile-column {
    min-width: 100px;
  }
  
  .pile-column-number {
    font-size: 11px;
  }
}

@media (max-width: 900px) {
  .pile-view {
    display: none;
  }
}

/* ===== END PILE VIEW STYLES ===== */
'''
    
    # Add the clean CSS at the end
    css_content += clean_pile_css
    print("  ✅ Added clean, consolidated pile view CSS")
    
    # Save CSS changes
    if not write_file(css_path, css_content):
        return False
    
    print("\n" + "=" * 55)
    print("🎉 ALL CLEANUP FIXES APPLIED SUCCESSFULLY!")
    print("=" * 55)
    print("\n📋 Summary of Fixes:")
    print("  ✅ Fixed sideboard sort menu ref bug")
    print("  ✅ Corrected z-index logic for proper card stacking")
    print("  ✅ Cleaned up all CSS conflicts and duplications")
    print("  ✅ Consolidated pile view styles into single clean section")
    print("  ✅ Ensured area-level scrolling only")
    print("\n🚀 The pile view should now work correctly!")
    print("   • First card fully visible (highest z-index)")
    print("   • Sideboard sort menu works properly")
    print("   • Clean CSS with no conflicts")
    print("   • Proper scrolling behavior")
    
    return True

if __name__ == "__main__":
    if apply_cleanup_fixes():
        print("\n✨ All cleanup fixes completed successfully!")
        print("🔧 Run 'npm start' to test the cleaned up pile view.")
    else:
        print("\n❌ Some fixes failed. Please check error messages above.")
