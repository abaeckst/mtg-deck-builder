#!/usr/bin/env python3

import os
import sys

def diagnose_load_more():
    """Diagnose why Load More button isn't appearing"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 LOAD MORE BUTTON DIAGNOSTIC")
    print("=" * 50)
    
    # Check 1: Is the Load More section in the collection area?
    if 'Load More Results Section' in content and 'mtgo-collection-area' in content:
        lines = content.split('\n')
        collection_area_line = -1
        load_more_line = -1
        
        for i, line in enumerate(lines):
            if 'Load More Results Section' in line:
                load_more_line = i
            if 'mtgo-collection-area' in line and collection_area_line == -1:
                collection_area_line = i
        
        if load_more_line > collection_area_line and load_more_line != -1:
            print("✅ Load More section found in collection area")
        else:
            print("❌ Load More section NOT in collection area")
            print(f"   Collection area line: {collection_area_line}")
            print(f"   Load More line: {load_more_line}")
    else:
        print("❌ Load More section not found or collection area missing")
    
    # Check 2: Look for the exact button condition
    if 'pagination.hasMore' in content:
        print("✅ pagination.hasMore condition found")
        
        # Find the exact condition
        hasmore_index = content.find('pagination.hasMore')
        if hasmore_index != -1:
            # Get surrounding context
            start = max(0, hasmore_index - 100)
            end = min(len(content), hasmore_index + 200)
            context = content[start:end]
            print("📋 Button condition context:")
            print("   " + context.replace('\n', '\n   '))
    else:
        print("❌ pagination.hasMore condition NOT found")
    
    # Check 3: Look for loadMoreResultsAction
    if 'loadMoreResultsAction' in content:
        print("✅ loadMoreResultsAction found")
    else:
        print("❌ loadMoreResultsAction NOT found")
    
    # Check 4: Show current pagination destructuring
    if 'pagination,' in content:
        # Find the destructuring line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'pagination,' in line and 'useCards' in line:
                print("✅ Pagination destructured from useCards:")
                print(f"   Line {i+1}: {line.strip()}")
                break
    else:
        print("❌ Pagination not properly destructured")
    
    print("\n🔧 RECOMMENDATIONS:")
    print("1. Check browser console for pagination state")
    print("2. Add debug logging to see pagination values")
    print("3. Verify search is using paginated search function")
    
    return True

def add_debug_logging():
    """Add debug logging to help diagnose pagination state"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add debug logging right after the collection header
    old_header = '''          <div className="panel-header">
            <h3>Collection ({cards.length.toLocaleString()} {pagination.totalCards > pagination.loadedCards && (<span className="pagination-info">of {pagination.totalCards.toLocaleString()}</span>)} cards)</h3>'''
    
    new_header = '''          <div className="panel-header">
            <h3>Collection ({cards.length.toLocaleString()} {pagination.totalCards > pagination.loadedCards && (<span className="pagination-info">of {pagination.totalCards.toLocaleString()}</span>)} cards)</h3>
            {/* DEBUG: Pagination state logging */}
            {console.log('🔍 PAGINATION DEBUG:', {
              hasMore: pagination.hasMore,
              totalCards: pagination.totalCards,
              loadedCards: pagination.loadedCards,
              isLoadingMore: pagination.isLoadingMore,
              currentPage: pagination.currentPage,
              loading: loading,
              error: error
            })}'''
    
    if old_header in content:
        content = content.replace(old_header, new_header)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Added debug logging to MTGOLayout.tsx")
        print("✅ Check browser console for pagination state details")
        return True
    else:
        print("❌ Could not find header section to add debug logging")
        return False

if __name__ == "__main__":
    print("Running Load More diagnostics...\n")
    diagnose_load_more()
    print("\n" + "=" * 50)
    print("Adding debug logging...\n")
    add_debug_logging()
    print("\n✅ Diagnostic complete!")
    print("📋 Next steps:")
    print("1. Run npm start")
    print("2. Open browser console")
    print("3. Look for '🔍 PAGINATION DEBUG:' messages")
    print("4. Check if hasMore is true but button still not showing")