# Fix screenshot optimization to prioritize width utilization
# This replaces the generateSmartConfigurations function with a corrected version

import re

def fix_screenshot_optimization():
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
  
  // MAIN DECK CONFIGURATIONS: PRIORITIZE WIDTH UTILIZATION (FEWER ROWS = MORE COLUMNS = BETTER WIDTH USE)
  const mainConfigs = [];
  if (mainDeckCards > 0) {
    console.log(`📊 Main deck has ${mainDeckCards} cards`);
    
    // CORRECTED PRIORITY: FEWER ROWS = MORE COLUMNS = BETTER WIDTH UTILIZATION
    
    // PRIORITY 1: Single row layouts (MAXIMUM width utilization)
    if (mainDeckCards <= 12) { // Allow up to 12 cards in single row
      mainConfigs.push({ columns: mainDeckCards, rows: 1 });
      console.log(`📊 Added single row: ${mainDeckCards}×1 (maximum width utilization)`);
    }
    
    // PRIORITY 2: Two row layouts (good width utilization)
    if (mainDeckCards > 4) {
      const cols2Row = Math.ceil(mainDeckCards / 2);
      if (cols2Row <= 10) { // Don't make rows too wide
        mainConfigs.push({ columns: cols2Row, rows: 2 });
        console.log(`📊 Added two row: ${cols2Row}×2 (good width utilization)`);
      }
    }
    
    // PRIORITY 3: Three row layouts (moderate width utilization)
    if (mainDeckCards > 6) {
      const cols3Row = Math.ceil(mainDeckCards / 3);
      if (cols3Row <= 8) {
        mainConfigs.push({ columns: cols3Row, rows: 3 });
        console.log(`📊 Added three row: ${cols3Row}×3 (moderate width utilization)`);
      }
    }
    
    // PRIORITY 4: Four row layouts (for larger decks only)
    if (mainDeckCards > 12) {
      const cols4Row = Math.ceil(mainDeckCards / 4);
      if (cols4Row >= 4 && cols4Row <= 8) {
        mainConfigs.push({ columns: cols4Row, rows: 4 });
        console.log(`📊 Added four row: ${cols4Row}×4 (larger deck layout)`);
      }
    }
    
    // Fallback: ensure we have at least one configuration
    if (mainConfigs.length === 0) {
      const fallbackCols = Math.min(mainDeckCards, 6);
      const fallbackRows = Math.ceil(mainDeckCards / fallbackCols);
      mainConfigs.push({ columns: fallbackCols, rows: fallbackRows });
      console.log(`📊 Added fallback: ${fallbackCols}×${fallbackRows}`);
    }
  } else {
    mainConfigs.push({ columns: 1, rows: 0 });
  }
  
  // SIDEBOARD CONFIGURATIONS: Favor horizontal layouts (prioritize single row)
  const sideboardConfigs = [];
  if (sideboardCards > 0) {
    // PRIORITY 1: Single row layouts (best for card size)
    if (sideboardCards <= 8) { // Allow up to 8 cards in single row
      sideboardConfigs.push({ columns: sideboardCards, rows: 1 });
    }
    
    // PRIORITY 2: Two-row layouts only if necessary
    if (sideboardCards > 4) {
      const cols2Row = Math.ceil(sideboardCards / 2);
      if (cols2Row <= 6) { // Don't make rows too wide
        sideboardConfigs.push({ columns: cols2Row, rows: 2 });
      }
    }
    
    // Fallback: ensure we have at least one configuration
    if (sideboardConfigs.length === 0) {
      sideboardConfigs.push({ columns: Math.min(sideboardCards, 6), rows: Math.ceil(sideboardCards / 6) });
    }
  } else {
    sideboardConfigs.push({ columns: 1, rows: 0 });
  }
  
  // COMBINE CONFIGURATIONS
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
  
  // Remove duplicates and sort by width utilization potential (fewer rows = better)
  const uniqueConfigs = configurations.filter((config, index, self) => 
    index === self.findIndex(c => 
      c.mainColumns === config.mainColumns && 
      c.mainRows === config.mainRows && 
      c.sideboardColumns === config.sideboardColumns && 
      c.sideboardRows === config.sideboardRows
    )
  );
  
  // Sort by FEWER ROWS (better width utilization)
  uniqueConfigs.sort((a, b) => {
    const totalRowsA = a.mainRows + a.sideboardRows;
    const totalRowsB = b.mainRows + b.sideboardRows;
    return totalRowsA - totalRowsB; // Fewer rows first = better width utilization
  });
  
  console.log(`🔥 Testing ${uniqueConfigs.length} smart configurations (prioritized for width utilization)`);
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
        
        print("✅ SUCCESS: Screenshot optimization fixed!")
        print("🔥 Now prioritizes width utilization for bigger cards")
        print("📊 5 cards should now use 5×1 layout instead of 2×3")
        print("🎯 Expected card scale should be 3.0x+ instead of 1.6x")
        print("")
        print("Next steps:")
        print("1. Save and close any text editors")
        print("2. Restart your app: npm start")
        print("3. Hard refresh browser: Ctrl+Shift+R")
        print("4. Test screenshot with your 5-card deck")
        print("5. Cards should be much larger!")
        
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {file_path}")
        print("Make sure you're running this script from your project root directory")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    fix_screenshot_optimization()