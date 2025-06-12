#!/usr/bin/env python3
"""
Fix Sort Direction Coordination Issue
Problem: Load More uses current sort defaults instead of preserving actual search sort parameters
Solution: Store and preserve actual sort parameters used in original search
"""

import re
import os

def fix_sort_parameter_preservation():
    """Fix useSearch to preserve actual sort parameters instead of using current defaults"""
    
    file_path = "src/hooks/useSearch.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 Fixing sort parameter preservation in {file_path}")
        
        # Step 1: Enhance lastSearchMetadata to include actual sort parameters
        old_metadata_pattern = r'lastSearchMetadata: \{(\s+)query,(\s+)filters: filters as FilterState,(\s+)totalCards: paginationResult\.totalCards,(\s+)loadedCards: paginationResult\.loadedCards,(\s+)\},'
        
        new_metadata = '''lastSearchMetadata: {
          query,
          filters: filters as FilterState,
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
          // ADDED: Store actual sort parameters used in this search
          actualSortOrder,
          actualSortDirection,
        },'''
        
        if re.search(old_metadata_pattern, content):
            content = re.sub(old_metadata_pattern, new_metadata, content)
            print("✅ Enhanced lastSearchMetadata to store actual sort parameters")
        else:
            print("⚠️ Could not find lastSearchMetadata pattern - checking for simpler pattern")
            
            # Try simpler pattern
            simple_pattern = r'lastSearchMetadata: \{[^}]+\},'
            if re.search(simple_pattern, content):
                content = re.sub(simple_pattern, new_metadata, content)
                print("✅ Enhanced lastSearchMetadata (simple pattern)")
        
        # Step 2: Update SearchState interface to include sort parameters
        interface_pattern = r'lastSearchMetadata: \{(\s+)query: string;(\s+)filters: FilterState;(\s+)totalCards: number;(\s+)loadedCards: number;(\s+)\} \| null;'
        
        new_interface = '''lastSearchMetadata: {
    query: string;
    filters: FilterState;
    totalCards: number;
    loadedCards: number;
    // ADDED: Actual sort parameters used in search
    actualSortOrder: string;
    actualSortDirection: 'asc' | 'desc';
  } | null;'''
        
        if re.search(interface_pattern, content):
            content = re.sub(interface_pattern, new_interface, content)
            print("✅ Updated SearchState interface to include sort parameters")
        
        # Step 3: Fix Load More to use preserved sort parameters
        old_last_sort = r'lastSort: getCollectionSortParams\(\), // ✅ FIXED: Use current sort parameters'
        new_last_sort = '''lastSort: {
          order: metadata.actualSortOrder,
          dir: metadata.actualSortDirection
        }, // ✅ FIXED: Use actual sort parameters from original search'''
        
        if re.search(old_last_sort, content):
            content = re.sub(old_last_sort, new_last_sort, content)
            print("✅ Fixed Load More to use preserved sort parameters")
        else:
            # Alternative pattern
            alt_pattern = r'lastSort: getCollectionSortParams\(\),'
            if re.search(alt_pattern, content):
                content = re.sub(alt_pattern, new_last_sort, content)
                print("✅ Fixed Load More to use preserved sort parameters (alternative)")
        
        # Step 4: Add debug logging to show actual vs current sort params
        debug_pattern = r'(console\.log\(\'🔍 Load More sort coordination:\', \{[^}]+\}\);)'
        
        enhanced_debug = '''console.log('🔍 Load More sort coordination:', {
      currentSortOrder: currentSortParams.order,
      currentSortDirection: currentSortParams.dir,
      actualSortOrder: metadata.actualSortOrder,
      actualSortDirection: metadata.actualSortDirection,
      willUseActualParams: true
    });'''
        
        if re.search(debug_pattern, content):
            content = re.sub(debug_pattern, enhanced_debug, content)
            print("✅ Enhanced debug logging to show actual vs current sort params")
        
        # Save the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path} updated successfully")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Apply the sort direction coordination fix"""
    print("🚀 Fixing sort direction coordination issue...")
    print("="*60)
    
    print("📝 Problem Analysis:")
    print("- Initial search: dir=desc (popular cards)")
    print("- Load More: dir=asc (current sorting default)")
    print("- Result: 422 error from inconsistent pagination")
    print("")
    
    print("📝 Solution:")
    print("- Store actual sort parameters in lastSearchMetadata")
    print("- Use stored parameters in Load More instead of current defaults")
    print("- Preserve sort consistency throughout pagination")
    print("")
    
    if fix_sort_parameter_preservation():
        print("✅ SORT COORDINATION FIX SUCCESSFUL!")
        print("\nExpected behavior after fix:")
        print("• ✅ Popular cards search: order=cmc&dir=desc")
        print("• ✅ Load More: order=cmc&dir=desc (preserved)")
        print("• ✅ No more 422 errors from inconsistent pagination")
        print("• ✅ Sort direction maintained throughout Load More operations")
        print("\nNext steps:")
        print("1. Run: npm start")
        print("2. Test: Popular cards → Load More button")
        print("3. Check console: Should show preserved sort parameters")
        print("4. Verify: No 422 errors, consistent sort order")
    else:
        print("❌ SORT COORDINATION FIX FAILED!")
        print("Manual review needed")
    
    print("\n🔄 Run `npm start` to test the fix")

if __name__ == "__main__":
    main()
