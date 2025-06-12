#!/usr/bin/env python3
"""
Add precise timing measurements to scryfallApi.ts for performance debugging
"""

import os
import re

def add_timing_to_scryfall_api():
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        print("Make sure you're running this from the mtg-deck-builder directory")
        return False
    
    print(f"Reading {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if timing is already added
    if '⏱️ TOTAL_SEARCH_TIME' in content:
        print("Performance timing already exists!")
        return True
    
    # Add timing to rateLimitedFetch function
    pattern1 = r'(const rateLimitedFetch = async \(url: string\): Promise<Response> => \{)'
    replacement1 = r'\1\n  console.time("⏱️ API_REQUEST_TIME");'
    
    if re.search(pattern1, content):
        content = re.sub(pattern1, replacement1, content)
        print("✅ Added timing start to rateLimitedFetch")
    
    # Add timing end to rateLimitedFetch (before return)
    pattern2 = r'(\s+)(return response;)(\s+\};)'
    replacement2 = r'\1console.timeEnd("⏱️ API_REQUEST_TIME");\n\1\2\3'
    
    if re.search(pattern2, content):
        content = re.sub(pattern2, replacement2, content)
        print("✅ Added timing end to rateLimitedFetch")
    
    # Add overall timing to searchCards function
    pattern3 = r'(export const searchCards = async \([^)]+\): Promise<ScryfallSearchResponse> => \{\s+try \{)'
    replacement3 = r'\1\n    console.time("⏱️ TOTAL_SEARCH_TIME");\n    console.log("🔍 Search started:", { query, order, dir });'
    
    if re.search(pattern3, content, re.DOTALL):
        content = re.sub(pattern3, replacement3, content, flags=re.DOTALL)
        print("✅ Added overall timing start to searchCards")
    
    # Add timing end before return in searchCards
    pattern4 = r'(\s+)(return data as ScryfallSearchResponse;)(\s+\} catch)'
    replacement4 = r'\1console.timeEnd("⏱️ TOTAL_SEARCH_TIME");\n\1console.log("✅ Search completed successfully");\n\1\2\3'
    
    if re.search(pattern4, content):
        content = re.sub(pattern4, replacement4, content)
        print("✅ Added overall timing end to searchCards")
    
    # Add timing to buildEnhancedSearchQuery function
    pattern5 = r'(function buildEnhancedSearchQuery\(query: string\): string \{)'
    replacement5 = r'\1\n  console.time("⏱️ QUERY_BUILDING_TIME");'
    
    if re.search(pattern5, content):
        content = re.sub(pattern5, replacement5, content)
        print("✅ Added query building timing start")
    
    # Add timing end to buildEnhancedSearchQuery (before return)
    pattern6 = r'(\s+)(console\.log\(\'🔍 ENHANCED QUERY RESULT:\',[\s\S]*?\);)(\s+return result;)'
    replacement6 = r'\1\2\n  console.timeEnd("⏱️ QUERY_BUILDING_TIME");\3'
    
    if re.search(pattern6, content, re.DOTALL):
        content = re.sub(pattern6, replacement6, content, flags=re.DOTALL)
        print("✅ Added query building timing end")
    
    # Add JSON parsing timing
    pattern7 = r'(\s+)(const data = await response\.json\(\);)'
    replacement7 = r'\1console.time("⏱️ JSON_PARSING_TIME");\n\1\2\n\1console.timeEnd("⏱️ JSON_PARSING_TIME");'
    
    if re.search(pattern7, content):
        content = re.sub(pattern7, replacement7, content)
        print("✅ Added JSON parsing timing")
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Successfully added performance timing to {file_path}")
    print("\nNow run your search and check the browser console for timing results!")
    print("\nLook for these timing measurements:")
    print("- ⏱️ QUERY_BUILDING_TIME (should be ~1ms)")
    print("- ⏱️ API_REQUEST_TIME (network time to Scryfall)")
    print("- ⏱️ JSON_PARSING_TIME (should be ~1-5ms)")
    print("- ⏱️ TOTAL_SEARCH_TIME (overall time)")
    
    return True

if __name__ == "__main__":
    print("Adding performance timing to scryfallApi.ts...")
    print("=" * 50)
    
    success = add_timing_to_scryfall_api()
    
    if success:
        print("\n" + "=" * 50)
        print("NEXT STEPS:")
        print("1. Open your app in browser")
        print("2. Open DevTools (F12) → Console tab")
        print("3. Search for 'fear of missin'")
        print("4. Check the timing results in console")
        print("5. Report back what you see!")
    else:
        print("❌ Failed to add timing. Check the error messages above.")
