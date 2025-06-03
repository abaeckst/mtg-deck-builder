#!/usr/bin/env python3
"""
Quick fixes for screenshot layout - more columns and larger manual sizes
"""

import os

def fix_screenshot_utils():
    """Update screenshotUtils.ts with more columns and larger manual sizes"""
    
    utils_path = "src/utils/screenshotUtils.ts"
    
    if not os.path.exists(utils_path):
        print(f"❌ Error: {utils_path} not found!")
        return
    
    print(f"Reading {utils_path}...")
    with open(utils_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update SIZE_OVERRIDES to be much larger
    old_size_overrides = '''export const SIZE_OVERRIDES = {
  small: 0.6,   // 60% of normal card size
  medium: 0.8,  // 80% of normal card size  
  large: 1.0,   // 100% of normal card size
};'''
    
    new_size_overrides = '''export const SIZE_OVERRIDES = {
  small: 1.8,   // 180% of normal card size (tripled from 60%)
  medium: 2.4,  // 240% of normal card size (tripled from 80%)  
  large: 3.0,   // 300% of normal card size (tripled from 100%)
};'''
    
    content = content.replace(old_size_overrides, new_size_overrides)
    
    # Update the card layout calculation to use 12 columns for main deck
    old_main_deck_calc = '''  // Calculate cards per column
  const cardsPerMainColumn = Math.ceil(mainDeckCount / 5);
  const cardsPerSideboardColumn = Math.ceil(sideboardCount / 2);'''
    
    new_main_deck_calc = '''  // Calculate cards per column
  const cardsPerMainColumn = Math.ceil(mainDeckCount / 12);
  const cardsPerSideboardColumn = Math.ceil(sideboardCount / 6);'''
    
    content = content.replace(old_main_deck_calc, new_main_deck_calc)
    
    # Update the width calculation for 12 columns
    old_width_calc = '''  // Calculate optimal card width (5 columns for main deck)
  const mainDeckGaps = 4 * cardGap; // Gaps between 5 columns
  const optimalCardWidth = (availableSpace.availableWidth - mainDeckGaps) / 5;'''
    
    new_width_calc = '''  // Calculate optimal card width (12 columns for main deck)
  const mainDeckGaps = 11 * cardGap; // Gaps between 12 columns
  const optimalCardWidth = (availableSpace.availableWidth - mainDeckGaps) / 12;'''
    
    content = content.replace(old_width_calc, new_width_calc)
    
    # Update the arrangeCardsForScreenshot function
    old_arrange = '''  // Distribute main deck across 5 columns (round-robin)
  const mainDeckColumns: DeckCardInstance[][] = [[], [], [], [], []];
  mainDeckCards.forEach((card, index) => {
    const columnIndex = index % 5;
    mainDeckColumns[columnIndex].push(card);
  });
  
  // Distribute sideboard across 2 columns (round-robin)
  const sideboardColumns: DeckCardInstance[][] = [[], []];
  sideboardCards.forEach((card, index) => {
    const columnIndex = index % 2;
    sideboardColumns[columnIndex].push(card);
  });'''
    
    new_arrange = '''  // Distribute main deck across 12 columns (round-robin)
  const mainDeckColumns: DeckCardInstance[][] = Array.from({ length: 12 }, () => []);
  mainDeckCards.forEach((card, index) => {
    const columnIndex = index % 12;
    mainDeckColumns[columnIndex].push(card);
  });
  
  // Distribute sideboard across 6 columns (round-robin)
  const sideboardColumns: DeckCardInstance[][] = Array.from({ length: 6 }, () => []);
  sideboardCards.forEach((card, index) => {
    const columnIndex = index % 6;
    sideboardColumns[columnIndex].push(card);
  });'''
    
    content = content.replace(old_arrange, new_arrange)
    
    # Write updated content
    with open(utils_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Updated {utils_path} with more columns and larger sizes")

def fix_screenshot_modal():
    """Update ScreenshotModal.tsx to use 12 columns for main deck and 6 for sideboard"""
    
    modal_path = "src/components/ScreenshotModal.tsx"
    
    if not os.path.exists(modal_path):
        print(f"❌ Error: {modal_path} not found!")
        return
    
    print(f"Reading {modal_path}...")
    with open(modal_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update main deck grid to 12 columns
    old_main_grid = '''            <div className="screenshot-deck-layout" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(5, 1fr)','''
    
    new_main_grid = '''            <div className="screenshot-deck-layout" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(12, 1fr)','''
    
    content = content.replace(old_main_grid, new_main_grid)
    
    # Update sideboard grid to 6 columns
    old_sideboard_grid = '''            <div className="screenshot-sideboard-layout" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(2, 1fr)','''
    
    new_sideboard_grid = '''            <div className="screenshot-sideboard-layout" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(6, 1fr)','''
    
    content = content.replace(old_sideboard_grid, new_sideboard_grid)
    
    # Write updated content
    with open(modal_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Updated {modal_path} with more columns")

def main():
    """Main execution function"""
    print("🔧 Applying quick fixes to screenshot layout...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: src directory not found!")
        print("Please run this script from your project root directory (mtg-deckbuilder)")
        return
    
    try:
        fix_screenshot_utils()
        fix_screenshot_modal()
        
        print("\n" + "=" * 60)
        print("✅ Quick fixes applied successfully!")
        print("\n🎯 Changes Made:")
        print("   • Main deck: 5 → 12 columns")
        print("   • Sideboard: 2 → 6 columns")
        print("   • Small size: 60% → 180% (tripled)")
        print("   • Medium size: 80% → 240% (tripled)")
        print("   • Large size: 100% → 300% (tripled)")
        print("\n🔧 Next Steps:")
        print("   1. Save any changes and refresh the browser")
        print("   2. Test screenshot modal with different deck sizes")
        print("   3. Try S/M/L controls - should be much more readable now")
        print("   4. Auto mode should fit more cards in horizontal space")
        
    except Exception as e:
        print(f"\n❌ Error during fixes: {str(e)}")
        print("Please check the error message and try again.")

if __name__ == "__main__":
    main()
