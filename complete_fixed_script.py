#!/usr/bin/env python3
"""
Complete Fixed CSS Update Script for Phase 3G
Adds ListView and AdaptiveHeader styles to MTGOLayout.css
"""

import os

def update_css_file():
    """Add ListView styles to MTGOLayout.css"""
    
    file_path = "src/components/MTGOLayout.css"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File {file_path} not found!")
        return False
    
    try:
        # Read the current file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("📖 Reading MTGOLayout.css...")
        
        # Complete ListView styles to add
        listview_styles = """

/* ===== LIST VIEW COMPONENT STYLES ===== */

/* Main list view container */
.list-view {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.list-view-container {
  flex: 1;
  overflow-x: auto;
  overflow-y: auto;
}

/* List view table */
.list-view-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  font-size: 12px;
  color: #ffffff;
}

/* Header styles */
.list-view-header-row {
  background-color: #333333;
  border-bottom: 2px solid #555555;
  position: sticky;
  top: 0;
  z-index: 10;
}

.list-view-header-cell {
  padding: 8px 12px;
  text-align: left;
  font-weight: 600;
  color: #ffffff;
  border-right: 1px solid #555555;
  user-select: none;
  position: relative;
}

.list-view-header-cell.sortable {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.list-view-header-cell.sortable:hover {
  background-color: #404040;
}

.list-view-header-cell.active {
  background-color: #3b82f6;
  color: #ffffff;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sort-indicator {
  margin-left: 4px;
  font-size: 12px;
  color: #ffffff;
}

/* Column resize handle */
.column-resize-handle:hover {
  background-color: rgba(59, 130, 246, 0.5) !important;
}

/* Row styles */
.list-view-row {
  transition: background-color 0.2s ease;
  cursor: pointer;
  border-bottom: 1px solid #2a2a2a;
}

.list-view-row.even {
  background-color: #2a2a2a;
}

.list-view-row.odd {
  background-color: #1e1e1e;
}

.list-view-row:hover {
  background-color: #3a3a3a !important;
}

.list-view-row.selected {
  background-color: rgba(59, 130, 246, 0.3) !important;
  border-color: #3b82f6;
}

/* Cell styles */
.list-view-cell {
  padding: 6px 12px;
  border-right: 1px solid #333333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  vertical-align: middle;
}

/* Specific cell content styles */
.card-name {
  font-weight: 500;
  color: #ffffff;
}

.mana-cost {
  font-family: 'Courier New', monospace;
  color: #fbbf24;
  font-weight: bold;
}

.type-line {
  color: #cccccc;
  font-style: italic;
}

.power, .toughness {
  font-weight: bold;
  color: #ef4444;
  text-align: center;
  display: block;
}

.oracle-text {
  color: #cccccc;
  font-size: 11px;
  line-height: 1.3;
}

/* Color circles */
.color-circles {
  display: flex;
  gap: 2px;
  align-items: center;
}

.color-circle {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
  border: 1px solid #555555;
  flex-shrink: 0;
}

.color-circle.color-w { background-color: #fffbd5; color: #000000; }
.color-circle.color-u { background-color: #0e68ab; color: #ffffff; }
.color-circle.color-b { background-color: #150b00; color: #ffffff; }
.color-circle.color-r { background-color: #d3202a; color: #ffffff; }
.color-circle.color-g { background-color: #00733e; color: #ffffff; }
.color-circle.color-c { background-color: #ccc2c0; color: #000000; }

/* Quantity controls */
.quantity-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.quantity-display {
  font-weight: bold;
  color: #ffffff;
  min-width: 20px;
  text-align: center;
}

.quantity-buttons {
  display: none;
  gap: 2px;
}

.list-view-row:hover .quantity-buttons {
  display: flex;
}

.quantity-btn {
  width: 20px;
  height: 20px;
  border: 1px solid #555555;
  background-color: #404040;
  color: #ffffff;
  cursor: pointer;
  border-radius: 3px;
  font-size: 12px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.quantity-btn:hover:not(:disabled) {
  background-color: #4a4a4a;
  transform: scale(1.1);
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-btn.minus:hover:not(:disabled) {
  background-color: #ef4444;
}

.quantity-btn.plus:hover:not(:disabled) {
  background-color: #10b981;
}

/* Empty state */
.list-view-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #888888;
  font-style: italic;
  border: 2px dashed #404040;
  border-radius: 8px;
  margin: 20px;
}

.empty-message {
  font-size: 16px;
}

/* Scrollbar styling for list view */
.list-view-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.list-view-container::-webkit-scrollbar-track {
  background-color: #1a1a1a;
  border-radius: 4px;
}

.list-view-container::-webkit-scrollbar-thumb {
  background-color: #404040;
  border-radius: 4px;
}

.list-view-container::-webkit-scrollbar-thumb:hover {
  background-color: #555555;
}

.list-view-container::-webkit-scrollbar-corner {
  background-color: #1a1a1a;
}

/* ===== ADAPTIVE HEADER STYLES ===== */

.adaptive-header {
  position: relative;
}

.header-control {
  display: flex;
  align-items: center;
}

.header-control.in-dropdown {
  width: 100%;
}

.header-dropdown-toggle:hover {
  background-color: #4a4a4a !important;
}

.dropdown-item:last-child {
  border-bottom: none !important;
}

/* Header control specific styles */
.header-control-button button {
  background-color: #404040;
  color: #ffffff;
  border: 1px solid #555555;
  padding: 4px 8px;
  border-radius: 3px;
  font-size: 11px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.header-control-button button:hover {
  background-color: #4a4a4a;
}

.header-control-button button.active {
  background-color: #3b82f6;
  border-color: #2563eb;
}

.header-control-slider input[type="range"] {
  width: 120px;
  height: 16px;
  background: linear-gradient(to right, #404040, #666666);
  border-radius: 8px;
  outline: none;
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
}

.header-control-slider input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  background: #3b82f6;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #ffffff;
}

/* Smooth transitions */
.adaptive-header * {
  transition: all 0.2s ease;
}

/* ===== END LIST VIEW & ADAPTIVE HEADER STYLES ===== */"""
        
        # Check if ListView styles already exist
        if "LIST VIEW COMPONENT STYLES" not in content:
            content += listview_styles
            print("✅ Added ListView and AdaptiveHeader styles to CSS")
        else:
            print("ℹ️ ListView styles already exist in CSS file")
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating CSS file: {e}")
        return False

def main():
    """Main execution function"""
    print("🚀 Starting CSS Update for Phase 3G...")
    print("📋 This script will add ListView and AdaptiveHeader styles to MTGOLayout.css")
    print()
    
    # Update CSS file
    if not update_css_file():
        print("❌ Failed to update MTGOLayout.css")
        return False
    
    print()
    print("🎉 CSS Update Complete!")
    print()
    print("📋 Summary of changes:")
    print("  ✅ Added comprehensive ListView table styles")
    print("  ✅ Added sortable column header styles")
    print("  ✅ Added row hover and selection styles")
    print("  ✅ Added color circle and quantity control styles")
    print("  ✅ Added AdaptiveHeader responsive styles")
    print("  ✅ Added proper scrollbar styling")
    print()
    print("🔄 Next steps:")
    print("  1. The MTGOLayout.tsx file is already updated with ListView integration")
    print("  2. Create the ListView.tsx and AdaptiveHeader.tsx component files")
    print("  3. Test the application to ensure List view works correctly")
    print()
    print("🎯 All ListView CSS styles are now available!")

if __name__ == "__main__":
    main()