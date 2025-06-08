#!/usr/bin/env python3

import os
import sys

def verify_search_flow():
    """Verify the search flow and identify where the disconnect is happening"""
    
    files_to_check = [
        "src/hooks/useCards.ts",
        "src/services/scryfallApi.ts",
        "src/components/MTGOLayout.tsx"
    ]
    
    print("🔍 SEARCH FLOW ANALYSIS")
    print("=" * 60)
    
    for filename in files_to_check:
        if not os.path.exists(filename):
            print(f"❌ Missing: {filename}")
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n📄 {filename}:")
        
        if filename.endswith("useCards.ts"):
            # Check for pagination integration
            if "searchCardsWithPagination" in content:
                print("  ✅ Has searchCardsWithPagination function")
            else:
                print("  ❌ Missing searchCardsWithPagination function")
            
            if "getScryfallSortParams" in content:
                print("  ✅ Has getScryfallSortParams integration")
            else:
                print("  ❌ Missing getScryfallSortParams integration")
            
            if "handleCollectionSortChange" in content:
                print("  ✅ Has handleCollectionSortChange function")
            else:
                print("  ❌ Missing handleCollectionSortChange function")
                
            # Check if load more is connected
            if "loadMoreResultsAction" in content:
                print("  ✅ Has loadMoreResultsAction function")
            else:
                print("  ❌ Missing loadMoreResultsAction function")
        
        elif filename.endswith("scryfallApi.ts"):
            # Check API functions
            if "searchCardsWithPagination" in content:
                print("  ✅ Has searchCardsWithPagination API function")
            else:
                print("  ❌ Missing searchCardsWithPagination API function")
            
            if "enhancedSearchCards" in content:
                print("  ✅ Has enhancedSearchCards function")
            else:
                print("  ❌ Missing enhancedSearchCards function")
            
            if "loadMoreResults" in content:
                print("  ✅ Has loadMoreResults function")
            else:
                print("  ❌ Missing loadMoreResults function")
        
        elif filename.endswith("MTGOLayout.tsx"):
            # Check UI integration
            if "load-more-results-btn" in content:
                print("  ✅ Has Load More Results button")
            else:
                print("  ❌ Missing Load More Results button")
            
            if "loadMoreResultsAction" in content:
                print("  ✅ Has loadMoreResultsAction call")
            else:
                print("  ❌ Missing loadMoreResultsAction call")
            
            if "pagination.hasMore" in content:
                print("  ✅ Has pagination.hasMore logic")
            else:
                print("  ❌ Missing pagination.hasMore logic")
    
    print("\n🔍 LOOKING FOR SPECIFIC ISSUES:")
    
    # Check if Load More section is conditionally rendered
    with open("src/components/MTGOLayout.tsx", 'r', encoding='utf-8') as f:
        mtgo_content = f.read()
    
    if "{!loading && !error && pagination.hasMore &&" in mtgo_content:
        print("  ✅ Load More section has correct conditional rendering")
    else:
        print("  ❌ Load More section conditional rendering may be broken")
    
    # Check if the section is properly closed
    load_more_start = mtgo_content.find("Load More Results Section")
    if load_more_start > -1:
        # Look for the closing div
        after_load_more = mtgo_content[load_more_start:load_more_start + 2000]
        if "</div>" in after_load_more and "Enhanced Resize Handle" in after_load_more:
            print("  ✅ Load More section is properly structured")
        else:
            print("  ❌ Load More section may not be properly closed")
    else:
        print("  ❌ Load More Results Section comment not found")
    
    print("\n✅ Analysis complete - check results above")
    return True

if __name__ == "__main__":
    verify_search_flow()
    sys.exit(0)