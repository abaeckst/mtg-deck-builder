#!/usr/bin/env python3

import os

def fix_use_search_interface():
    """Fix the broken interface in useSearch.ts"""
    
    file_path = r"C:\Users\abaec\Development\mtg-deck-builder\src\hooks\useSearch.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    
    print("🔧 FIXING broken interface in useSearch.ts...")
    
    # Find and replace the broken interface section
    broken_interface_start = content.find("interface UseSearchProps {")
    if broken_interface_start == -1:
        print("❌ Could not find UseSearchProps interface")
        return False
    
    # Find the end of the broken interface
    broken_interface_end = content.find("export const useSearch = ({", broken_interface_start)
    if broken_interface_end == -1:
        print("❌ Could not find end of interface")
        return False
    
    # Extract the parts before and after the broken interface
    before_interface = content[:broken_interface_start]
    after_interface = content[broken_interface_end:]
    
    # Create the correct interface
    correct_interface = """interface UseSearchProps {
  activeFilters: FilterState;
  hasActiveFilters: () => boolean;
  onPaginationStateChange: (state: PaginatedSearchState | null) => void;
  onPaginationUpdate: (update: Partial<{
    totalCards: number;
    loadedCards: number;
    hasMore: boolean;
    isLoadingMore: boolean;
    currentPage: number;
  }>) => void;
  resetPagination: () => void;
  addToSearchHistory: (query: string) => void;
  // ADDED: Get default sort parameters from useSorting
  getCollectionSortParams: () => { order: string; dir: 'asc' | 'desc' };
}

"""
    
    # Reconstruct the file
    fixed_content = before_interface + correct_interface + after_interface
    
    # Also fix the hook parameter destructuring if it's broken
    if "getCollectionSortParams" not in after_interface:
        # Fix the export const useSearch parameters
        hook_start = fixed_content.find("export const useSearch = ({")
        if hook_start != -1:
            hook_end = fixed_content.find("}: UseSearchProps)", hook_start)
            if hook_end != -1:
                before_hook = fixed_content[:hook_start]
                after_hook_params = fixed_content[hook_end:]
                
                correct_hook_params = """export const useSearch = ({
  activeFilters,
  hasActiveFilters,
  onPaginationStateChange,
  onPaginationUpdate,
  resetPagination,
  addToSearchHistory,
  getCollectionSortParams
"""
                
                fixed_content = before_hook + correct_hook_params + after_hook_params
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print("✅ useSearch.ts interface fixed successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to write useSearch.ts: {e}")
        return False

def main():
    print("🔧 FIXING BROKEN TYPESCRIPT INTERFACE")
    print("=" * 50)
    
    success = fix_use_search_interface()
    
    if success:
        print("\n✅ SYNTAX ERROR FIXED!")
        print("🎯 Next step: Update the searchWithPagination function")
        print("The interface is now correct, but we still need to update the function logic.")
    else:
        print("\n❌ COULD NOT FIX AUTOMATICALLY")
        print("Please check the file manually")

if __name__ == "__main__":
    main()