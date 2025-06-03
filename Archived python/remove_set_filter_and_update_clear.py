#!/usr/bin/env python3
"""
Remove Set Filter and Update Features
1. Removes all set filter code from useCards.ts
2. Removes set filter UI from MTGOLayout.tsx
3. Updates clear deck button to clear both maindeck and sideboard
4. Changes default format to custom-standard
"""

import re
import os

def clean_use_cards():
    """Remove set filter functionality and update default format in useCards.ts"""
    file_path = "src/hooks/useCards.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        return False
    
    print(f"🔧 Cleaning useCards.ts...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove getSets import
        old_import = """import { searchCards, getRandomCard, searchCardsWithFilters, SearchFilters, enhancedSearchCards, getSearchSuggestions, getSets } from '../services/scryfallApi';"""
        new_import = """import { searchCards, getRandomCard, searchCardsWithFilters, SearchFilters, enhancedSearchCards, getSearchSuggestions } from '../services/scryfallApi';"""
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            print("✅ Removed getSets import")
        
        # Remove set filter state from UseCardsState interface
        old_state_interface = """  // Set filter state
  availableSets: any[];
  setSearchText: string;
  filteredSets: any[];"""
        
        if old_state_interface in content:
            content = content.replace(old_state_interface, "")
            print("✅ Removed set filter state from UseCardsState interface")
        
        # Remove set filter actions from UseCardsActions interface
        old_actions_interface = """  // Set filter actions
  updateSetSearchText: (text: string) => void;
  toggleSetSelection: (setCode: string) => void;"""
        
        if old_actions_interface in content:
            content = content.replace(old_actions_interface, "")
            print("✅ Removed set filter actions from UseCardsActions interface")
        
        # Update default format to custom-standard in state initialization
        old_format_default = """      format: 'standard',"""
        new_format_default = """      format: 'custom-standard',"""
        
        if old_format_default in content:
            content = content.replace(old_format_default, new_format_default)
            print("✅ Changed default format to custom-standard")
        
        # Remove set filter state initialization
        old_state_init = """    // Set filter state
    availableSets: [],
    setSearchText: '',
    filteredSets: [],"""
        
        if old_state_init in content:
            content = content.replace(old_state_init, "")
            print("✅ Removed set filter state initialization")
        
        # Remove sets loading effect
        old_sets_effect = """  // Load sets on mount
  useEffect(() => {
    getSets().then(sets => {
      setState(prev => ({
        ...prev,
        availableSets: sets,
        filteredSets: sets.slice(0, 20), // Show first 20 initially
      }));
    }).catch(error => {
      console.error('Failed to load sets:', error);
    });
  }, []);

  // Filter sets based on search
  useEffect(() => {
    if (!state.setSearchText.trim()) {
      setState(prev => ({
        ...prev,
        filteredSets: prev.availableSets.slice(0, 20),
      }));
    } else {
      const searchTerm = state.setSearchText.toLowerCase();
      const filtered = state.availableSets.filter(set =>
        set.name.toLowerCase().includes(searchTerm) ||
        set.code.toLowerCase().includes(searchTerm)
      );
      setState(prev => ({
        ...prev,
        filteredSets: filtered.slice(0, 20),
      }));
    }
  }, [state.setSearchText, state.availableSets]);"""
        
        if old_sets_effect in content:
            content = content.replace(old_sets_effect, "")
            print("✅ Removed sets loading and filtering effects")
        
        # Remove set filter functions
        old_set_functions = """  // Set filter functions
  const updateSetSearchText = useCallback((text: string) => {
    setState(prev => ({ ...prev, setSearchText: text }));
  }, []);

  const toggleSetSelection = useCallback((setCode: string) => {
    const newSets = state.activeFilters.sets.includes(setCode)
      ? state.activeFilters.sets.filter(code => code !== setCode)
      : [...state.activeFilters.sets, setCode];
    
    updateFilter('sets', newSets);
    
    // Trigger search with updated filters
    setTimeout(() => {
      enhancedSearch(state.searchQuery || '', {
        ...state.activeFilters,
        sets: newSets
      });
    }, 50);
  }, [state.activeFilters.sets, updateFilter, enhancedSearch, state.searchQuery, state.activeFilters]);"""
        
        if old_set_functions in content:
            content = content.replace(old_set_functions, "")
            print("✅ Removed set filter functions")
        
        # Remove set filter actions from return object
        old_return_actions = """    updateSetSearchText,
    toggleSetSelection,"""
        
        if old_return_actions in content:
            content = content.replace(old_return_actions, "")
            print("✅ Removed set filter actions from return object")
        
        # Update clearAllFilters to use custom-standard as default
        old_clear_filters = """        format: 'standard',"""
        new_clear_filters = """        format: 'custom-standard',"""
        
        # This should replace the format in clearAllFilters function
        if 'clearAllFilters' in content and old_clear_filters in content:
            # Find the clearAllFilters function and replace only within it
            clear_filters_start = content.find('const clearAllFilters')
            clear_filters_end = content.find('}, [loadPopularCards]);', clear_filters_start)
            if clear_filters_start != -1 and clear_filters_end != -1:
                clear_filters_section = content[clear_filters_start:clear_filters_end]
                if old_clear_filters in clear_filters_section:
                    new_clear_filters_section = clear_filters_section.replace(old_clear_filters, new_clear_filters)
                    content = content[:clear_filters_start] + new_clear_filters_section + content[clear_filters_end:]
                    print("✅ Updated clearAllFilters to use custom-standard default")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ SUCCESS: Cleaned useCards.ts")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to update {file_path}: {str(e)}")
        return False

def clean_mtgo_layout():
    """Remove set filter UI and update clear deck button in MTGOLayout.tsx"""
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        return False
    
    print(f"🔧 Cleaning MTGOLayout.tsx...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove set filter destructuring from useCards
        old_destructuring = """    availableSets,
    setSearchText: setFilterSearchText,
    filteredSets,
    updateSetSearchText,
    toggleSetSelection"""
        
        if old_destructuring in content:
            content = content.replace(old_destructuring, "")
            print("✅ Removed set filter destructuring")
        
        # Remove the entire Sets Group UI section
        old_sets_ui = """            
            {/* Sets Group */}
            <div className="filter-group">
              <label>Sets</label>
              <div className="set-filter-container">
                <input
                  type="text"
                  placeholder="Search sets..."
                  value={setFilterSearchText}
                  onChange={(e) => updateSetSearchText(e.target.value)}
                  className="set-search-input"
                  style={{
                    width: '100%',
                    padding: '6px 10px',
                    borderRadius: '4px',
                    border: '1px solid #404040',
                    backgroundColor: '#2a2a2a',
                    color: '#fff',
                    fontSize: '14px',
                    marginBottom: '8px'
                  }}
                />
                <div className="set-selection-area" style={{
                  maxHeight: '150px',
                  overflowY: 'auto',
                  border: '1px solid #404040',
                  borderRadius: '4px',
                  backgroundColor: '#1e1e1e',
                  padding: '4px'
                }}>
                  {filteredSets.map((set: any) => (
                    <label key={set.code} className="set-checkbox-label" style={{
                      display: 'block',
                      padding: '4px 8px',
                      cursor: 'pointer',
                      borderRadius: '2px',
                      fontSize: '13px',
                      color: '#ccc',
                      // Note: hover styles should be in CSS file
                    }}>
                      <input
                        type="checkbox"
                        checked={activeFilters.sets.includes(set.code)}
                        onChange={() => toggleSetSelection(set.code)}
                        style={{ marginRight: '8px' }}
                      />
                      <span className="set-display">
                        {set.name} ({set.code})
                      </span>
                    </label>
                  ))}
                  {filteredSets.length === 0 && setFilterSearchText && (
                    <div style={{ padding: '8px', color: '#888', textAlign: 'center', fontSize: '13px' }}>
                      No sets found
                    </div>
                  )}
                </div>
                {activeFilters.sets.length > 0 && (
                  <div style={{ marginTop: '8px', fontSize: '12px', color: '#888' }}>
                    {activeFilters.sets.length} set{activeFilters.sets.length !== 1 ? 's' : ''} selected
                  </div>
                )}
              </div>
            </div>"""
        
        if old_sets_ui in content:
            content = content.replace(old_sets_ui, "")
            print("✅ Removed set filter UI section")
        
        # Update clear deck button to clear both deck and sideboard
        old_clear_deck = """  // PHASE 3A: Clear deck functionality - FIXED
  const handleClearDeck = useCallback(() => {
    setMainDeck([]);
    clearSelection();
    console.log('Deck cleared - all cards moved back to collection');
  }, [clearSelection]);"""
        
        new_clear_deck = """  // Clear both deck and sideboard functionality
  const handleClearDeck = useCallback(() => {
    setMainDeck([]);
    setSideboard([]);
    clearSelection();
    console.log('Deck and sideboard cleared - all cards moved back to collection');
  }, [clearSelection]);"""
        
        if old_clear_deck in content:
            content = content.replace(old_clear_deck, new_clear_deck)
            print("✅ Updated clear deck button to clear both deck and sideboard")
        
        # Update the button text to reflect it clears both
        old_button_text = """                <button onClick={handleClearDeck} title="Clear all cards from deck">
                  Clear Deck
                </button>"""
        
        new_button_text = """                <button onClick={handleClearDeck} title="Clear all cards from deck and sideboard">
                  Clear All
                </button>"""
        
        if old_button_text in content:
            content = content.replace(old_button_text, new_button_text)
            print("✅ Updated clear button text to 'Clear All'")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ SUCCESS: Cleaned MTGOLayout.tsx")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to update {file_path}: {str(e)}")
        return False

def clean_scryfall_api():
    """Remove set filter functions from scryfallApi.ts"""
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File {file_path} not found!")
        return False
    
    print(f"🔧 Cleaning scryfallApi.ts...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove set filter logic from searchCardsWithFilters
        old_set_logic = """  // Add set filters (multiple sets support)
  if (filters.sets && filters.sets.length > 0) {
    console.log('🎯 Set filter being applied:', filters.sets);
    if (filters.sets.length === 1) {
      const setCode = filters.sets[0].toLowerCase();
      console.log('🎯 Single set query:', `set:${setCode}`);
      searchQuery += ` set:${setCode}`;
    } else {
      const setQuery = filters.sets.map(set => `set:${set.toLowerCase()}`).join(' OR ');
      console.log('🎯 Multiple set query:', `(${setQuery})`);
      searchQuery += ` (${setQuery})`;
    }
  }"""
        
        if old_set_logic in content:
            content = content.replace(old_set_logic, "")
            print("✅ Removed set filter logic from searchCardsWithFilters")
        
        # Remove set search functions
        old_set_functions = """/**
 * Search sets with text query
 */
export const searchSets = async (query: string): Promise<any[]> => {
  const allSets = await getSets();
  
  if (!query.trim()) return allSets.slice(0, 20);
  
  const searchTerm = query.toLowerCase();
  return allSets.filter(set => 
    set.name.toLowerCase().includes(searchTerm) ||
    set.code.toLowerCase().includes(searchTerm)
  ).slice(0, 20);
};

/**
 * Get popular/recent sets for quick selection
 */
export const getPopularSets = async (): Promise<any[]> => {
  const allSets = await getSets();
  // Return last 10 expansion sets
  return allSets
    .filter(set => set.set_type === 'expansion')
    .sort((a, b) => new Date(b.released_at).getTime() - new Date(a.released_at).getTime())
    .slice(0, 10);
};"""
        
        if old_set_functions in content:
            content = content.replace(old_set_functions, "")
            print("✅ Removed set search functions")
        
        # Remove debug logging
        old_debug = """  console.log('🎯 Final search query:', searchQuery.trim());"""
        if old_debug in content:
            content = content.replace(old_debug, "")
            print("✅ Removed debug logging")
        
        old_enhanced_debug = """  console.log('🔍 Enhanced search - query:', searchQuery, 'filters:', filters);"""
        if old_enhanced_debug in content:
            content = content.replace(old_enhanced_debug, "")
            print("✅ Removed enhanced search debugging")
        
        # Write the updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ SUCCESS: Cleaned scryfallApi.ts")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to update {file_path}: {str(e)}")
        return False

def main():
    print("🚀 MTG Deck Builder - Remove Set Filter and Update Features")
    print("=" * 70)
    print("This script removes set filter and updates clear deck functionality.\n")
    
    success = True
    
    # Step 1: Clean useCards.ts
    print("📦 Step 1: Cleaning useCards.ts...")
    if not clean_use_cards():
        success = False
    
    # Step 2: Clean MTGOLayout.tsx
    print("\n🎨 Step 2: Cleaning MTGOLayout.tsx...")
    if not clean_mtgo_layout():
        success = False
    
    # Step 3: Clean scryfallApi.ts
    print("\n🔧 Step 3: Cleaning scryfallApi.ts...")
    if not clean_scryfall_api():
        success = False
    
    if success:
        print("\n🎉 All cleanup completed successfully!")
        print("📋 Changes made:")
        print("   ✅ Removed all set filter code and UI")
        print("   ✅ Updated clear deck button to clear both deck and sideboard")
        print("   ✅ Changed button text to 'Clear All'")
        print("   ✅ Set default format to 'Custom Standard'")
        print("\n📋 Next steps:")
        print("   1. Run 'npm start' to test the changes")
        print("   2. Verify app loads with Custom Standard format selected")
        print("   3. Test that 'Clear All' button clears both deck and sideboard")
        print("   4. Confirm set filter is completely removed from UI")
    else:
        print("\n❌ Some cleanup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()    