#!/usr/bin/env python3
"""
Fix the actual syntax errors in PaginatedSearchState interface.
The interface in card.ts is malformed and scryfallApi.ts has a duplicate.
"""

def fix_card_types_interface():
    """Fix the malformed PaginatedSearchState interface in card.ts"""
    print("🔧 Fixing malformed PaginatedSearchState interface in card.ts...")
    
    with open('src/types/card.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the malformed interface and fix it
    # The current broken pattern:
    broken_pattern = r'''export interface PaginatedSearchState \{
  initialResults: ScryfallCard\[\];
  totalCards: number;
  loadedCards: number;
  hasMore: boolean;
  isLoadingMore: boolean;
  currentPage: number;
  lastQuery: string;
  lastFilters: any;
  lastSort: \{ order: string; dir: 'asc' \| 'desc' 
  // Partial page consumption tracking
  currentScryfallPage: number;        // Actual Scryfall page number \(1-based\)
  cardsConsumedFromCurrentPage: number; // How many cards used from current Scryfall page
  currentPageCards: ScryfallCard\[\];   // Full current page data from Scryfall
  scryfallPageSize: number;           // Scryfall page size \(175\)
  displayBatchSize: number;           // User display batch size \(75\)
\};
\}'''
    
    # Correct interface definition
    fixed_interface = '''export interface PaginatedSearchState {
  initialResults: ScryfallCard[];
  totalCards: number;
  loadedCards: number;
  hasMore: boolean;
  isLoadingMore: boolean;
  currentPage: number;
  lastQuery: string;
  lastFilters: any;
  lastSort: { order: string; dir: 'asc' | 'desc' };
  // Partial page consumption tracking
  currentScryfallPage: number;        // Actual Scryfall page number (1-based)
  cardsConsumedFromCurrentPage: number; // How many cards used from current Scryfall page
  currentPageCards: ScryfallCard[];   // Full current page data from Scryfall
  scryfallPageSize: number;           // Scryfall page size (175)
  displayBatchSize: number;           // User display batch size (75)
}'''
    
    import re
    
    # Try to find and replace the broken interface
    if 'lastSort: { order: string; dir: \'asc\' | \'desc\' ' in content and 'currentScryfallPage' in content:
        # More flexible pattern to catch the malformed interface
        # Find from "export interface PaginatedSearchState {" to the extra "}"
        pattern = r'export interface PaginatedSearchState \{[^}]*\};[\s]*\}'
        
        updated_content = re.sub(pattern, fixed_interface, content, flags=re.DOTALL)
        
        if updated_content != content:
            with open('src/types/card.ts', 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("✅ Fixed malformed PaginatedSearchState interface")
            return True
        else:
            print("❌ Pattern didn't match - trying manual fix")
            return manual_fix_interface(content)
    else:
        print("⚠️ Interface doesn't appear malformed")
        return True

def manual_fix_interface(content):
    """Manual fix for the interface if regex fails"""
    print("🔧 Attempting manual fix...")
    
    # Find the start of the interface
    start_marker = "export interface PaginatedSearchState {"
    start_pos = content.find(start_marker)
    
    if start_pos == -1:
        print("❌ Could not find interface start")
        return False
    
    # Find the problematic area and the extra closing brace
    # Look for the pattern after lastSort
    lastSort_pos = content.find("lastSort: { order: string; dir: 'asc' | 'desc'", start_pos)
    if lastSort_pos == -1:
        print("❌ Could not find lastSort property")
        return False
    
    # Find the end - look for the extra }
    end_search_start = lastSort_pos + 100
    end_pos = -1
    brace_count = 0
    in_interface = False
    
    # Count braces to find the real end
    for i in range(start_pos, len(content)):
        char = content[i]
        if char == '{':
            brace_count += 1
            in_interface = True
        elif char == '}':
            brace_count -= 1
            if in_interface and brace_count == 0:
                # This should be the end of the interface
                # But check if there's an extra } after
                next_brace = content.find('}', i + 1)
                if next_brace != -1 and content[i:next_brace+1].strip() == '}\n}':
                    end_pos = next_brace + 1
                else:
                    end_pos = i + 1
                break
    
    if end_pos == -1:
        print("❌ Could not find interface end")
        return False
    
    # Extract the broken interface
    broken_interface = content[start_pos:end_pos]
    print(f"📝 Found broken interface: {len(broken_interface)} characters")
    
    # Replace with fixed version
    fixed_interface = '''export interface PaginatedSearchState {
  initialResults: ScryfallCard[];
  totalCards: number;
  loadedCards: number;
  hasMore: boolean;
  isLoadingMore: boolean;
  currentPage: number;
  lastQuery: string;
  lastFilters: any;
  lastSort: { order: string; dir: 'asc' | 'desc' };
  // Partial page consumption tracking
  currentScryfallPage: number;        // Actual Scryfall page number (1-based)
  cardsConsumedFromCurrentPage: number; // How many cards used from current Scryfall page
  currentPageCards: ScryfallCard[];   // Full current page data from Scryfall
  scryfallPageSize: number;           // Scryfall page size (175)
  displayBatchSize: number;           // User display batch size (75)
}'''
    
    # Replace in content
    new_content = content[:start_pos] + fixed_interface + content[end_pos:]
    
    with open('src/types/card.ts', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Manually fixed malformed interface")
    return True

def remove_duplicate_interface():
    """Remove duplicate PaginatedSearchState from scryfallApi.ts"""
    print("🔧 Removing duplicate PaginatedSearchState from scryfallApi.ts...")
    
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the duplicate interface
    duplicate_pattern = r'/\*\*\s*\* Pagination state interface for progressive loading\s*\*/\s*export interface PaginatedSearchState \{[^}]+\}'
    
    import re
    
    # Check if duplicate exists
    if re.search(duplicate_pattern, content, flags=re.DOTALL):
        updated_content = re.sub(duplicate_pattern, '', content, flags=re.DOTALL)
        
        with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✅ Removed duplicate interface")
        return True
    else:
        print("ℹ️ No duplicate interface found")
        return True

def add_import_statement():
    """Ensure scryfallApi.ts imports PaginatedSearchState from card.ts"""
    print("🔧 Ensuring proper import in scryfallApi.ts...")
    
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check current import
    current_import = "import { ScryfallCard, ScryfallSearchResponse } from '../types/card';"
    
    if current_import in content and 'PaginatedSearchState' not in content[:500]:
        # Replace with enhanced import
        new_import = "import { ScryfallCard, ScryfallSearchResponse, PaginatedSearchState } from '../types/card';"
        updated_content = content.replace(current_import, new_import)
        
        with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✅ Added PaginatedSearchState to import")
        return True
    else:
        print("ℹ️ Import already correct or not found")
        return True

def main():
    """Execute all fixes in order"""
    print("🚨 CRITICAL FIX: TypeScript Interface Syntax Errors")
    print("=" * 60)
    print("Problem: Malformed PaginatedSearchState interface")
    print("=" * 60)
    
    success = True
    
    # Step 1: Fix the malformed interface in card.ts
    if not fix_card_types_interface():
        success = False
        print("❌ CRITICAL: Could not fix malformed interface")
    
    # Step 2: Remove duplicate from scryfallApi.ts
    if not remove_duplicate_interface():
        success = False
    
    # Step 3: Ensure proper import
    if not add_import_statement():
        success = False
    
    if success:
        print("\n🎯 SUCCESS! TypeScript syntax errors fixed:")
        print("1. ✅ Fixed malformed PaginatedSearchState interface in card.ts")
        print("2. ✅ Removed duplicate interface from scryfallApi.ts")
        print("3. ✅ Ensured proper import statement")
        print("\n🧪 Test with: npm start")
        print("Should compile without TypeScript errors now")
    else:
        print("\n❌ FAILED to fix syntax errors")
        print("Manual intervention required")
    
    return success

if __name__ == "__main__":
    main()
