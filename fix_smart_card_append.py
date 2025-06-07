#!/usr/bin/env python3
"""
Fix Smart Card Append logic to properly split existing vs new cards
This should resolve the pagination issue where cards are jumping from A to C
"""

import re

def fix_smart_card_append():
    """Fix the Smart Card Append logic to properly handle existing vs new cards"""
    print("🔧 Fixing Smart Card Append logic...")
    
    # Read the current file
    try:
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ MTGOLayout.tsx not found")
        return False
    
    # Fix the Smart Card Append calculation
    # Find the problematic line
    old_calculation = r'const existingCardsCount = Math\.min\(loadedCardsCount - \(cards\.length > loadedCardsCount \? 175 : 0\), sortedCollectionCards\.length\);'
    new_calculation = 'const existingCardsCount = Math.min(loadedCardsCount, sortedCollectionCards.length);'
    
    if re.search(old_calculation, content):
        content = re.sub(old_calculation, new_calculation, content)
        print("✅ Fixed existingCardsCount calculation")
    else:
        print("⚠️ Could not find the problematic calculation - checking alternative patterns...")
        
        # Try to find and fix the line manually
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'existingCardsCount' in line and 'loadedCardsCount -' in line:
                print(f"📍 Found line {i + 1}: {line.strip()}")
                # Replace with simpler logic
                lines[i] = '                    const existingCardsCount = Math.min(loadedCardsCount, sortedCollectionCards.length);'
                content = '\n'.join(lines)
                print("✅ Fixed existingCardsCount calculation (manual replacement)")
                break
        else:
            print("❌ Could not find existingCardsCount calculation")
            return False
    
    # Also improve the useEffect to be more reliable
    # Change the useEffect to track previous length to avoid unnecessary updates
    useeffect_pattern = r'useEffect\(\(\) => \{\s*if \(cards\.length > 0\) \{\s*setLoadedCardsCount\(cards\.length\);\s*\}\s*\}, \[cards\.length\]\);'
    improved_useeffect = '''useEffect(() => {
    // Only update if cards length actually increased (Load More scenario)
    if (cards.length > loadedCardsCount) {
      setLoadedCardsCount(cards.length);
    }
  }, [cards.length, loadedCardsCount]);'''
    
    if re.search(useeffect_pattern, content, re.DOTALL):
        content = re.sub(useeffect_pattern, improved_useeffect, content, flags=re.DOTALL)
        print("✅ Improved useEffect logic for loadedCardsCount")
    else:
        print("⚠️ Could not find useEffect pattern to improve")
    
    # Write the fixed content
    try:
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully fixed Smart Card Append logic")
        print("🎯 Changes made:")
        print("  1. Simplified existingCardsCount calculation")
        print("  2. Improved useEffect to only update when cards actually increase")
        print("📝 This should fix the B cards pagination issue")
        return True
        
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

if __name__ == "__main__":
    fix_smart_card_append()
