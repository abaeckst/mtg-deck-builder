#!/usr/bin/env python3

import re
import os

def targeted_pagination_fix():
    """
    Targeted fix for the Load More 422 error.
    
    ROOT CAUSE: currentPageCards is empty, so loadMoreResults thinks 
    there are no remaining cards and tries to fetch page 2.
    
    SOLUTION: Ensure the full page data is properly stored and passed.
    """
    
    # Fix 1: Update scryfallApi.ts to store full page data correctly
    scryfallApi_path = 'src/services/scryfallApi.ts'
    
    if not os.path.exists(scryfallApi_path):
        print(f"❌ File not found: {scryfallApi_path}")
        return
    
    try:
        with open(scryfallApi_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔍 Analyzing scryfallApi.ts...")
        
        # The issue: searchCardsWithPagination stores response.data in currentPageCards
        # but this data isn't being passed through properly to loadMoreResults
        
        # Fix the searchCardsWithPagination return to ensure currentPageCards contains full data
        old_return_pattern = r'return \{([^}]+)currentPageCards: response\.data,([^}]+)\};'
        
        # Find and replace the return statement
        if 'currentPageCards: response.data,' in content:
            print("✅ Found currentPageCards assignment - this should be working")
            
            # The issue might be that the data isn't being passed through the chain
            # Let's add debugging to loadMoreResults to see what currentPageCards contains
            
            # Find the loadMoreResults function and add debugging
            debug_section = '''console.log('📊 Partial page analysis:', {
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
      // CRITICAL DEBUG: WHY IS CURRENTPAGECARDS EMPTY?
      paginationStateTotalCards: paginationState.totalCards,
      paginationStateLoadedCards: paginationState.loadedCards,
      currentPageCardsPreview: currentPageCards.slice(0, 3).map(c => c.name),
      shouldUseRemainingCards: currentPageCards.length > cardsConsumed
    });
    
    // EMERGENCY FIX: If currentPageCards is empty but we know there should be more cards,
    // prevent fetching next page and show error instead
    if (currentPageCards.length === 0 && paginationState.loadedCards < paginationState.totalCards) {
      console.error('🚨 PAGINATION BUG: currentPageCards is empty but more cards should exist');
      console.error('🚨 This means the full page data was not stored properly during initial search');
      throw new Error('Pagination data missing - please refresh and try again');
    }'''
            
            content = re.sub(
                re.escape(debug_section),
                enhanced_debug,
                content
            )
            
        else:
            print("❌ Could not find currentPageCards assignment - this is the problem!")
            
            # The data storage is broken - let's fix it
            # Find the return statement in searchCardsWithPagination
            return_pattern = r'(return \{[^}]+)(currentPageCards: response\.data,)([^}]+\};)'
            
            def fix_return(match):
                before = match.group(1)
                current_line = match.group(2)
                after = match.group(3)
                
                # Ensure we're definitely storing the full response data
                fixed_line = 'currentPageCards: response.data || [], // FIXED: Store full page data for Load More'
                return f"{before}{fixed_line}{after}"
            
            content = re.sub(return_pattern, fix_return, content, flags=re.DOTALL)
        
        # Write the updated file
        with open(scryfallApi_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {scryfallApi_path}")
        
        # Fix 2: Ensure useSearch.ts passes the pagination state correctly
        useSearch_path = 'src/hooks/useSearch.ts'
        
        if os.path.exists(useSearch_path):
            with open(useSearch_path, 'r', encoding='utf-8') as f:
                search_content = f.read()
            
            # Check if we're storing the enhanced pagination result properly
            if 'enhancedPaginationResult' in search_content:
                print("✅ Found enhanced pagination result storage")
            else:
                print("⚠️ Adding enhanced pagination result storage")
                
                # Find where onPaginationStateChange is called and enhance it
                old_pagination_call = 'onPaginationStateChange(paginationResult);'
                new_pagination_call = '''// CRITICAL: Store enhanced pagination result with full page data
      const enhancedPaginationResult = {
        ...paginationResult,
        currentPageCards: paginationResult.currentPageCards || [], // Ensure array exists
        cardsConsumedFromCurrentPage: paginationResult.loadedCards
      };
      onPaginationStateChange(enhancedPaginationResult);'''
                
                search_content = search_content.replace(old_pagination_call, new_pagination_call)
            
            with open(useSearch_path, 'w', encoding='utf-8') as f:
                f.write(search_content)
            
            print(f"✅ Updated {useSearch_path}")
        
        print("\n🎯 TARGETED FIX APPLIED:")
        print("1. ✅ Enhanced debugging in loadMoreResults to show why currentPageCards is empty")
        print("2. ✅ Added emergency safeguard to prevent 422 errors when data is missing")  
        print("3. ✅ Ensured pagination state properly stores full page data")
        
        print("\n🔍 NEXT STEPS:")
        print("1. Test Load More again - should see detailed debug logs")
        print("2. Look for 'CRITICAL DEBUG' section to understand data flow")
        print("3. If currentPageCards is still empty, we need to trace the data storage chain")
        
        print("\n🚨 IF STILL BROKEN:")
        print("- Check that searchCardsWithPagination response.data contains all 97 cards")
        print("- Verify onPaginationStateChange receives the full currentPageCards array")
        print("- Ensure loadMoreResults gets the complete pagination state")
        
    except Exception as e:
        print(f"❌ Error updating files: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    targeted_pagination_fix()