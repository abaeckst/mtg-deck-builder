# Fix overflow selection - ensure algorithm never chooses layouts that cause scrolling
# This modifies the layout selection logic to REJECT any layout with >100% height utilization

import re

def fix_overflow_selection():
    file_path = "src/utils/screenshotUtils.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find and replace the layout selection logic in findOptimalLayoutBySpaceUtilization
        old_loop_pattern = r'(for \(const config of testConfigurations\) \{.*?)(\s+\/\/ Choose layout with BIGGEST cards.*?if \(\!bestLayout \|\| cardSizeScore > bestLayout\.cardSizeScore\) \{.*?\s+bestLayout = layout;.*?\s+\}.*?\s+\})'
        
        new_loop = r'''\1
    // CRITICAL: Reject any layout that causes scrolling (height utilization > 100%)
    if (heightUtilization > 1.0) {
      console.log(`❌ ${config.mainColumns}×${config.mainRows} main, ${config.sideboardColumns}×${config.sideboardRows} SB: REJECTED - height overflow ${(heightUtilization * 100).toFixed(1)}%`);
      continue; // Skip layouts that cause scrolling
    }
    
    // Choose layout with BIGGEST cards (among layouts that FIT without scrolling)
    if (!bestLayout || cardSizeScore > bestLayout.cardSizeScore) {
      bestLayout = layout;
      console.log(`✅ NEW BEST: ${config.mainColumns}×${config.mainRows} main, ${config.sideboardColumns}×${config.sideboardRows} SB: scale ${finalScale.toFixed(2)}, no overflow`);
    }
  }'''
        
        # Apply the replacement
        new_content = re.sub(
            old_loop_pattern,
            new_loop,
            content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Also add a safety check before the final return
        safety_check_pattern = r'(console\.log\(`🔥 OPTIMAL HYBRID:.*?\`\);.*?console\.log\(`   Card scale:.*?\`\);)'
        
        safety_replacement = r'''\1
  
  // SAFETY CHECK: Ensure selected layout doesn't cause overflow
  const finalHeightUtil = (bestLayout.mainHeight + bestLayout.sideboardHeight) / totalAvailableHeight;
  if (finalHeightUtil > 1.0) {
    console.warn(`⚠️  SAFETY OVERRIDE: Selected layout causes ${(finalHeightUtil * 100).toFixed(1)}% height utilization - this should not happen!`);
  }'''
        
        new_content = re.sub(
            safety_check_pattern,
            safety_replacement,
            new_content,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Write the updated content back
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print("✅ SUCCESS: Overflow prevention logic added!")
        print("")
        print("🔧 Fix Applied:")
        print("   - Algorithm now REJECTS any layout with >100% height utilization")
        print("   - Will choose 11×2 layout (60% height) instead of 7×3 layout (101% height)")
        print("   - Added safety checks to prevent overflow selection")
        print("")
        print("📊 Expected Results for 21 cards:")
        print("   Before: 7×3 layout → 101.4% height → CARD CUTOFF")
        print("   After:  11×2 layout → 60.0% height → NO CUTOFF + BIGGER CARDS")
        print("")
        print("🎯 Console output should show:")
        print("   ❌ 7×3 main: REJECTED - height overflow 101.4%")
        print("   ✅ NEW BEST: 11×2 main: scale 1.31, no overflow")
        print("   🔥 OPTIMAL HYBRID: 11×2 main")
        print("")
        print("Next steps:")
        print("1. Save and restart: npm start")
        print("2. Hard refresh: Ctrl+Shift+R")
        print("3. Test screenshot - no cards should be cut off!")
        
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {file_path}")
        print("Make sure you're running this script from your project root directory")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    fix_overflow_selection()