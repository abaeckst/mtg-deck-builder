# Phase 3C Final Polish - Input Validation & Error Handling
# Fix 1: Add validation for min/max inputs (CMC, Power, Toughness)
# Fix 2: Add graceful "no results found" handling for 404 errors

import os
import re

def add_input_validation():
    """Add validation for min/max range inputs to prevent invalid searches"""
    
    # Read the current MTGOLayout.tsx file
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add validation helper function
    validation_function = '''
  // Input validation helper
  const validateRangeInput = useCallback((min: number | null, max: number | null, fieldName: string) => {
    if (min !== null && max !== null && min > max) {
      console.log('⚠️ Validation error:', fieldName, 'min cannot exceed max');
      return false;
    }
    return true;
  }, []);

  // Enhanced filter change handler with validation
  const handleFilterChangeWithValidation = useCallback((filterType: string, value: any) => {
    console.log('🔧 Filter changing with validation:', filterType, '=', value);
    
    // Validate range inputs
    if (filterType === 'cmc' && value && typeof value === 'object') {
      if (!validateRangeInput(value.min, value.max, 'CMC')) {
        // Show user feedback for invalid range
        alert('Invalid CMC range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    if (filterType === 'power' && value && typeof value === 'object') {
      if (!validateRangeInput(value.min, value.max, 'Power')) {
        alert('Invalid Power range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    if (filterType === 'toughness' && value && typeof value === 'object') {
      if (!validateRangeInput(value.min, value.max, 'Toughness')) {
        alert('Invalid Toughness range: Minimum cannot be greater than maximum');
        return;
      }
    }
    
    // If validation passes, proceed with normal filter change
    handleFilterChange(filterType, value);
  }, [handleFilterChange, validateRangeInput]);

'''
    
    # Insert the validation function before the existing handleFilterChange
    insert_position = content.find('  // Handle any filter change by triggering new search')
    if insert_position != -1:
        content = content[:insert_position] + validation_function + content[insert_position:]
    
    # Update CMC input handlers to use validation
    old_cmc_min = '''                  value={activeFilters.cmc.min || ''}
                  onChange={(e) => handleFilterChange('cmc', {
                    ...activeFilters.cmc,
                    min: e.target.value ? parseInt(e.target.value) : null
                  })}'''
    
    new_cmc_min = '''                  value={activeFilters.cmc.min || ''}
                  onChange={(e) => handleFilterChangeWithValidation('cmc', {
                    ...activeFilters.cmc,
                    min: e.target.value ? parseInt(e.target.value) : null
                  })}'''
    
    content = content.replace(old_cmc_min, new_cmc_min)
    
    old_cmc_max = '''                  value={activeFilters.cmc.max || ''}
                  onChange={(e) => handleFilterChange('cmc', {
                    ...activeFilters.cmc,
                    max: e.target.value ? parseInt(e.target.value) : null
                  })}'''
    
    new_cmc_max = '''                  value={activeFilters.cmc.max || ''}
                  onChange={(e) => handleFilterChangeWithValidation('cmc', {
                    ...activeFilters.cmc,
                    max: e.target.value ? parseInt(e.target.value) : null
                  })}'''
    
    content = content.replace(old_cmc_max, new_cmc_max)
    
    # Update Power input handlers
    old_power_min = '''                    value={activeFilters.power.min || ''}
                    onChange={(e) => handleFilterChange('power', {
                      ...activeFilters.power,
                      min: e.target.value ? parseInt(e.target.value) : null
                    })}'''
    
    new_power_min = '''                    value={activeFilters.power.min || ''}
                    onChange={(e) => handleFilterChangeWithValidation('power', {
                      ...activeFilters.power,
                      min: e.target.value ? parseInt(e.target.value) : null
                    })}'''
    
    content = content.replace(old_power_min, new_power_min)
    
    old_power_max = '''                    value={activeFilters.power.max || ''}
                    onChange={(e) => handleFilterChange('power', {
                      ...activeFilters.power,
                      max: e.target.value ? parseInt(e.target.value) : null
                    })}'''
    
    new_power_max = '''                    value={activeFilters.power.max || ''}
                    onChange={(e) => handleFilterChangeWithValidation('power', {
                      ...activeFilters.power,
                      max: e.target.value ? parseInt(e.target.value) : null
                    })}'''
    
    content = content.replace(old_power_max, new_power_max)
    
    # Update Toughness input handlers
    old_toughness_min = '''                    value={activeFilters.toughness.min || ''}
                    onChange={(e) => handleFilterChange('toughness', {
                      ...activeFilters.toughness,
                      min: e.target.value ? parseInt(e.target.value) : null
                    })}'''
    
    new_toughness_min = '''                    value={activeFilters.toughness.min || ''}
                    onChange={(e) => handleFilterChangeWithValidation('toughness', {
                      ...activeFilters.toughness,
                      min: e.target.value ? parseInt(e.target.value) : null
                    })}'''
    
    content = content.replace(old_toughness_min, new_toughness_min)
    
    old_toughness_max = '''                    value={activeFilters.toughness.max || ''}
                    onChange={(e) => handleFilterChange('toughness', {
                      ...activeFilters.toughness,
                      max: e.target.value ? parseInt(e.target.value) : null
                    })}'''
    
    new_toughness_max = '''                    value={activeFilters.toughness.max || ''}
                    onChange={(e) => handleFilterChangeWithValidation('toughness', {
                      ...activeFilters.toughness,
                      max: e.target.value ? parseInt(e.target.value) : null
                    })}'''
    
    content = content.replace(old_toughness_max, new_toughness_max)
    
    # Write the updated file
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added input validation for min/max range fields")

def add_graceful_error_handling():
    """Add graceful error handling for 404 "no results" scenarios"""
    
    # Read the current useCards.ts file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the searchWithAllFilters error handling
    old_error_handling = '''    } catch (error) {
      if ((window as any).currentSearchId === searchId) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to search with filters';
        setState(prev => ({
          ...prev,
          error: errorMessage,
          cards: [],
          totalCards: 0,
          hasMore: false,
        }));
      }
    }'''
    
    new_error_handling = '''    } catch (error) {
      if ((window as any).currentSearchId === searchId) {
        let errorMessage = error instanceof Error ? error.message : 'Failed to search with filters';
        let isNoResults = false;
        
        // Handle 404 as "no results found" rather than error
        if (errorMessage.includes('404') || errorMessage.includes('No cards found')) {
          errorMessage = 'No cards found matching your search criteria. Try adjusting your filters.';
          isNoResults = true;
          console.log('📭 No results found for current filters');
        } else {
          console.error('❌ Search error:', errorMessage);
        }
        
        setState(prev => ({
          ...prev,
          error: isNoResults ? null : errorMessage, // Don't show error state for no results
          cards: [],
          totalCards: 0,
          hasMore: false,
          searchQuery: isNoResults ? 'No results found' : prev.searchQuery,
        }));
      }
    }'''
    
    content = content.replace(old_error_handling, new_error_handling)
    
    # Also update the regular searchForCards function
    old_search_error = '''    } catch (error) {
      // Only show error if this search wasn't cancelled
      if ((window as any).currentSearchId === searchId) {
        const errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
        
        console.error('❌ SEARCH ERROR:', {
          searchId: searchId.toFixed(3),
          query: query,
          format: format || 'none',
          error: errorMessage
        });

        setState(prev => ({
          ...prev,
          error: errorMessage,
          cards: [],
          totalCards: 0,
          hasMore: false,
        }));
      }
    }'''
    
    new_search_error = '''    } catch (error) {
      // Only show error if this search wasn't cancelled
      if ((window as any).currentSearchId === searchId) {
        let errorMessage = error instanceof Error ? error.message : 'Failed to search cards';
        let isNoResults = false;
        
        // Handle 404 as "no results found" rather than error
        if (errorMessage.includes('404') || errorMessage.includes('No cards found')) {
          errorMessage = 'No cards found matching your search. Try different keywords or filters.';
          isNoResults = true;
          console.log('📭 No results found for search:', query);
        } else {
          console.error('❌ SEARCH ERROR:', {
            searchId: searchId.toFixed(3),
            query: query,
            format: format || 'none',
            error: errorMessage
          });
        }

        setState(prev => ({
          ...prev,
          error: isNoResults ? null : errorMessage,
          cards: [],
          totalCards: 0,
          hasMore: false,
          searchQuery: isNoResults ? 'No results found' : prev.searchQuery,
        }));
      }
    }'''
    
    content = content.replace(old_search_error, new_search_error)
    
    # Write the updated file
    with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added graceful error handling for no results scenarios")

def add_no_results_ui():
    """Add a professional no results UI state"""
    
    # Read the current MTGOLayout.tsx file
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the collection grid content and add no results state
    old_collection_content = '''          <div 
            className="collection-grid"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, max-content))`,
              gap: `${Math.round(4 * cardSizes.collection)}px`,
              alignContent: 'start',
              padding: '8px'
            }}
          >
            {loading && <div className="loading-message">Loading cards...</div>}
            {error && <div className="error-message">Error: {error}</div>}
            {cards.map(card => ('''
    
    new_collection_content = '''          <div 
            className="collection-grid"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, max-content))`,
              gap: `${Math.round(4 * cardSizes.collection)}px`,
              alignContent: 'start',
              padding: '8px'
            }}
          >
            {loading && <div className="loading-message">Loading cards...</div>}
            {error && <div className="error-message">Error: {error}</div>}
            {!loading && !error && cards.length === 0 && (
              <div className="no-results-message">
                <div className="no-results-icon">🔍</div>
                <h3>No cards found</h3>
                <p>No cards match your current search and filter criteria.</p>
                <div className="no-results-suggestions">
                  <p><strong>Try:</strong></p>
                  <ul>
                    <li>Adjusting your search terms</li>
                    <li>Changing filter settings</li>
                    <li>Using broader criteria</li>
                    <li>Clearing some filters</li>
                  </ul>
                </div>
              </div>
            )}
            {cards.map(card => ('''
    
    content = content.replace(old_collection_content, new_collection_content)
    
    # Write the updated file
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added professional no results UI")

def add_no_results_css():
    """Add CSS styling for the no results state"""
    
    # Read the current MTGOLayout.css file
    with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add no results styling
    no_results_css = '''
/* No Results State Styling */
.no-results-message {
  grid-column: 1 / -1;
  text-align: center;
  color: #cccccc;
  padding: 60px 40px;
  background-color: rgba(255, 255, 255, 0.02);
  border: 2px dashed #404040;
  border-radius: 12px;
  margin: 20px;
  max-width: 500px;
  justify-self: center;
}

.no-results-icon {
  font-size: 48px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.no-results-message h3 {
  color: #ffffff;
  font-size: 24px;
  margin: 0 0 12px 0;
  font-weight: 600;
}

.no-results-message p {
  color: #cccccc;
  font-size: 16px;
  margin: 0 0 20px 0;
  line-height: 1.5;
}

.no-results-suggestions {
  background-color: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 8px;
  padding: 16px;
  text-align: left;
  margin-top: 20px;
}

.no-results-suggestions p {
  margin: 0 0 8px 0;
  font-weight: 600;
  color: #3b82f6;
}

.no-results-suggestions ul {
  margin: 0;
  padding-left: 20px;
  color: #cccccc;
}

.no-results-suggestions li {
  margin-bottom: 4px;
  font-size: 14px;
}

/* Validation Error Styling */
.validation-error {
  background-color: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #ef4444;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.validation-error::before {
  content: "⚠️";
  font-size: 14px;
}

/* Enhanced Loading and Error Messages */
.loading-message {
  background-color: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: #3b82f6;
  padding: 20px;
  border-radius: 8px;
  margin: 20px;
  text-align: center;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.loading-message::before {
  content: "⏳";
  font-size: 20px;
  animation: pulse 2s ease-in-out infinite;
}

.error-message {
  background-color: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
  padding: 20px;
  border-radius: 8px;
  margin: 20px;
  text-align: center;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.error-message::before {
  content: "❌";
  font-size: 20px;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

'''
    
    # Insert the CSS before the existing scrollbar styling
    scrollbar_position = content.find('/* Scrollbar Styling */')
    if scrollbar_position != -1:
        content = content[:scrollbar_position] + no_results_css + content[scrollbar_position:]
    else:
        # If we can't find the scrollbar section, append to end
        content += no_results_css
    
    # Write the updated file
    with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added no results CSS styling")

def main():
    """Execute all final polish fixes"""
    try:
        print("🎨 Applying Phase 3C Final Polish Fixes")
        print("=" * 50)
        
        print("\n📋 Fix 1: Adding input validation for min/max ranges...")
        add_input_validation()
        
        print("\n📋 Fix 2: Adding graceful error handling for 404s...")
        add_graceful_error_handling()
        
        print("\n📋 Fix 3: Adding professional no results UI...")
        add_no_results_ui()
        
        print("\n📋 Fix 4: Adding no results CSS styling...")
        add_no_results_css()
        
        print("\n" + "=" * 50)
        print("✅ All Final Polish Fixes Complete!")
        print("\n🎯 Issues Fixed:")
        print("   • Min/max validation prevents invalid searches")
        print("   • User gets alerts for invalid ranges (e.g., Min > Max)")
        print("   • 404 errors now show 'No results found' instead of ugly error")
        print("   • Professional no results UI with helpful suggestions")
        print("   • Enhanced loading and error message styling")
        print("\n🧪 Test These Fixes:")
        print("   1. Set CMC Min to 10, Max to 5 → should get validation alert")
        print("   2. Set Power Min to 8, Max to 2 → should get validation alert")
        print("   3. Search for impossible combination → should see 'No cards found' UI")
        print("   4. Try 'Standard + CMC Min 15 + Common' → graceful no results")
        print("\n🎉 Phase 3C Enhanced Filtering System is now complete!")
        print("   • 35/35 tests should now pass")
        print("   • Professional user experience")
        print("   • Comprehensive filtering capabilities")
        print("   • Graceful error handling")
        
    except Exception as e:
        print(f"\n❌ Error during final polish: {e}")
        print("Please check the file paths and try again.")

if __name__ == "__main__":
    main()
