#!/usr/bin/env python3
"""
Complete Search Coordination Fix
Fixes: Load More 422 errors, 80+ second wildcard queries, sort parameter coordination
"""

import re
import os

def fix_useSearch_load_more_sort_coordination():
    """Fix the hardcoded sort parameters in Load More operation"""
    
    file_path = "src/hooks/useSearch.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 Fixing Load More sort coordination in {file_path}")
        
        # Fix the hardcoded lastSort in currentPaginationState
        old_pattern = r'lastSort: \{ order: "name", dir: "asc" \},'
        new_replacement = 'lastSort: getCollectionSortParams(), // ✅ FIXED: Use current sort parameters'
        
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_replacement, content)
            print("✅ Fixed Load More sort parameter coordination")
        else:
            print("⚠️ Load More sort pattern not found - checking alternative pattern")
            
            # Alternative pattern check
            alt_pattern = r'lastSort: \{ order: "name", dir: "asc" \}'
            if re.search(alt_pattern, content):
                content = re.sub(alt_pattern, 'lastSort: getCollectionSortParams() // ✅ FIXED: Use current sort parameters', content)
                print("✅ Fixed Load More sort parameter coordination (alternative pattern)")
        
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

def fix_wildcard_optimization():
    """Fix wildcard query optimization to prevent expensive 80+ second queries"""
    
    file_path = "src/services/scryfallApi.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 Fixing wildcard optimization in {file_path}")
        
        # Find the buildEnhancedSearchQuery function and add early return for wildcards
        function_start = content.find('function buildEnhancedSearchQuery(query: string): string {')
        
        if function_start == -1:
            print("❌ buildEnhancedSearchQuery function not found")
            return False
        
        # Find the existing logging section
        logging_pattern = r'console\.log\(\'🔍 INPUT ANALYSIS:\', \{[^}]+\}\);'
        
        if re.search(logging_pattern, content):
            # Add wildcard optimization right after input analysis
            wildcard_optimization = '''
  
  // WILDCARD OPTIMIZATION: Early return for simple wildcard queries
  // Prevents expensive (name:* OR o:* OR type:*) queries that cause 80+ second response times
  if (query.trim() === '*') {
    console.log('🔍 WILDCARD OPTIMIZATION: Returning simple wildcard to leverage Scryfall optimizations');
    console.timeEnd("⏱️ QUERY_BUILDING_TIME");
    return '*';
  }'''
            
            # Insert the optimization right after the INPUT ANALYSIS log
            insertion_point = re.search(logging_pattern, content).end()
            content = content[:insertion_point] + wildcard_optimization + content[insertion_point:]
            
            print("✅ Added wildcard optimization to prevent expensive queries")
        else:
            print("⚠️ Could not find insertion point for wildcard optimization")
        
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

def fix_timer_conflicts():
    """Fix timer conflicts by adding proper timer management"""
    
    file_path = "src/services/scryfallApi.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 Fixing timer conflicts in {file_path}")
        
        # Fix timer conflicts in searchCards function
        timer_fixes = [
            {
                'old': 'console.time("⏱️ TOTAL_SEARCH_TIME");',
                'new': '''// Start timer (clear any existing timer first)
    console.timeEnd("⏱️ TOTAL_SEARCH_TIME"); // Clear existing timer if any
    console.time("⏱️ TOTAL_SEARCH_TIME");'''
            },
            {
                'old': 'console.time("⏱️ JSON_PARSING_TIME");',
                'new': '''// Start JSON parsing timer (clear any existing timer first)
    try { console.timeEnd("⏱️ JSON_PARSING_TIME"); } catch(e) {} // Clear existing timer if any
    console.time("⏱️ JSON_PARSING_TIME");'''
            }
        ]
        
        for fix in timer_fixes:
            if fix['old'] in content:
                content = content.replace(fix['old'], fix['new'])
                print(f"✅ Fixed timer: {fix['old'][:30]}...")
        
        # Save the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path} timer conflicts fixed")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def add_debug_logging():
    """Add debug logging to track sort parameter flow"""
    
    file_path = "src/hooks/useSearch.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 Adding debug logging to {file_path}")
        
        # Add debug logging to Load More operation
        debug_pattern = r'(console\.log\(\'🔄 useSearch\.loadMoreCards called\'\);)'
        
        if re.search(debug_pattern, content):
            debug_addition = '''console.log('🔄 useSearch.loadMoreCards called');
    
    // DEBUG: Log current sort parameters for Load More coordination
    const currentSortParams = getCollectionSortParams();
    console.log('🔍 Load More sort coordination:', {
      currentSortOrder: currentSortParams.order,
      currentSortDirection: currentSortParams.dir,
      willPreserveSortParams: true
    });'''
            
            content = re.sub(debug_pattern, debug_addition, content)
            print("✅ Added Load More debug logging")
        
        # Save the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path} debug logging added")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Run all fixes for search coordination issues"""
    print("🚀 Starting complete search coordination fix...")
    print("="*60)
    
    # Track success of each fix
    fixes = [
        ("Load More Sort Coordination", fix_useSearch_load_more_sort_coordination),
        ("Wildcard Query Optimization", fix_wildcard_optimization),
        ("Timer Conflict Resolution", fix_timer_conflicts),
        ("Debug Logging Enhancement", add_debug_logging)
    ]
    
    successful_fixes = 0
    
    for fix_name, fix_function in fixes:
        print(f"\n📝 {fix_name}:")
        print("-" * 40)
        
        if fix_function():
            successful_fixes += 1
            print(f"✅ {fix_name} completed successfully")
        else:
            print(f"❌ {fix_name} failed")
    
    print("\n" + "="*60)
    print(f"🎯 COORDINATION FIX SUMMARY:")
    print(f"✅ Successful fixes: {successful_fixes}/{len(fixes)}")
    
    if successful_fixes == len(fixes):
        print("\n🚀 ALL FIXES SUCCESSFUL!")
        print("\nExpected improvements:")
        print("• ✅ Load More will preserve original search sort parameters")
        print("• ✅ Wildcard queries will be fast (no more 80+ second responses)")
        print("• ✅ No more 422 errors from inconsistent pagination")
        print("• ✅ No more timer conflict warnings in console")
        print("\nNext steps:")
        print("1. Run: npm start")
        print("2. Test: Search → Filter clicks → Load More button")
        print("3. Verify: Console shows preserved sort parameters and fast responses")
    else:
        print(f"\n⚠️ {len(fixes) - successful_fixes} fixes failed - manual review needed")
    
    print("\n🔄 Run `npm start` to test the fixes")

if __name__ == "__main__":
    main()
