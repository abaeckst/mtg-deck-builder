#!/usr/bin/env python3
"""
Fix format filter in useCards.ts to work without search terms
Issue: Format dropdown only works when there's a search query
Solution: Allow format-only filtering to show all cards of that format
"""

def fix_format_standalone():
    file_path = "src/hooks/useCards.ts"
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading {file_path}")
        print(f"📏 File size: {len(content)} characters")
        
        # Find and replace the searchForCards function to handle format-only filtering
        old_empty_query_check = '''  const searchForCards = useCallback(async (query: string, format?: string) => {
    if (!query.trim()) {
      setState(prev => ({ 
        ...prev, 
        cards: [], 
        searchQuery: '', 
        totalCards: 0,
        selectedCards: new Set() // Clear selection when clearing search
      }));
      return;
    }'''
        
        new_empty_query_check = '''  const searchForCards = useCallback(async (query: string, format?: string) => {
    // Handle empty query cases
    if (!query.trim()) {
      // If there's a format selected, search for all cards in that format
      if (format && format !== '') {
        // Don't return early - continue with format-only search
        query = '*'; // Use wildcard to get all cards
      } else {
        // No query and no format - clear results
        setState(prev => ({ 
          ...prev, 
          cards: [], 
          searchQuery: '', 
          totalCards: 0,
          selectedCards: new Set() // Clear selection when clearing search
        }));
        return;
      }
    }'''
        
        if old_empty_query_check in content:
            content = content.replace(old_empty_query_check, new_empty_query_check)
            print("✅ Fix 1: Updated empty query handling to support format-only filtering")
        else:
            print("❌ Fix 1: Could not find empty query check pattern")
            return False
        
        # Update the success logging to show when it's a format-only search
        old_success_log = '''      console.log('✅ SEARCH SUCCESS:', {
        searchId: searchId.toFixed(3),
        query: query,
        format: format || 'none',
        resultCount: response.data.length,
        firstCard: response.data[0]?.name || 'NO_RESULTS'
      });'''
        
        new_success_log = '''      console.log('✅ SEARCH SUCCESS:', {
        searchId: searchId.toFixed(3),
        query: query,
        format: format || 'none',
        resultCount: response.data.length,
        firstCard: response.data[0]?.name || 'NO_RESULTS',
        isFormatOnly: query === '*'
      });'''
        
        if old_success_log in content:
            content = content.replace(old_success_log, new_success_log)
            print("✅ Fix 2: Updated success logging to indicate format-only searches")
        else:
            print("⚠️ Fix 2: Success log not found - not critical")
        
        # Update the state update to show appropriate search query text
        old_state_update = '''      // Only update state if this is still the current search
      setState(prev => ({
        ...prev,
        cards: response.data,
        searchQuery: query,
        totalCards: response.total_cards,
        hasMore: response.has_more,
        selectedCards: new Set(), // Clear selection on new search
      }));'''
        
        new_state_update = '''      // Only update state if this is still the current search
      setState(prev => ({
        ...prev,
        cards: response.data,
        searchQuery: query === '*' ? `All ${format || 'Cards'}` : query,
        totalCards: response.total_cards,
        hasMore: response.has_more,
        selectedCards: new Set(), // Clear selection on new search
      }));'''
        
        if old_state_update in content:
            content = content.replace(old_state_update, new_state_update)
            print("✅ Fix 3: Updated state to show descriptive text for format-only searches")
        else:
            print("⚠️ Fix 3: State update not found - not critical")
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"💾 Successfully updated {file_path}")
        print("🎯 Changes made:")
        print("   - Format filter now works without search terms")
        print("   - Selecting 'Standard' shows all Standard-legal cards")
        print("   - Uses '*' wildcard query for format-only searches")
        print("   - Shows descriptive text like 'All Standard' in search display")
        print("   - Maintains all existing search functionality")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        return False
    except Exception as e:
        print(f"❌ Error updating file: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing format filter to work without search terms...")
    success = fix_format_standalone()
    
    if success:
        print("\n✅ FORMAT FILTER FIX COMPLETE!")
        print("🧪 Test the fix:")
        print("   1. Run: npm start")
        print("   2. Clear any search terms (empty search box)")
        print("   3. Select 'Standard' from format dropdown")
        print("   4. Should show all Standard-legal cards")
        print("   5. Try other formats like 'Modern', 'Legacy'")
        print("   6. Search query should show 'All Standard', 'All Modern', etc.")
    else:
        print("\n❌ Fix failed - please check error messages above")
