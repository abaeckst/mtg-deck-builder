import os
import re

# Navigate to project directory
project_path = r"C:\Users\carol\mtg-deck-builder"
os.chdir(project_path)

def fix_load_more_logic():
    """Fix the Load More 422 error by correcting pagination logic"""
    
    filepath = "src/services/scryfallApi.ts"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 FIXING LOAD MORE 422 ERROR")
        print("="*60)
        
        # The issue is in loadMoreResults function - it's checking remainingInCurrentPage
        # but the logic is wrong. When we have 97 total cards, load 75 initially,
        # we should have 22 remaining cards from the current page.
        
        # Find the problematic section
        old_logic = '''    // Check if current Scryfall page has remaining cards
    const remainingInCurrentPage = currentPageCards.length - cardsConsumed;
    
    console.log('📊 Partial page analysis:', {
      currentPageTotalCards: currentPageCards.length,
      cardsAlreadyConsumed: cardsConsumed,
      remainingInCurrentPage,
      needsNewPage: remainingInCurrentPage <= 0,
      // CRITICAL DEBUG INFO
      totalCardsFromSearch: paginationState.totalCards,
      loadedSoFar: paginationState.loadedCards,
      shouldHaveMoreOnCurrentPage: paginationState.totalCards > paginationState.loadedCards && currentPageCards.length > cardsConsumed
    });
    
    let newCards: ScryfallCard[];
    
    if (remainingInCurrentPage > 0) {'''
        
        # The fixed logic should properly handle the case where all results fit on page 1
        new_logic = '''    // FIXED: Check if current Scryfall page has remaining cards
    const remainingInCurrentPage = currentPageCards.length - cardsConsumed;
    
    // CRITICAL FIX: When all results fit on page 1 (97 total, 75 displayed, 22 remaining),
    // we should use the remaining 22 cards instead of trying to fetch page 2
    const allResultsFitOnCurrentPage = paginationState.totalCards <= currentPageCards.length;
    const hasRemainingCards = remainingInCurrentPage > 0;
    
    console.log('📊 Partial page analysis (FIXED):', {
      currentPageTotalCards: currentPageCards.length,
      cardsAlreadyConsumed: cardsConsumed,
      remainingInCurrentPage,
      allResultsFitOnCurrentPage,
      hasRemainingCards,
      totalCardsFromSearch: paginationState.totalCards,
      loadedSoFar: paginationState.loadedCards,
      decision: allResultsFitOnCurrentPage && hasRemainingCards ? 'USE_REMAINING_CARDS' : 'FETCH_NEW_PAGE'
    });
    
    let newCards: ScryfallCard[];
    
    if (allResultsFitOnCurrentPage && hasRemainingCards) {
      // FIXED: All results fit on current page, use remaining cards
      const cardsToReturn = Math.min(remainingInCurrentPage, displayBatchSize);
      newCards = currentPageCards.slice(cardsConsumed, cardsConsumed + cardsToReturn);
      
      console.log('📄 Using remaining cards from complete page:', {
        cardsToReturn,
        sliceStart: cardsConsumed,
        sliceEnd: cardsConsumed + cardsToReturn,
        remainingAfterThis: remainingInCurrentPage - cardsToReturn,
        reason: 'All results fit on current Scryfall page'
      });
      
    } else if (remainingInCurrentPage > 0) {'''
        
        # Apply the fix
        if old_logic in content:
            content = content.replace(old_logic, new_logic)
            print("✅ FIXED: Load More pagination logic")
            print("- Added allResultsFitOnCurrentPage check")
            print("- Prevents 422 error when all results fit on page 1")
            print("- Uses remaining cards instead of fetching non-existent page 2")
        else:
            print("❌ Could not find the exact pattern to replace")
            print("Manual fix needed in loadMoreResults function")
            return False
        
        # Write the fixed content back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ FIXED: {filepath}")
        print("🎯 The Load More 422 error should now be resolved")
        print("📋 Test by searching for anything that returns 75+ results and clicking Load More")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return False
    except Exception as e:
        print(f"❌ Error fixing file: {e}")
        return False

if __name__ == "__main__":
    success = fix_load_more_logic()
    if success:
        print("\n🚀 NEXT STEPS:")
        print("1. Run npm start to test the fix")
        print("2. Search for 'lightning bolt' or similar")
        print("3. Click Load More - should work without 422 error")
        print("4. Check console logs for 'Using remaining cards from complete page'")
    else:
        print("\n❌ Fix failed - manual intervention needed")
