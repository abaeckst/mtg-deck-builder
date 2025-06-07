#!/usr/bin/env python3

import os
import sys

def update_filterpanel_css_polish():
    """Update FilterPanel.css with Keyrune mana symbols, compact spacing, and professional polish"""
    
    filename = "src/components/FilterPanel.css"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CSS updates for professional polish with Keyrune symbols
    updates = [
        # 1. Add Keyrune font face declaration at the top
        (
            '/* src/components/FilterPanel.css - Phase 4B: Professional MTGO-style filter styling */',
            '''/* src/components/FilterPanel.css - Phase 4B: Professional MTGO-style filter styling */

/* Keyrune Font for MTG Mana Symbols */
@font-face {
  font-family: 'Keyrune';
  src: url('/fonts/keyrune.woff2') format('woff2'),
       url('/fonts/keyrune.woff') format('woff'),
       url('/fonts/keyrune.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}''',
            "Add Keyrune font declaration"
        ),
        
        # 2. Add new color filter grid layouts for 2-row arrangement
        (
            '/* Enhanced Filter Panel Layout */',
            '''/* Color Filter Grid - 2 Row Layout */
.color-filter-grid-row1,
.color-filter-grid-row2 {
  display: flex;
  gap: 6px;
  margin-bottom: 6px;
  justify-content: center;
}

.color-filter-grid-row1 {
  /* Row 1: W U B R G */
}

.color-filter-grid-row2 {
  /* Row 2: C GOLD */
  justify-content: center;
  gap: 12px;
}

/* Mana Symbol Buttons with Keyrune Font */
.color-button {
  font-family: 'Keyrune', Arial, sans-serif;
  font-size: 20px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid transparent;
  background: #333333;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  font-weight: normal;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
}

.color-button:hover:not(.disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.color-button.selected {
  border-color: #3b82f6;
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.8), inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

.color-button.disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

/* Individual Mana Symbol Styling */
.color-button.color-w {
  background: linear-gradient(135deg, #FFFBD5 0%, #F0F0F0 100%);
  color: #333333;
  border-color: #E0E0E0;
}

.color-button.color-w::before {
  content: "\\e600"; /* Keyrune white mana symbol */
}

.color-button.color-u {
  background: linear-gradient(135deg, #0E68AB 0%, #1E88E5 100%);
  color: #ffffff;
  border-color: #1976D2;
}

.color-button.color-u::before {
  content: "\\e601"; /* Keyrune blue mana symbol */
}

.color-button.color-b {
  background: linear-gradient(135deg, #150B00 0%, #2D1B00 100%);
  color: #ffffff;
  border-color: #4A3000;
}

.color-button.color-b::before {
  content: "\\e602"; /* Keyrune black mana symbol */
}

.color-button.color-r {
  background: linear-gradient(135deg, #D32F2F 0%, #F44336 100%);
  color: #ffffff;
  border-color: #C62828;
}

.color-button.color-r::before {
  content: "\\e603"; /* Keyrune red mana symbol */
}

.color-button.color-g {
  background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
  color: #ffffff;
  border-color: #1B5E20;
}

.color-button.color-g::before {
  content: "\\e604"; /* Keyrune green mana symbol */
}

.color-button.color-c {
  background: linear-gradient(135deg, #9E9E9E 0%, #BDBDBD 100%);
  color: #333333;
  border-color: #757575;
}

.color-button.color-c::before {
  content: "\\e904"; /* Keyrune colorless symbol */
}

/* Enhanced Filter Panel Layout */''',
            "Add comprehensive mana symbol styling with Keyrune"
        ),
        
        # 3. Update Gold Button styling with proper blue glow
        (
            '.color-gold.selected {\n  background: #FFD700;\n  box-shadow: 0 0 12px rgba(255, 215, 0, 0.8), inset 0 2px 4px rgba(0, 0, 0, 0.2);\n  border-color: #FFA500;\n}',
            '''.color-gold.selected {
  background: #FFD700;
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.8), 0 0 8px rgba(255, 215, 0, 0.6), inset 0 2px 4px rgba(0, 0, 0, 0.2);
  border-color: #3b82f6;
  color: #000000;
}''',
            "Fix gold button blue glow when selected"
        ),
        
        # 4. Add compact spacing for sections
        (
            '.section-content {\n  padding: 12px;\n  background: #2a2a2a;\n  border-left: 1px solid #404040;\n  border-right: 1px solid #404040;\n  border-bottom: 1px solid #404040;\n  animation: expandSection 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);\n}',
            '''.section-content {
  padding: 8px 12px;
  background: #2a2a2a;
  border-left: 1px solid #404040;
  border-right: 1px solid #404040;
  border-bottom: 1px solid #404040;
  animation: expandSection 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}

.section-content .filter-group {
  margin-bottom: 0;
  padding: 0;
}

.section-content .filter-group label {
  font-size: 11px;
  margin-bottom: 4px;
  display: block;
  color: #cccccc;
}''',
            "Add compact spacing for section content"
        ),
        
        # 5. Add enhanced search group styling
        (
            '/* Scrollbar styling for filter content */',
            '''/* Search Group Enhanced Styling */
.search-group {
  margin-bottom: 12px;
}

.search-group .search-input {
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

/* Format Group Styling */
.format-group select {
  width: 100%;
  padding: 6px 8px;
  background: #1a1a1a;
  border: 1px solid #404040;
  border-radius: 4px;
  color: white;
  font-size: 12px;
}

/* Multi-select grid improvements */
.multi-select-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 4px;
  margin-top: 6px;
}

.type-button,
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
}

.type-button:hover,
.rarity-button:hover {
  background: #404040;
}

.type-button.selected,
.rarity-button.selected {
  background: #3b82f6;
  border-color: #3b82f6;
}

/* Range filter improvements */
.range-filter {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
}

.range-filter span {
  font-size: 11px;
  color: #cccccc;
}

.range-input,
.stat-input {
  width: 60px;
  padding: 4px 6px;
  background: #1a1a1a;
  border: 1px solid #404040;
  border-radius: 3px;
  color: white;
  font-size: 11px;
}

/* Stats filter layout */
.stats-filter {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-row span {
  font-size: 11px;
  color: #cccccc;
  min-width: 60px;
}

/* Rarity grid */
.rarity-filter-grid {
  display: flex;
  gap: 4px;
  margin-top: 6px;
}

.rarity-button {
  flex: 1;
  min-width: 40px;
}

/* Quick actions styling */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.quick-actions button {
  padding: 6px 8px;
  background: #404040;
  border: 1px solid #555555;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 11px;
  transition: background-color 0.2s ease;
}

.quick-actions button:hover {
  background: #505050;
}

/* Panel minimum width and overflow handling */
.mtgo-filter-panel {
  min-width: 280px;
  max-width: 400px;
  overflow-x: hidden;
}

.filter-content {
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 4px;
}

/* Scrollbar styling for filter content */''',
            "Add comprehensive styling improvements"
        ),
        
        # 6. Update animation for more compact expansion
        (
            '@keyframes expandSection {\n  from {\n    opacity: 0;\n    max-height: 0;\n    padding-top: 0;\n    padding-bottom: 0;\n  }\n  to {\n    opacity: 1;\n    max-height: 200px;\n    padding-top: 12px;\n    padding-bottom: 12px;\n  }\n}',
            '''@keyframes expandSection {
  from {
    opacity: 0;
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
  }
  to {
    opacity: 1;
    max-height: 180px;
    padding-top: 8px;
    padding-bottom: 8px;
  }
}''',
            "Update animation for compact spacing"
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
    success = update_filterpanel_css_polish()
    sys.exit(0 if success else 1)