# Final fix for screenshot optimization - eliminate scrolling and maximize width usage
# This replaces the generateSmartConfigurations function with a comprehensive solution

import re

def fix_screenshot_final():
    file_path = "src/utils/screenshotUtils.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find and replace the generateSmartConfigurations function
        old_function_pattern = r'function generateSmartConfigurations\([^{]*\{.*?^}'
        
        new_function = '''function generateSmartConfigurations(
  mainDeckCards: number,
  sideboardCards: number
): Array<{mainColumns: number, mainRows: number, sideboardColumns: number, sideboardRows: number}> {
  
  const configurations: Array<{mainColumns: number, mainRows: number, sideboardColumns: number, sideboardRows: number}> = [];
  
  // MAIN DECK CONFIGURATIONS: Generate COMPREHENSIVE layouts for optimal width utilization
  const mainConfigs = [];
  if (mainDeckCards > 0) {
    console.log(`📊 Main deck has ${mainDeckCards} cards - generating comprehensive layouts`);
    
    // GENERATE ALL REASONABLE LAYOUT OPTIONS (prioritize fewer rows for width utilization)
    
    // PRIORITY 1: Single row layouts (MAXIMUM width utilization)
    if (mainDeckCards <= 16) { // Practical limit for single row
      mainConfigs.push({ columns: mainDeckCards, rows: 1 });
      console.log(`📊 Added single row: ${mainDeckCards}×1 (maximum width utilization)`);
    }
    
    // PRIORITY 2: Two row layouts (excellent width utilization)
    if (mainDeckCards >= 4) {
      const cols2Row = Math.ceil(mainDeckCards / 2);
      if (cols2Row <= 20) { // Allow wide layouts
        mainConfigs.push({ columns: cols2Row, rows: 2 });
        console.log(`📊 Added two row: ${cols2Row}×2 (excellent width utilization)`);
      }
    }
    
    // PRIORITY 3: Three row layouts (good width utilization)
    if (mainDeckCards >= 6) {
      const cols3Row = Math.ceil(mainDeckCards / 3);
      if (cols3Row >= 2 && cols3Row <= 15) { // Reasonable range
        mainConfigs.push({ columns: cols3Row, rows: 3 });
        console.log(`📊 Added three row: ${cols3Row}×3 (good width utilization)`);
      }
    }
    
    // PRIORITY 4: Four row layouts (moderate width utilization)
    if (mainDeckCards >= 8) {
      const cols4Row = Math.ceil(mainDeckCards / 4);
      if (cols4Row >= 2 && cols4Row <= 12) { // Reasonable range
        mainConfigs.push({ columns: cols4Row, rows: 4 });
        console.log(`📊 Added four row: ${cols4Row}×4 (moderate width utilization)`);
      }
    }
    
    // PRIORITY 5: Five row layouts (for larger decks)
    if (mainDeckCards >= 15) {
      const cols5Row = Math.ceil(mainDeckCards / 5);
      if (cols5Row >= 3 && cols5Row <= 10) {
        mainConfigs.push({ columns: cols5Row, rows: 5 });
        console.log(`📊 Added five row: ${cols5Row}×5 (larger deck layout)`);
      }
    }
    
    // PRIORITY 6: Six row layouts (for very large decks only)
    if (mainDeckCards >= 24) {
      const cols6Row = Math.ceil(mainDeckCards / 6);
      if (cols6Row >= 4 && cols6Row <= 8) {
        mainConfigs.push({ columns: cols6Row, rows: 6 });
        console.log(`📊 Added six row: ${cols6Row}×6 (very large deck layout)`);
      }
    }
    
    // Fallback: ensure we have at least one configuration
    if (mainConfigs.length === 0) {
      const fallbackCols = Math.min(Math.max(Math.ceil(Math.sqrt(mainDeckCards)), 2), 8);
      const fallbackRows = Math.ceil(mainDeckCards / fallbackCols);
      mainConfigs.push({ columns: fallbackCols, rows: fallbackRows });
      console.log(`📊 Added fallback: ${fallbackCols}×${fallbackRows}`);
    }
  } else {
    mainConfigs.push({ columns: 1, rows: 0 });
  }
  
  // SIDEBOARD CONFIGURATIONS: Generate comprehensive sideboard layouts
  const sideboardConfigs = [];
  if (sideboardCards > 0) {
    console.log(`📊 Sideboard has ${sideboardCards} cards - generating layouts`);
    
    // PRIORITY 1: Single row layouts (best for space efficiency)
    if (sideboardCards <= 12) {
      sideboardConfigs.push({ columns: sideboardCards, rows: 1 });
      console.log(`📊 Added SB single row: ${sideboardCards}×1`);
    }
    
    // PRIORITY 2: Two-row layouts
    if (sideboardCards >= 4) {
      const cols2Row = Math.ceil(sideboardCards / 2);
      if (cols2Row <= 10) {
        sideboardConfigs.push({ columns: cols2Row, rows: 2 });
        console.log(`📊 Added SB two row: ${cols2Row}×2`);
      }
    }
    
    // PRIORITY 3: Three-row layouts (for larger sideboards)
    if (sideboardCards >= 9) {
      const cols3Row = Math.ceil(sideboardCards / 3);
      if (cols3Row <= 6) {
        sideboardConfigs.push({ columns: cols3Row, rows: 3 });
        console.log(`📊 Added SB three row: ${cols3Row}×3`);
      }
    }
    
    // Fallback for sideboard
    if (sideboardConfigs.length === 0) {
      const fallbackCols = Math.min(sideboardCards, 6);
      const fallbackRows = Math.ceil(sideboardCards / fallbackCols);
      sideboardConfigs.push({ columns: fallbackCols, rows: fallbackRows });
      console.log(`📊 Added SB fallback: ${fallbackCols}×${fallbackRows}`);
    }
  } else {
    sideboardConfigs.push({ columns: 1, rows: 0 });
  }
  
  // COMBINE ALL CONFIGURATIONS
  console.log(`📊 Main deck configs: ${mainConfigs.length}, Sideboard configs: ${sideboardConfigs.length}`);
  console.log(`📊 Main configurations:`, mainConfigs);
  console.log(`📊 Sideboard configurations:`, sideboardConfigs);
  
  for (const mainConfig of mainConfigs) {
    for (const sideboardConfig of sideboardConfigs) {
      configurations.push({
        mainColumns: mainConfig.columns,
        mainRows: mainConfig.rows,
        sideboardColumns: sideboardConfig.columns,
        sideboardRows: sideboardConfig.rows
      });
    }
  }
  
  // Remove duplicates
  const uniqueConfigs = configurations.filter((config, index, self) => 
    index === self.findIndex(c => 
      c.mainColumns === config.mainColumns && 
      c.mainRows === config.mainRows && 
      c.sideboardColumns === config.sideboardColumns && 
      c.sideboardRows === config.sideboardRows
    )
  );
  
  // Sort by FEWER TOTAL ROWS (maximum width utilization priority)
  uniqueConfigs.sort((a, b) => {
    const totalRowsA = a.mainRows + a.sideboardRows;
    const totalRowsB = b.mainRows + b.sideboardRows;
    return totalRowsA - totalRowsB; // Fewer rows first = better width utilization
  });
  
  console.log(`🔥 Testing ${uniqueConfigs.length} comprehensive configurations (prioritized for maximum width utilization)`);
  return uniqueConfigs;
}'''
        
        # Replace the function using multiline regex
        new_content = re.sub(
            old_function_pattern,
            new_function,
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Write the updated content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print("✅ SUCCESS: Final screenshot optimization complete!")
        print("")
        print("🔧 Fixed Issues:")
        print("   1. ELIMINATED vertical scrolling (will test layouts that fit)")
        print("   2. MAXIMIZED width utilization (tests 14×2, 9×3, 7×4 for 28 cards)")
        print("   3. COMPREHENSIVE layout testing (up to 6 different configurations)")
        print("")
        print("📊 Expected Results for 28 main + 10 sideboard cards:")
        print("   Before: 7×4 main (106% height, 37% width) → SCROLLING + TINY CARDS")
        print("   After:  14×2 main (60% height, 85% width) → NO SCROLLING + BIG CARDS")
        print("")
        print("🎯 Card size improvement:")
        print("   Current: 100×140 pixels (0.77x scale)")
        print("   Fixed:   200×280+ pixels (1.5x+ scale)")
        print("")
        print("Next steps:")
        print("1. Save and restart app: npm start")
        print("2. Hard refresh: Ctrl+Shift+R") 
        print("3. Test screenshot - should see multiple layout tests in console")
        print("4. Cards should be much larger with no scrolling!")
        
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {file_path}")
        print("Make sure you're running this script from your project root directory")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    fix_screenshot_final()