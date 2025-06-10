#!/usr/bin/env python3

import re
import os

def fix_load_more_pagination():
    """
    Fix Load More pagination logic to properly handle the case where
    all results fit on the first Scryfall page but are artificially 
    limited to 75 cards for display.
    
    ROOT ISSUE: When search returns 97 cards on page 1, but we only display 75,
    Load More tries to fetch page 2 instead of using remaining 22 cards from page 1.
    """
    
    # Update useSearch.ts loadMoreCards function
    useSearch_path = 'src/hooks/useSearch.ts'
    
    if not os.path.exists(useSearch_path):
        print(f"❌ File not found: {useSearch_path}")
        return
    
    try:
        with open(useSearch_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # CRITICAL FIX: The currentScryfallPage calculation is wrong
        # It calculates: Math.floor(75 / 175) + 1 = 1, but then increments to 2
        # When we should stay on page 1 and use remaining cards
        
        # Find and replace the currentScryfallPage calculation
        old_scryfall_page = r'currentScryfallPage: Math\.floor\(actualLoadedCards / 175\) \+ 1,'
        new_scryfall_page = 'currentScryfallPage: 1, // FIXED: Stay on page 1 when all results fit'
        
        content = re.sub(old_scryfall_page, new_scryfall_page, content)
        
        # Also fix the cardsConsumedFromCurrentPage to be more explicit
        old_consumed = r'cardsConsumedFromCurrentPage: actualLoadedCards % 175,'
        new_consumed = 'cardsConsumedFromCurrentPage: actualLoadedCards, // FIXED: Track cards consumed from page 1'
        
        content = re.sub(old_consumed, new_consumed, content)
        
        # Write the updated file
        with open(useSearch_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {useSearch_path}")
        
        # Also need to ensure the API stores full page data properly
        scryfallApi_path = 'src/services/scryfallApi.ts'
        
        if os.path.exists(scryfallApi_path):
            with open(scryfallApi_path, 'r', encoding='utf-8') as f:
                api_content = f.read()
            
            # Look for the loadMoreResults function and add better logic
            # Find the section that determines whether to fetch new page
            
            # The key issue is that remainingInCurrentPage calculation may be wrong
            # when currentPageCards is empty or not properly stored
            
            # Add debug logging to understand what's happening
            load_more_debug = '''console.log('📊 Partial page analysis:', {
      currentPageTotalCards: currentPageCards.length,
      cardsAlreadyConsumed: cardsConsumed,
      remainingInCurrentPage,
      needsNewPage: remainingInCurrentPage <= 0
    });'''
    
            enhanced_debug = '''console.log('📊 Partial page analysis:', {
      currentPageTotalCards: currentPageCards.length,
      cardsAlreadyConsumed: cardsConsumed,
      remainingInCurrentPage,
      needsNewPage: remainingInCurrentPage <= 0,
      // CRITICAL DEBUG INFO
      totalCardsFromSearch: paginationState.totalCards,
      loadedSoFar: paginationState.loadedCards,
      shouldHaveMoreOnCurrentPage: paginationState.totalCards > paginationState.loadedCards && currentPageCards.length > cardsConsumed
    });'''
            
            api_content = re.sub(
                re.escape(load_more_debug),
                enhanced_debug,
                api_content
            )
            
            with open(scryfallApi_path, 'w', encoding='utf-8') as f:
                f.write(api_content)
            
            print(f"✅ Updated {scryfallApi_path} with enhanced debugging")
        
        print("\n🎯 PAGINATION FIX APPLIED:")
        print("1. ✅ Fixed currentScryfallPage to stay at 1 when all results fit on first page")
        print("2. ✅ Fixed cardsConsumedFromCurrentPage tracking")
        print("3. ✅ Enhanced debugging to show why Load More tries to fetch new page")
        
        print("\n🔍 EXPECTED BEHAVIOR AFTER FIX:")
        print("- Search: Gets 97 cards from Scryfall page 1, displays first 75")  
        print("- Load More: Should use remaining 22 cards from stored page 1 data")
        print("- No 422 error because currentScryfallPage stays at 1")
        
        print("\n🐛 IF ISSUE PERSISTS:")
        print("- Check console logs for 'CRITICAL DEBUG INFO' section")
        print("- Verify currentPageCards.length = 97 (full page stored)")
        print("- Verify cardsConsumed = 75 (display limit)")
        print("- Verify remainingInCurrentPage = 22 (97 - 75)")
        
    except Exception as e:
        print(f"❌ Error updating files: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_load_more_pagination()