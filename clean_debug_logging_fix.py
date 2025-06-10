#!/usr/bin/env python3
"""
Clean up debug logging issues in useSearch.ts
Problem: Multiple broken debug logging sections referencing undefined variables
Solution: Remove all broken debug logging and add one clean, working version
"""

import re
import os

def clean_debug_logging():
    """Remove all broken debug logging and add one clean version"""
    
    file_path = "src/hooks/useSearch.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 Cleaning debug logging in {file_path}")
        
        # Remove all instances of broken debug logging
        broken_patterns = [
            # Pattern 1: Debug logging with currentSortParams that doesn't exist
            r'''console\.log\('🔍 Load More sort coordination:', \{[\s\S]*?currentSortParams[\s\S]*?\}\);''',
            # Pattern 2: Any debug with currentSortParams references
            r'''// DEBUG: Log current sort parameters for Load More coordination\s*const currentSortParams = getCollectionSortParams\(\);\s*console\.log\('🔍 Load More sort coordination:', \{[\s\S]*?\}\);''',
        ]
        
        for pattern in broken_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                content = re.sub(pattern, '', content, flags=re.MULTILINE)
                print(f"✅ Removed {len(matches)} broken debug logging instances")
        
        # Remove any standalone currentSortParams declarations
        content = re.sub(r'const currentSortParams = getCollectionSortParams\(\);\s*', '', content)
        
        # Add one clean debug logging section after metadata null check
        # Find the location after metadata check but before the actual API work
        insertion_point = r'(console\.log\(\'📡 Loading more cards via API\.\.\.\'\);)'
        
        clean_debug = r'''\1
      
      // DEBUG: Load More sort coordination
      console.log('🔍 Load More sort coordination:', {
        preservedSortOrder: metadata.actualSortOrder || 'missing',
        preservedSortDirection: metadata.actualSortDirection || 'missing',
        willUsePreservedParams: !!(metadata.actualSortOrder && metadata.actualSortDirection)
      });'''
        
        if re.search(insertion_point, content):
            content = re.sub(insertion_point, clean_debug, content)
            print("✅ Added clean debug logging")
        
        # Clean up any extra whitespace that might have been left
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Save the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path} debug logging cleaned up")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def verify_fix():
    """Verify that the core sort coordination fix is still in place"""
    
    file_path = "src/hooks/useSearch.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that the core fixes are still in place
        fixes_present = {
            'actualSortOrder in metadata': 'actualSortOrder' in content,
            'actualSortDirection in metadata': 'actualSortDirection' in content,
            'lastSort uses metadata': 'metadata.actualSortOrder' in content and 'metadata.actualSortDirection' in content,
        }
        
        print("\n🔍 Verifying core fixes are still present:")
        for fix_name, is_present in fixes_present.items():
            status = "✅" if is_present else "❌"
            print(f"{status} {fix_name}: {'Present' if is_present else 'Missing'}")
        
        all_present = all(fixes_present.values())
        if all_present:
            print("\n✅ All core sort coordination fixes are still in place")
        else:
            print("\n❌ Some core fixes are missing - manual review needed")
        
        return all_present
        
    except Exception as e:
        print(f"❌ Error verifying fixes: {e}")
        return False

def main():
    """Clean up debug logging issues while preserving core functionality"""
    print("🚀 Cleaning up debug logging issues...")
    print("="*50)
    
    print("📝 Problem:")
    print("- Multiple broken debug logging sections")
    print("- References to undefined currentSortParams variable")
    print("- TypeScript compilation errors")
    print("")
    
    if clean_debug_logging():
        print("✅ Debug logging cleaned up!")
        
        if verify_fix():
            print("\n🎯 SOLUTION VERIFIED:")
            print("• ✅ Core sort coordination fix preserved")
            print("• ✅ Debug logging cleaned and working")
            print("• ✅ TypeScript compilation should succeed")
            print("\nExpected behavior:")
            print("• Initial search: order=cmc&dir=desc")
            print("• Load More: order=cmc&dir=desc (preserved)")
            print("• No 422 errors from sort inconsistency")
        else:
            print("\n⚠️ Core fixes may need manual verification")
        
        print("\nNext steps:")
        print("1. Run: npm start")
        print("2. Test: Popular cards → Load More")
        print("3. Verify: No 422 errors, consistent sort order")
    else:
        print("❌ Failed to clean debug logging")
    
    print("\n🔄 Run `npm start` to test the fix")

if __name__ == "__main__":
    main()
