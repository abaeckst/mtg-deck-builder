#!/usr/bin/env python3
"""
Fix the enhanced search query building in scryfallApi.ts
The issue is likely that the enhanced search is over-complicating simple queries
"""

import os

def fix_enhanced_search_query():
    """Fix the buildEnhancedSearchQuery function to handle simple searches correctly"""
    file_path = "src/services/scryfallApi.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the buildEnhancedSearchQuery function
        find_function = '''/**
 * Build enhanced search query with operator support
 */
function buildEnhancedSearchQuery(query: string): string {
  // Simple operator parsing for Phase 3E
  const parts: string[] = [];
  let workingQuery = query;
  
  // Handle quoted phrases
  const quotedPhrases = query.match(/"[^"]+"/g) || [];
  quotedPhrases.forEach(phrase => {
    parts.push(phrase); // Keep quoted phrases as-is for Scryfall
    workingQuery = workingQuery.replace(phrase, '');
  });
  
  // Handle exclusions
  const exclusions = workingQuery.match(/-\\w+/g) || [];
  exclusions.forEach(exclusion => {
    parts.push(exclusion); // Keep exclusions as-is
    workingQuery = workingQuery.replace(exclusion, '');
  });
  
  // Handle field-specific searches
  const fieldSearches = workingQuery.match(/(name|text|type):[\\w\\s]+/g) || [];
  fieldSearches.forEach(fieldSearch => {
    const [field, value] = fieldSearch.split(':');
    if (field === 'text') {
      parts.push(`oracle:${value}`); // Convert text: to oracle: for Scryfall
    } else {
      parts.push(fieldSearch); // Keep name: and type: as-is
    }
    workingQuery = workingQuery.replace(fieldSearch, '');
  });
  
  // Handle remaining terms as full-text search
  const remainingTerms = workingQuery.trim().split(/\\s+/).filter(term => term.length > 0);
  if (remainingTerms.length > 0) {
    const fullTextSearch = remainingTerms.join(' ');
    // Search across name, oracle text, and type for full-text capability
    parts.push(`(name:"${fullTextSearch}" OR oracle:"${fullTextSearch}" OR type:"${fullTextSearch}")`);
  }
  
  return parts.join(' ').trim() || '*';
}'''

        replace_function = '''/**
 * Build enhanced search query with operator support
 */
function buildEnhancedSearchQuery(query: string): string {
  // For simple queries without operators, just return the query as-is
  // This allows Scryfall's natural search to work normally
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    return query;
  }
  
  // Only do advanced parsing for queries with operators
  const parts: string[] = [];
  let workingQuery = query;
  
  // Handle quoted phrases
  const quotedPhrases = query.match(/"[^"]+"/g) || [];
  quotedPhrases.forEach(phrase => {
    parts.push(phrase); // Keep quoted phrases as-is for Scryfall
    workingQuery = workingQuery.replace(phrase, '');
  });
  
  // Handle exclusions
  const exclusions = workingQuery.match(/-\\w+/g) || [];
  exclusions.forEach(exclusion => {
    parts.push(exclusion); // Keep exclusions as-is
    workingQuery = workingQuery.replace(exclusion, '');
  });
  
  // Handle field-specific searches
  const fieldSearches = workingQuery.match(/(name|text|type):[\\w\\s]+/g) || [];
  fieldSearches.forEach(fieldSearch => {
    const [field, value] = fieldSearch.split(':');
    if (field === 'text') {
      parts.push(`oracle:${value}`); // Convert text: to oracle: for Scryfall
    } else {
      parts.push(fieldSearch); // Keep name: and type: as-is
    }
    workingQuery = workingQuery.replace(fieldSearch, '');
  });
  
  // Handle remaining terms - for advanced queries, do full-text search
  const remainingTerms = workingQuery.trim().split(/\\s+/).filter(term => term.length > 0);
  if (remainingTerms.length > 0) {
    const fullTextSearch = remainingTerms.join(' ');
    // Only use complex OR logic if we already have other operators
    if (parts.length > 0) {
      parts.push(`(name:"${fullTextSearch}" OR oracle:"${fullTextSearch}" OR type:"${fullTextSearch}")`);
    } else {
      // If no operators detected, just add the simple search
      parts.push(fullTextSearch);
    }
  }
  
  return parts.join(' ').trim() || query;
}'''
        
        if find_function in content:
            content = content.replace(find_function, replace_function)
            print("✅ Fixed buildEnhancedSearchQuery function")
        else:
            print("❌ Could not find buildEnhancedSearchQuery function to fix")
            return False
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
        
    except Exception as e:
        print(f"❌ Error fixing enhanced search query: {e}")
        return False

def main():
    """Run the search query fix"""
    print("🔧 Fixing enhanced search query building")
    print("=" * 45)
    
    if not os.path.exists("src/services/scryfallApi.ts"):
        print("❌ Error: scryfallApi.ts not found")
        return False
    
    if fix_enhanced_search_query():
        print("=" * 45)
        print("🎉 Enhanced search should now work correctly!")
        print("\\n🔧 Test these searches:")
        print('• Simple: "lightning"')
        print('• Operators: "flying -blue"')
        print('• Field search: "name:bolt"')
        print('• Exact phrase: "\\"destroy target creature\\""')
        print("\\n🔧 The search should now:")
        print("• Work with simple queries like before")
        print("• Add enhanced functionality for operator queries")
        print("• Provide autocomplete suggestions as you type")
    else:
        print("❌ Fix failed. Please check the error above.")
    
    return True

if __name__ == "__main__":
    main()