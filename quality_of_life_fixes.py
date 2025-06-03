#!/usr/bin/env python3
"""
Quality of Life Improvements - Panel Resizing & Multi-Word Search Fix
Fixes both panel resizing constraints and multi-word search functionality
"""

import os
import re

def update_useLayout_constraints():
    """Update panel constraints to allow much smaller minimum sizes"""
    
    file_path = "src/hooks/useLayout.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the CONSTRAINTS object
        old_constraints = """const CONSTRAINTS = {
  filterPanelWidth: { min: 200, max: 500 },
  deckAreaHeightPercent: { min: 25, max: 60 }, // 25% to 60% of screen height
  sideboardWidth: { min: 200, max: 1000 },"""
        
        new_constraints = """const CONSTRAINTS = {
  filterPanelWidth: { min: 20, max: 500 },     // Allow near-invisible (20px = resize handle only)
  deckAreaHeightPercent: { min: 8, max: 75 },  // Allow much smaller/larger ranges
  sideboardWidth: { min: 20, max: 1000 },      // Allow near-invisible (20px = resize handle only)"""
        
        if old_constraints in content:
            content = content.replace(old_constraints, new_constraints)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Updated useLayout.ts constraints for extended panel resizing")
            return True
        else:
            print("❌ Could not find CONSTRAINTS object pattern in useLayout.ts")
            return False
            
    except Exception as e:
        print(f"❌ Error updating useLayout.ts: {e}")
        return False

def fix_multi_word_search():
    """Fix multi-word search functionality in scryfallApi.ts"""
    
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the buildEnhancedSearchQuery function
        old_function = """function buildEnhancedSearchQuery(query: string): string {
  // For simple queries without operators, enable full-text search
  // This searches across name, oracle text, and type line
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    return `(name:${query} OR oracle:${query} OR type:${query})`;
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
  const exclusions = workingQuery.match(/-\w+/g) || [];
  exclusions.forEach(exclusion => {
    parts.push(exclusion); // Keep exclusions as-is
    workingQuery = workingQuery.replace(exclusion, '');
  });
  
  // Handle field-specific searches
  const fieldSearches = workingQuery.match(/(name|text|type):[\w\s]+/g) || [];
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
  const remainingTerms = workingQuery.trim().split(/\s+/).filter(term => term.length > 0);
  if (remainingTerms.length > 0) {
    const fullTextSearch = remainingTerms.join(' ');
    // Only use complex OR logic if we already have other operators
    if (parts.length > 0) {
      parts.push(`(name:${fullTextSearch} OR oracle:${fullTextSearch} OR type:${fullTextSearch})`);
    } else {
      // If no operators detected, just add the simple search
      parts.push(fullTextSearch);
    }
  }
  
  return parts.join(' ').trim() || query;
}"""

        new_function = """function buildEnhancedSearchQuery(query: string): string {
  // FIXED: Handle multi-word search properly with quotes
  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    // Check if query contains multiple words
    const words = query.trim().split(/\s+/);
    
    if (words.length > 1) {
      // Multi-word query: quote the entire phrase for each field
      const quotedQuery = `"${query}"`;
      return `(name:${quotedQuery} OR oracle:${quotedQuery} OR type:${quotedQuery})`;
    } else {
      // Single word: no quotes needed
      return `(name:${query} OR oracle:${query} OR type:${query})`;
    }
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
  
  // Handle exclusions (improved pattern to catch multi-word exclusions)
  const exclusions = workingQuery.match(/-"[^"]+"|--?[\w\s]+/g) || [];
  exclusions.forEach(exclusion => {
    parts.push(exclusion); // Keep exclusions as-is
    workingQuery = workingQuery.replace(exclusion, '');
  });
  
  // Handle field-specific searches (improved pattern)
  const fieldSearches = workingQuery.match(/(name|text|type|oracle):"[^"]+"|(?:name|text|type|oracle):[\w\s]+(?=\s|$)/g) || [];
  fieldSearches.forEach(fieldSearch => {
    const colonIndex = fieldSearch.indexOf(':');
    const field = fieldSearch.substring(0, colonIndex);
    const value = fieldSearch.substring(colonIndex + 1);
    
    if (field === 'text') {
      parts.push(`oracle:${value}`); // Convert text: to oracle: for Scryfall
    } else {
      parts.push(fieldSearch); // Keep name:, type:, oracle: as-is
    }
    workingQuery = workingQuery.replace(fieldSearch, '');
  });
  
  // Handle remaining terms - for advanced queries, do full-text search
  const remainingTerms = workingQuery.trim().split(/\s+/).filter(term => term.length > 0);
  if (remainingTerms.length > 0) {
    const fullTextSearch = remainingTerms.join(' ');
    
    // If multiple words, quote them for proper multi-word search
    const searchTerm = remainingTerms.length > 1 ? `"${fullTextSearch}"` : fullTextSearch;
    
    // Only use complex OR logic if we already have other operators
    if (parts.length > 0) {
      parts.push(`(name:${searchTerm} OR oracle:${searchTerm} OR type:${searchTerm})`);
    } else {
      // If no operators detected, just add the search term
      parts.push(fullTextSearch);
    }
  }
  
  return parts.join(' ').trim() || query;
}"""
        
        if old_function in content:
            content = content.replace(old_function, new_function)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Fixed multi-word search in scryfallApi.ts")
            return True
        else:
            print("❌ Could not find buildEnhancedSearchQuery function in scryfallApi.ts")
            return False
            
    except Exception as e:
        print(f"❌ Error updating scryfallApi.ts: {e}")
        return False

def add_content_hiding_css():
    """Add CSS rules to hide content when panels get very small"""
    
    file_path = "src/components/MTGOLayout.css"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # CSS rules to add at the end of the file
        new_css_rules = """

/* ===== EXTENDED PANEL RESIZING - CONTENT HIDING ===== */

/* Hide filter panel content when very narrow */
.mtgo-filter-panel {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Filter panel: Hide content when width <= 50px */
.mtgo-filter-panel[style*="width: 20px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 21px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 22px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 23px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 24px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 25px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 26px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 27px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 28px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 29px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 30px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 31px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 32px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 33px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 34px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 35px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 36px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 37px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 38px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 39px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 40px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 41px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 42px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 43px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 44px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 45px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 46px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 47px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 48px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 49px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 50px"] .panel-header h3,
.mtgo-filter-panel[style*="width: 20px"] .filter-content,
.mtgo-filter-panel[style*="width: 21px"] .filter-content,
.mtgo-filter-panel[style*="width: 22px"] .filter-content,
.mtgo-filter-panel[style*="width: 23px"] .filter-content,
.mtgo-filter-panel[style*="width: 24px"] .filter-content,
.mtgo-filter-panel[style*="width: 25px"] .filter-content,
.mtgo-filter-panel[style*="width: 26px"] .filter-content,
.mtgo-filter-panel[style*="width: 27px"] .filter-content,
.mtgo-filter-panel[style*="width: 28px"] .filter-content,
.mtgo-filter-panel[style*="width: 29px"] .filter-content,
.mtgo-filter-panel[style*="width: 30px"] .filter-content,
.mtgo-filter-panel[style*="width: 31px"] .filter-content,
.mtgo-filter-panel[style*="width: 32px"] .filter-content,
.mtgo-filter-panel[style*="width: 33px"] .filter-content,
.mtgo-filter-panel[style*="width: 34px"] .filter-content,
.mtgo-filter-panel[style*="width: 35px"] .filter-content,
.mtgo-filter-panel[style*="width: 36px"] .filter-content,
.mtgo-filter-panel[style*="width: 37px"] .filter-content,
.mtgo-filter-panel[style*="width: 38px"] .filter-content,
.mtgo-filter-panel[style*="width: 39px"] .filter-content,
.mtgo-filter-panel[style*="width: 40px"] .filter-content,
.mtgo-filter-panel[style*="width: 41px"] .filter-content,
.mtgo-filter-panel[style*="width: 42px"] .filter-content,
.mtgo-filter-panel[style*="width: 43px"] .filter-content,
.mtgo-filter-panel[style*="width: 44px"] .filter-content,
.mtgo-filter-panel[style*="width: 45px"] .filter-content,
.mtgo-filter-panel[style*="width: 46px"] .filter-content,
.mtgo-filter-panel[style*="width: 47px"] .filter-content,
.mtgo-filter-panel[style*="width: 48px"] .filter-content,
.mtgo-filter-panel[style*="width: 49px"] .filter-content,
.mtgo-filter-panel[style*="width: 50px"] .filter-content {
  display: none !important;
}

/* Show thin colored border when filter panel is very narrow */
.mtgo-filter-panel[style*="width: 20px"],
.mtgo-filter-panel[style*="width: 21px"],
.mtgo-filter-panel[style*="width: 22px"],
.mtgo-filter-panel[style*="width: 23px"],
.mtgo-filter-panel[style*="width: 24px"],
.mtgo-filter-panel[style*="width: 25px"],
.mtgo-filter-panel[style*="width: 26px"],
.mtgo-filter-panel[style*="width: 27px"],
.mtgo-filter-panel[style*="width: 28px"],
.mtgo-filter-panel[style*="width: 29px"],
.mtgo-filter-panel[style*="width: 30px"],
.mtgo-filter-panel[style*="width: 31px"],
.mtgo-filter-panel[style*="width: 32px"],
.mtgo-filter-panel[style*="width: 33px"],
.mtgo-filter-panel[style*="width: 34px"],
.mtgo-filter-panel[style*="width: 35px"],
.mtgo-filter-panel[style*="width: 36px"],
.mtgo-filter-panel[style*="width: 37px"],
.mtgo-filter-panel[style*="width: 38px"],
.mtgo-filter-panel[style*="width: 39px"],
.mtgo-filter-panel[style*="width: 40px"],
.mtgo-filter-panel[style*="width: 41px"],
.mtgo-filter-panel[style*="width: 42px"],
.mtgo-filter-panel[style*="width: 43px"],
.mtgo-filter-panel[style*="width: 44px"],
.mtgo-filter-panel[style*="width: 45px"],
.mtgo-filter-panel[style*="width: 46px"],
.mtgo-filter-panel[style*="width: 47px"],
.mtgo-filter-panel[style*="width: 48px"],
.mtgo-filter-panel[style*="width: 49px"],
.mtgo-filter-panel[style*="width: 50px"] {
  background-color: #404040;
  border-right: 3px solid #3b82f6;
}

/* Sideboard panel: Hide content when width <= 50px */
.mtgo-sideboard-panel[style*="width: 20px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 21px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 22px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 23px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 24px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 25px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 26px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 27px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 28px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 29px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 30px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 31px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 32px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 33px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 34px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 35px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 36px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 37px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 38px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 39px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 40px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 41px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 42px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 43px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 44px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 45px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 46px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 47px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 48px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 49px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 50px"] .panel-header h3,
.mtgo-sideboard-panel[style*="width: 20px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 21px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 22px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 23px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 24px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 25px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 26px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 27px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 28px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 29px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 30px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 31px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 32px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 33px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 34px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 35px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 36px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 37px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 38px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 39px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 40px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 41px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 42px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 43px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 44px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 45px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 46px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 47px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 48px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 49px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 50px"] .sideboard-controls,
.mtgo-sideboard-panel[style*="width: 20px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 21px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 22px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 23px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 24px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 25px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 26px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 27px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 28px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 29px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 30px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 31px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 32px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 33px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 34px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 35px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 36px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 37px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 38px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 39px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 40px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 41px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 42px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 43px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 44px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 45px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 46px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 47px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 48px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 49px"] .sideboard-content,
.mtgo-sideboard-panel[style*="width: 50px"] .sideboard-content {
  display: none !important;
}

/* Show thin colored border when sideboard is very narrow */
.mtgo-sideboard-panel[style*="width: 20px"],
.mtgo-sideboard-panel[style*="width: 21px"],
.mtgo-sideboard-panel[style*="width: 22px"],
.mtgo-sideboard-panel[style*="width: 23px"],
.mtgo-sideboard-panel[style*="width: 24px"],
.mtgo-sideboard-panel[style*="width: 25px"],
.mtgo-sideboard-panel[style*="width: 26px"],
.mtgo-sideboard-panel[style*="width: 27px"],
.mtgo-sideboard-panel[style*="width: 28px"],
.mtgo-sideboard-panel[style*="width: 29px"],
.mtgo-sideboard-panel[style*="width: 30px"],
.mtgo-sideboard-panel[style*="width: 31px"],
.mtgo-sideboard-panel[style*="width: 32px"],
.mtgo-sideboard-panel[style*="width: 33px"],
.mtgo-sideboard-panel[style*="width: 34px"],
.mtgo-sideboard-panel[style*="width: 35px"],
.mtgo-sideboard-panel[style*="width: 36px"],
.mtgo-sideboard-panel[style*="width: 37px"],
.mtgo-sideboard-panel[style*="width: 38px"],
.mtgo-sideboard-panel[style*="width: 39px"],
.mtgo-sideboard-panel[style*="width: 40px"],
.mtgo-sideboard-panel[style*="width: 41px"],
.mtgo-sideboard-panel[style*="width: 42px"],
.mtgo-sideboard-panel[style*="width: 43px"],
.mtgo-sideboard-panel[style*="width: 44px"],
.mtgo-sideboard-panel[style*="width: 45px"],
.mtgo-sideboard-panel[style*="width: 46px"],
.mtgo-sideboard-panel[style*="width: 47px"],
.mtgo-sideboard-panel[style*="width: 48px"],
.mtgo-sideboard-panel[style*="width: 49px"],
.mtgo-sideboard-panel[style*="width: 50px"] {
  background-color: #404040;
  border-left: 3px solid #10b981;
  border-right: none;
}

/* Deck area: Hide content when height <= 12% */
html[style*="--deck-area-height-percent: 8%"] .mtgo-bottom-area .panel-header h3,
html[style*="--deck-area-height-percent: 9%"] .mtgo-bottom-area .panel-header h3,
html[style*="--deck-area-height-percent: 10%"] .mtgo-bottom-area .panel-header h3,
html[style*="--deck-area-height-percent: 11%"] .mtgo-bottom-area .panel-header h3,
html[style*="--deck-area-height-percent: 12%"] .mtgo-bottom-area .panel-header h3,
html[style*="--deck-area-height-percent: 8%"] .mtgo-bottom-area .deck-controls,
html[style*="--deck-area-height-percent: 9%"] .mtgo-bottom-area .deck-controls,
html[style*="--deck-area-height-percent: 10%"] .mtgo-bottom-area .deck-controls,
html[style*="--deck-area-height-percent: 11%"] .mtgo-bottom-area .deck-controls,
html[style*="--deck-area-height-percent: 12%"] .mtgo-bottom-area .deck-controls,
html[style*="--deck-area-height-percent: 8%"] .mtgo-bottom-area .sideboard-controls,
html[style*="--deck-area-height-percent: 9%"] .mtgo-bottom-area .sideboard-controls,
html[style*="--deck-area-height-percent: 10%"] .mtgo-bottom-area .sideboard-controls,
html[style*="--deck-area-height-percent: 11%"] .mtgo-bottom-area .sideboard-controls,
html[style*="--deck-area-height-percent: 12%"] .mtgo-bottom-area .sideboard-controls,
html[style*="--deck-area-height-percent: 8%"] .deck-content,
html[style*="--deck-area-height-percent: 9%"] .deck-content,
html[style*="--deck-area-height-percent: 10%"] .deck-content,
html[style*="--deck-area-height-percent: 11%"] .deck-content,
html[style*="--deck-area-height-percent: 12%"] .deck-content,
html[style*="--deck-area-height-percent: 8%"] .sideboard-content,
html[style*="--deck-area-height-percent: 9%"] .sideboard-content,
html[style*="--deck-area-height-percent: 10%"] .sideboard-content,
html[style*="--deck-area-height-percent: 11%"] .sideboard-content,
html[style*="--deck-area-height-percent: 12%"] .sideboard-content {
  display: none !important;
}

/* Show thin colored border when deck area is very short */
html[style*="--deck-area-height-percent: 8%"] .mtgo-bottom-area,
html[style*="--deck-area-height-percent: 9%"] .mtgo-bottom-area,
html[style*="--deck-area-height-percent: 10%"] .mtgo-bottom-area,
html[style*="--deck-area-height-percent: 11%"] .mtgo-bottom-area,
html[style*="--deck-area-height-percent: 12%"] .mtgo-bottom-area {
  background-color: #404040;
  border-top: 3px solid #ef4444;
}

/* Enhanced resize handle visibility when panels are very small */
.mtgo-filter-panel[style*="width: 20px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 21px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 22px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 23px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 24px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 25px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 26px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 27px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 28px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 29px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 30px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 31px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 32px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 33px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 34px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 35px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 36px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 37px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 38px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 39px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 40px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 41px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 42px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 43px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 44px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 45px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 46px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 47px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 48px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 49px"] .resize-handle-right,
.mtgo-filter-panel[style*="width: 50px"] .resize-handle-right,
.mtgo-sideboard-panel[style*="width: 20px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 21px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 22px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 23px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 24px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 25px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 26px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 27px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 28px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 29px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 30px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 31px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 32px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 33px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 34px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 35px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 36px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 37px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 38px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 39px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 40px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 41px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 42px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 43px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 44px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 45px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 46px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 47px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 48px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 49px"] .resize-handle-left,
.mtgo-sideboard-panel[style*="width: 50px"] .resize-handle-left {
  background-color: rgba(59, 130, 246, 0.8) !important;
}

/* ===== END EXTENDED PANEL RESIZING ===== */
"""
        
        # Check if these rules are already present
        if "EXTENDED PANEL RESIZING" not in content:
            content += new_css_rules
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Added content hiding CSS rules to MTGOLayout.css")
            return True
        else:
            print("⚠️  Content hiding CSS rules already present in MTGOLayout.css")
            return True
            
    except Exception as e:
        print(f"❌ Error updating MTGOLayout.css: {e}")
        return False

def main():
    """Execute all quality of life fixes"""
    print("🎯 Starting Quality of Life Improvements...")
    print("=" * 60)
    
    success_count = 0
    total_operations = 3
    
    # Update useLayout constraints
    if update_useLayout_constraints():
        success_count += 1
    
    # Fix multi-word search
    if fix_multi_word_search():
        success_count += 1
    
    # Add CSS content hiding rules
    if add_content_hiding_css():
        success_count += 1
    
    print("=" * 60)
    if success_count == total_operations:
        print("🎉 Quality of Life Improvements COMPLETE!")
        print("\n✅ PANEL RESIZING ENHANCEMENTS:")
        print("   • Filter panel: Now resizes down to 20px (thin blue border)")
        print("   • Sideboard: Now resizes down to 20px (thin green border)")  
        print("   • Deck area: Now resizes down to 8% of screen height (thin red border)")
        print("   • Content automatically hides when panels get very small")
        print("   • Resize handles remain visible for easy expansion")
        print("\n✅ MULTI-WORD SEARCH FIXES:")
        print("   • 'Lightning Bolt' → searches for exact phrase in names, text & types")
        print("   • '\"Lightning Bolt\"' → explicit quoted phrase search")  
        print("   • 'lightning bolt' → case insensitive phrase search")
        print("   • Single words still work normally without quotes")
        print("   • Improved operator parsing (-, :, field searches)")
        print("\n🎮 USAGE:")
        print("   • Drag resize handles to make panels near-invisible")
        print("   • Search multi-word card names normally")
        print("   • Use quotes for exact phrase matching")
        print("   • Panels show as colored borders when minimized")
        print("\n🚀 Ready to test enhanced panel resizing and multi-word search!")
    else:
        print(f"❌ Quality of Life Improvements FAILED: {success_count}/{total_operations} operations successful")
        print("   Please check error messages above and retry.")

if __name__ == "__main__":
    main()
