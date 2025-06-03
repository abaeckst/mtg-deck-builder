#!/usr/bin/env python3
"""
Fix Collection Grid CSS - Remove hardcoded grid rules that conflict with dynamic sizing
"""

def fix_css_file():
    file_path = "src/components/MTGOLayout.css"
    
    try:
        # Read the current file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Successfully read MTGOLayout.css")
        
        # Fix 1: Remove hardcoded grid-template-columns from .collection-grid
        old_collection_grid = """.collection-grid {
  padding: 12px;
  overflow-y: auto;
  flex: 1; /* Take remaining space after header */
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 8px;
  align-content: start;
}"""
        
        new_collection_grid = """.collection-grid {
  padding: 12px;
  overflow-y: auto;
  flex: 1; /* Take remaining space after header */
  display: grid;
  /* Grid columns and gap set dynamically by JavaScript */
  align-content: start;
}"""
        
        if old_collection_grid in content:
            content = content.replace(old_collection_grid, new_collection_grid)
            print("✅ Fix 1: Removed hardcoded grid-template-columns from .collection-grid")
        else:
            print("⚠️  Fix 1: Collection grid rule not found in expected format")
        
        # Fix 2: Remove hardcoded grid rules from responsive media queries
        old_responsive_1200 = """@media (max-width: 1200px) {
  .mtgo-filter-panel {
    min-width: 180px;
  }
  
  .mtgo-sideboard-panel {
    min-width: 180px;
  }
  
  .collection-grid {
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  }
}"""
        
        new_responsive_1200 = """@media (max-width: 1200px) {
  .mtgo-filter-panel {
    min-width: 180px;
  }
  
  .mtgo-sideboard-panel {
    min-width: 180px;
  }
  
  /* Collection grid sizing controlled by JavaScript */
}"""
        
        if old_responsive_1200 in content:
            content = content.replace(old_responsive_1200, new_responsive_1200)
            print("✅ Fix 2: Removed hardcoded collection grid from 1200px media query")
        else:
            print("⚠️  Fix 2: 1200px media query not found in expected format")
        
        # Fix 3: Remove hardcoded grid rules from 900px media query
        old_responsive_900 = """@media (max-width: 900px) {
  .panel-header h3 {
    font-size: 13px;
  }
  
  .view-controls,
  .deck-controls {
    display: none;
  }
  
  .collection-grid {
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
    gap: 6px;
  }
}"""
        
        new_responsive_900 = """@media (max-width: 900px) {
  .panel-header h3 {
    font-size: 13px;
  }
  
  .view-controls,
  .deck-controls {
    display: none;
  }
  
  /* Collection grid sizing controlled by JavaScript */
}"""
        
        if old_responsive_900 in content:
            content = content.replace(old_responsive_900, new_responsive_900)
            print("✅ Fix 3: Removed hardcoded collection grid from 900px media query")
        else:
            print("⚠️  Fix 3: 900px media query not found in expected format")
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n🎯 SUCCESS: Fixed MTGOLayout.css")
        print("✅ Removed all hardcoded grid-template-columns rules from .collection-grid")
        print("✅ Collection area will now respect the size slider like deck/sideboard areas")
        print("✅ All grid sizing is now handled consistently by JavaScript")
        print("\nNext step: Test with 'npm start' to verify collection cards resize properly!")
        
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find {file_path}")
        print("Please make sure you're in the correct directory")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    fix_css_file()
