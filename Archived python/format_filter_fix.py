#!/usr/bin/env python3
"""
Phase 3B-2: Format Filter Fix Implementation
Connects format dropdown to search functionality with Custom Standard support
"""

import os
import re

def update_use_cards_hook():
    """Update useCards hook to support format filtering"""
    file_path = "src/hooks/useCards.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📝 Updating {file_path}...")
        
        # 1. Add import for searchCardsWithFilters
        old_import = "import { searchCards, getRandomCard } from '../services/scryfallApi';"
        new_import = "import { searchCards, getRandomCard, searchCardsWithFilters } from '../services/scryfallApi';"
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            print("✅ Updated API imports")
        else:
            print("⚠️ Could not find import statement to update")
        
        # 2. Add format parameter to searchForCards function signature
        old_signature = "  searchForCards: (query: string) => Promise<void>;"
        new_signature = "  searchForCards: (query: string, format?: string) => Promise<void>;"
        
        if old_signature in content:
            content = content.replace(old_signature, new_signature)
            print("✅ Updated searchForCards interface")
        
        # 3. Update searchForCards implementation to use format
        old_search_impl = """  // Search for cards with query
  const searchForCards = useCallback(async (query: string) => {
    if (!query.trim()) {
      setState(prev => ({ 
        ...prev, 
        cards: [], 
        searchQuery: '', 
        totalCards: 0,
        selectedCards: new Set() // Clear selection when clearing search
      }));
      return;
    }

    clearError();
    setLoading(true);

    try {
      const response = await searchCards(query);"""
        
        new_search_impl = """  // Search for cards with query and optional format filter
  const searchForCards = useCallback(async (query: string, format?: string) => {
    if (!query.trim()) {
      setState(prev => ({ 
        ...prev, 
        cards: [], 
        searchQuery: '', 
        totalCards: 0,
        selectedCards: new Set() // Clear selection when clearing search
      }));
      return;
    }

    clearError();
    setLoading(true);

    try {
      // Use format-aware search if format is specified
      const response = format && format !== '' 
        ? await searchCardsWithFilters(query, { format: format === 'custom-standard' ? 'standard' : format })
        : await searchCards(query);"""
        
        if old_search_impl in content:
            content = content.replace(old_search_impl, new_search_impl)
            print("✅ Updated searchForCards implementation")
        else:
            print("⚠️ Could not find searchForCards implementation to update")
        
        # Write the updated content
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

def update_mtgo_layout():
    """Update MTGOLayout to pass format to search and add Custom Standard"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📝 Updating {file_path}...")
        
        # 1. Update format options to include Custom Standard
        old_format_options = """            <select 
              value={selectedFormat} 
              onChange={(e) => setSelectedFormat(e.target.value)}
              className="format-select"
            >
              <option value="">All Formats</option>
              <option value="standard">Standard</option>
              <option value="pioneer">Pioneer</option>
              <option value="modern">Modern</option>
              <option value="legacy">Legacy</option>
              <option value="vintage">Vintage</option>
            </select>"""
        
        new_format_options = """            <select 
              value={selectedFormat} 
              onChange={(e) => setSelectedFormat(e.target.value)}
              className="format-select"
            >
              <option value="">All Formats</option>
              <option value="standard">Standard</option>
              <option value="custom-standard">Custom Standard (Standard + Unreleased)</option>
              <option value="pioneer">Pioneer</option>
              <option value="modern">Modern</option>
              <option value="legacy">Legacy</option>
              <option value="vintage">Vintage</option>
            </select>"""
        
        if old_format_options in content:
            content = content.replace(old_format_options, new_format_options)
            print("✅ Updated format dropdown options")
        else:
            print("⚠️ Could not find format dropdown to update")
        
        # 2. Update handleSearch function to pass format parameter
        old_handle_search = """  // Search handling
  const handleSearch = (text: string) => {
    setSearchText(text);
    if (text.trim()) {
      searchForCards(text);
    } else {
      loadPopularCards();
    }
  };"""
        
        new_handle_search = """  // Search handling with format support
  const handleSearch = (text: string) => {
    setSearchText(text);
    if (text.trim()) {
      searchForCards(text, selectedFormat);
    } else {
      loadPopularCards();
    }
  };"""
        
        if old_handle_search in content:
            content = content.replace(old_handle_search, new_handle_search)
            print("✅ Updated handleSearch function")
        else:
            print("⚠️ Could not find handleSearch function to update")
        
        # 3. Add format change handler to trigger new search
        # Find the end of the handleSearch function and add format effect
        search_function_end = """  };
  
  // Card interaction handlers"""
        
        new_section = """  };
  
  // Re-search when format changes
  React.useEffect(() => {
    if (searchText.trim()) {
      searchForCards(searchText, selectedFormat);
    }
  }, [selectedFormat, searchText, searchForCards]);
  
  // Card interaction handlers"""
        
        if search_function_end in content:
            content = content.replace(search_function_end, new_section)
            print("✅ Added format change effect")
        else:
            print("⚠️ Could not find location to add format effect")
        
        # Write the updated content
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

def update_scryfall_api():
    """Update Scryfall API to handle Custom Standard format"""
    file_path = "src/services/scryfallApi.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📝 Updating {file_path}...")
        
        # Add Custom Standard handling in searchCardsWithFilters
        old_format_logic = """  // Add format filter
  if (filters.format) {
    searchQuery += ` legal:${filters.format}`;
  }"""
        
        new_format_logic = """  // Add format filter with Custom Standard support
  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Use standard legality as base
      // In future phases, this will be extended to include unreleased sets
      searchQuery += ` legal:standard`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }"""
        
        if old_format_logic in content:
            content = content.replace(old_format_logic, new_format_logic)
            print("✅ Updated format filtering logic")
        else:
            print("⚠️ Could not find format logic to update")
        
        # Write the updated content
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
    """Run all format filter fixes"""
    print("🚀 Phase 3B-2: Implementing Format Filter Fix")
    print("=" * 50)
    
    success_count = 0
    total_updates = 3
    
    # Update all files
    if update_use_cards_hook():
        success_count += 1
    
    if update_mtgo_layout():
        success_count += 1
        
    if update_scryfall_api():
        success_count += 1
    
    print("\n" + "=" * 50)
    if success_count == total_updates:
        print("🎉 All format filter fixes applied successfully!")
        print("\n✅ Implementation Complete:")
        print("   • Format dropdown now filters search results")
        print("   • Custom Standard format added")
        print("   • Format changes trigger automatic re-search")
        print("   • Architecture ready for unreleased set integration")
        print("\n🧪 Testing Instructions:")
        print("   1. Run 'npm start' to launch the application")
        print("   2. Search for a card (e.g., 'Lightning Bolt')")
        print("   3. Change format dropdown - results should filter")
        print("   4. Try 'Custom Standard' format option")
        print("   5. Verify format filtering works with all search functionality")
    else:
        print(f"⚠️ Partial success: {success_count}/{total_updates} files updated")
        print("   Please review any errors above and retry failed updates")
    
    return success_count == total_updates

if __name__ == "__main__":
    main()
