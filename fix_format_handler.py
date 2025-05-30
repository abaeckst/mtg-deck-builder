#!/usr/bin/env python3
"""
Fix format change handler in MTGOLayout.tsx
Issue: Format dropdown doesn't trigger search when search box is empty
Solution: Always trigger search when format changes, regardless of search text
"""

def fix_format_handler():
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading {file_path}")
        print(f"📏 File size: {len(content)} characters")
        
        # Find and replace the handleFormatChange function
        old_format_handler = '''  // Handle format changes by re-searching with current text
  const handleFormatChange = useCallback((newFormat: string) => {
    setSelectedFormat(newFormat);
    if (searchText.trim()) {
      setTimeout(() => {
        searchForCards(searchText, newFormat);
      }, 50);
    }
  }, [searchText, searchForCards]);'''
        
        new_format_handler = '''  // Handle format changes by re-searching with current text
  const handleFormatChange = useCallback((newFormat: string) => {
    setSelectedFormat(newFormat);
    // Always trigger search when format changes, even with empty search text
    setTimeout(() => {
      searchForCards(searchText, newFormat);
    }, 50);
  }, [searchText, searchForCards]);'''
        
        if old_format_handler in content:
            content = content.replace(old_format_handler, new_format_handler)
            print("✅ Fix 1: Updated handleFormatChange to always trigger search")
        else:
            print("❌ Fix 1: Could not find handleFormatChange function")
            
            # Try alternative pattern in case the comment or spacing is different
            alt_pattern = '''  const handleFormatChange = useCallback((newFormat: string) => {
    setSelectedFormat(newFormat);
    if (searchText.trim()) {
      setTimeout(() => {
        searchForCards(searchText, newFormat);
      }, 50);
    }
  }, [searchText, searchForCards]);'''
            
            alt_replacement = '''  const handleFormatChange = useCallback((newFormat: string) => {
    setSelectedFormat(newFormat);
    // Always trigger search when format changes, even with empty search text
    setTimeout(() => {
      searchForCards(searchText, newFormat);
    }, 50);
  }, [searchText, searchForCards]);'''
            
            if alt_pattern in content:
                content = content.replace(alt_pattern, alt_replacement)
                print("✅ Fix 1 (alt): Updated handleFormatChange to always trigger search")
            else:
                print("❌ Could not find format handler - may need manual update")
                return False
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Successfully updated {file_path}")
        print("🎯 Changes made:")
        print("   - Format dropdown now triggers search even with empty search box")
        print("   - Selecting 'Standard' with empty search will show all Standard cards")
        print("   - Works with the format-only search logic we added to useCards.ts")
        print("   - Maintains existing behavior for text + format combinations")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        return False
    except Exception as e:
        print(f"❌ Error updating file: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing format change handler...")
    success = fix_format_handler()
    
    if success:
        print("\n✅ FORMAT HANDLER FIX COMPLETE!")
        print("🧪 Test the fix:")
        print("   1. Run: npm start")
        print("   2. Clear the search box completely")
        print("   3. Select 'Standard' from format dropdown")
        print("   4. Should show all Standard-legal cards")
        print("   5. Switch to 'Modern' - should show all Modern cards")
        print("   6. Switch back to 'All Formats' - should show popular cards")
    else:
        print("\n❌ Fix failed - please check error messages above")
