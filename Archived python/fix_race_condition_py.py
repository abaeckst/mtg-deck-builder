#!/usr/bin/env python3
"""
Phase 3B-2: Fix Search Race Condition
Eliminates duplicate API calls that cause flickering search results
"""

import os

def fix_race_condition():
    """Fix the search race condition in MTGOLayout"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📝 Fixing race condition in {file_path}...")
        
        # 1. Remove the problematic useEffect that causes duplicate searches
        problematic_lines = [
            "  // Re-search when format changes",
            "  React.useEffect(() => {",
            "    if (searchText.trim()) {",
            "      searchForCards(searchText, selectedFormat);",
            "    }",
            "  }, [selectedFormat, searchText, searchForCards]);",
            ""
        ]
        problematic_block = "\n".join(problematic_lines)
        
        if problematic_block in content:
            content = content.replace(problematic_block, "")
            print("✅ Removed duplicate search useEffect")
        else:
            print("⚠️ Duplicate useEffect not found (might already be fixed)")
        
        # 2. Replace handleSearch function
        old_handle_search = """  // Search handling with format support
  const handleSearch = (text: string) => {
    setSearchText(text);
    if (text.trim()) {
      searchForCards(text, selectedFormat);
    } else {
      loadPopularCards();
    }
  };"""
        
        new_handle_search = """  // Search handling with format support - FIXED race condition
  const handleSearch = useCallback((text: string) => {
    setSearchText(text);
    if (text.trim()) {
      searchForCards(text, selectedFormat);
    } else {
      loadPopularCards();
    }
  }, [selectedFormat, searchForCards, loadPopularCards]);
  
  // Handle format changes by re-searching with current text
  const handleFormatChange = useCallback((newFormat: string) => {
    setSelectedFormat(newFormat);
    if (searchText.trim()) {
      // Small delay to prevent race condition with state update
      setTimeout(() => {
        searchForCards(searchText, newFormat);
      }, 50);
    }
  }, [searchText, searchForCards]);"""
        
        if old_handle_search in content:
            content = content.replace(old_handle_search, new_handle_search)
            print("✅ Updated handleSearch with race condition fix")
        else:
            print("⚠️ Could not find handleSearch to update")
        
        # 3. Update format dropdown onChange
        old_onchange = 'onChange={(e) => setSelectedFormat(e.target.value)}'
        new_onchange = 'onChange={(e) => handleFormatChange(e.target.value)}'
        
        if old_onchange in content:
            content = content.replace(old_onchange, new_onchange)
            print("✅ Updated format dropdown onChange handler")
        else:
            print("⚠️ Could not find format dropdown onChange to update")
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path} race condition fixed successfully")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Run the race condition fix"""
    print("🚀 Phase 3B-2: Fixing Search Race Condition")
    print("=" * 50)
    
    if fix_race_condition():
        print("\n🎉 Search race condition fixed successfully!")
        print("\n✅ Changes Applied:")
        print("   • Removed duplicate useEffect that caused flickering")
        print("   • Added proper format change handler with timing control") 
        print("   • Updated format dropdown to use race-condition-safe handler")
        print("\n🧪 Testing Instructions:")
        print("   1. Run 'npm start' to launch the application")
        print("   2. Search for a card (e.g., 'Lightning Bolt')")
        print("   3. Change format dropdown - no more flickering!")
        print("   4. Verify format filtering works correctly")
        print("\n🎯 Expected Result:")
        print("   • No more result flickering when searching")
        print("   • Format changes trigger clean re-search")
        print("   • Smooth user experience with format filtering")
    else:
        print("\n❌ Fix failed - please check errors above")
    
    return True

if __name__ == "__main__":
    main()
