#!/usr/bin/env python3
"""
Fix TypeScript errors in useSearch.ts
Problem: Debug logging is referencing metadata before it's declared
Solution: Move debug logging to after metadata declaration
"""

import re
import os

def fix_typescript_errors():
    """Fix the TypeScript errors by moving debug logging to correct location"""
    
    file_path = "src/hooks/useSearch.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 Fixing TypeScript errors in {file_path}")
        
        # Remove the misplaced debug logging
        misplaced_debug = r'''console\.log\('🔍 Load More sort coordination:', \{
      currentSortOrder: currentSortParams\.order,
      currentSortDirection: currentSortParams\.dir,
      actualSortOrder: metadata\.actualSortOrder,
      actualSortDirection: metadata\.actualSortDirection,
      willUseActualParams: true
    \}\);'''
        
        if re.search(misplaced_debug, content, re.MULTILINE):
            content = re.sub(misplaced_debug, '', content)
            print("✅ Removed misplaced debug logging")
        
        # Find the correct location (after metadata declaration) and add proper debug logging
        correct_location_pattern = r'(const metadata = state\.lastSearchMetadata;\s+if \(!metadata\) \{[^}]+\}\s+)'
        
        correct_debug = r'''\1
    // DEBUG: Log current sort parameters for Load More coordination
    const currentSortParams = getCollectionSortParams();
    console.log('🔍 Load More sort coordination:', {
      currentSortOrder: currentSortParams.order,
      currentSortDirection: currentSortParams.dir,
      actualSortOrder: metadata.actualSortOrder,
      actualSortDirection: metadata.actualSortDirection,
      willUseActualParams: true
    });
'''
        
        if re.search(correct_location_pattern, content, re.MULTILINE | re.DOTALL):
            content = re.sub(correct_location_pattern, correct_debug, content, flags=re.MULTILINE | re.DOTALL)
            print("✅ Added debug logging in correct location")
        else:
            # Fallback: just remove all problematic debug code for now
            print("⚠️ Could not find correct location, removing problematic debug code")
            # Remove any remaining references to metadata in debug logging before declaration
            content = re.sub(r'.*metadata\.actual.*\n', '', content)
        
        # Also remove duplicate currentSortParams declaration if it exists
        duplicate_pattern = r'// DEBUG: Log current sort parameters for Load More coordination\s+const currentSortParams = getCollectionSortParams\(\);\s+'
        content = re.sub(duplicate_pattern, '', content)
        
        # Save the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path} TypeScript errors fixed")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def add_minimal_debug_logging():
    """Add simple debug logging that doesn't reference metadata before declaration"""
    
    file_path = "src/hooks/useSearch.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add simple debug after metadata is confirmed to exist
        pattern = r'(console\.log\(\'📡 Loading more cards via API\.\.\.\'\);)'
        
        replacement = r'''\1
      
      // DEBUG: Log sort coordination (after metadata check)
      console.log('🔍 Load More will use preserved sort params:', {
        actualSortOrder: metadata.actualSortOrder || 'not-stored',
        actualSortDirection: metadata.actualSortDirection || 'not-stored'
      });'''
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            print("✅ Added safe debug logging after metadata check")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding debug logging: {e}")
        return False

def main():
    """Fix TypeScript compilation errors"""
    print("🚀 Fixing TypeScript compilation errors...")
    print("="*50)
    
    if fix_typescript_errors():
        print("✅ TypeScript errors fixed!")
        
        if add_minimal_debug_logging():
            print("✅ Added safe debug logging")
        
        print("\nNext steps:")
        print("1. Run: npm start")
        print("2. Check: Compilation should succeed")
        print("3. Test: Load More should work without 422 errors")
    else:
        print("❌ Failed to fix TypeScript errors")
    
    print("\n🔄 Run `npm start` to verify the fix")

if __name__ == "__main__":
    main()
