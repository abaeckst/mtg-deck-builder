#!/usr/bin/env python3

import os
import sys

def debug_load_more_visibility():
    """Add comprehensive debugging to understand why Load More button isn't showing"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the Load More section and add debugging
    old_load_more = """          {/* Load More Results Section */}
          {!loading && !error && pagination.hasMore && (
            <div className="load-more-section">"""
    
    new_load_more = """          {/* Load More Results Section - DEBUGGING */}
          {(() => {
            console.log('🔍 Load More Debug:', {
              loading,
              error,
              'pagination.hasMore': pagination.hasMore,
              'pagination.totalCards': pagination.totalCards,
              'pagination.loadedCards': pagination.loadedCards,
              'cards.length': cards.length,
              'shouldShow': !loading && !error && pagination.hasMore
            });
            return null;
          })()}
          {!loading && !error && pagination.hasMore && (
            <div className="load-more-section">"""
    
    if old_load_more in content:
        content = content.replace(old_load_more, new_load_more)
        print("✅ Added Load More visibility debugging")
    else:
        print("❌ Could not find Load More section pattern")
        return False
    
    # Also add debugging to the pagination debug section
    old_pagination_debug = """            {/* Safe pagination debug - check browser console */}
            {(() => {
              console.log('🔍 Pagination Debug:', {
                hasMore: pagination.hasMore,
                totalCards: pagination.totalCards,
                loadedCards: pagination.loadedCards,
                isLoadingMore: pagination.isLoadingMore,
                cardsDisplayed: cards.length
              });
              return null;
            })()}"""
    
    new_pagination_debug = """            {/* Enhanced pagination debug - check browser console */}
            {(() => {
              const debugInfo = {
                hasMore: pagination.hasMore,
                totalCards: pagination.totalCards,
                loadedCards: pagination.loadedCards,
                isLoadingMore: pagination.isLoadingMore,
                cardsDisplayed: cards.length,
                loading,
                error,
                'LOAD_MORE_SHOULD_SHOW': !loading && !error && pagination.hasMore
              };
              console.log('🔍 ENHANCED Pagination Debug:', debugInfo);
              if (!pagination.hasMore && pagination.totalCards > pagination.loadedCards) {
                console.log('🚨 BUG: hasMore is false but totalCards > loadedCards!');
              }
              return null;
            })()}"""
    
    if old_pagination_debug in content:
        content = content.replace(old_pagination_debug, new_pagination_debug)
        print("✅ Enhanced pagination debugging")
    else:
        print("⚠️ Could not find pagination debug section")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully added Load More debugging to {filename}")
    return True

if __name__ == "__main__":
    success = debug_load_more_visibility()
    sys.exit(0 if success else 1)