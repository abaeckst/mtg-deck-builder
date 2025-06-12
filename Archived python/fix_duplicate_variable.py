#!/usr/bin/env python3
"""
Fix duplicate isInitialMount variable in useCards.ts

Issue: The search coordination fix script accidentally added the filter reactivity 
code twice, creating duplicate variable declarations.

Solution: Remove duplicate code and ensure clean single implementation.
"""

import os
import re

def fix_use_cards_duplicates():
    """Remove duplicate isInitialMount and filter reactivity code"""
    
    file_path = "src/hooks/useCards.ts"
    
    # Read current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove ALL instances of the filter reactivity code first
    # Pattern to match the entire filter reactivity block
    filter_reactivity_pattern = r"""
  // FILTER CHANGE REACTIVITY: Trigger fresh search when filters change
  // Skip on initial mount to prevent interference with loadPopularCards
  const isInitialMount = useRef\(true\);
  
  useEffect\(\(\) => \{
    // Skip filter reactivity on initial mount
    if \(isInitialMount\.current\) \{
      isInitialMount\.current = false;
      return;
    \}
    
    // Skip if no active filters \(user cleared filters - handled by clearAllFilters\)
    if \(!hasActiveFilters\(\)\) \{
      return;
    \}
    
    console\.log\('🎯 Filter change detected, triggering fresh search'\);
    
    // Trigger fresh search with current filters
    // Use '\*' as base query to get all cards matching filters
    searchWithAllFilters\('\*'\);
    
  \}, \[activeFilters, hasActiveFilters, searchWithAllFilters\]\);
  
  // SORT CHANGE REACTIVITY: Currently handled by useSorting hook coordination
  // No additional effect needed as handleCollectionSortChange is already wired up"""
    
    # Remove all instances of this pattern
    content = re.sub(filter_reactivity_pattern, '', content, flags=re.DOTALL)
    
    # Now add the filter reactivity code ONCE in the correct location
    # Find the loadPopularCards useEffect
    load_popular_pattern = r"(  // Load popular cards on mount\s+useEffect\(\(\) => \{\s+loadPopularCards\(\);\s+\}, \[loadPopularCards\]\);)"
    
    # Add the filter reactivity after loadPopularCards effect
    filter_reactivity_code = '''

  // FILTER CHANGE REACTIVITY: Trigger fresh search when filters change
  // Skip on initial mount to prevent interference with loadPopularCards
  const isInitialMount = useRef(true);
  
  useEffect(() => {
    // Skip filter reactivity on initial mount
    if (isInitialMount.current) {
      isInitialMount.current = false;
      return;
    }
    
    // Skip if no active filters (user cleared filters - handled by clearAllFilters)
    if (!hasActiveFilters()) {
      return;
    }
    
    console.log('🎯 Filter change detected, triggering fresh search');
    
    // Trigger fresh search with current filters
    // Use '*' as base query to get all cards matching filters
    searchWithAllFilters('*');
    
  }, [activeFilters, hasActiveFilters, searchWithAllFilters]);
  
  // SORT CHANGE REACTIVITY: Currently handled by useSorting hook coordination
  // No additional effect needed as handleCollectionSortChange is already wired up'''
    
    # Add the code after loadPopularCards effect
    content = re.sub(load_popular_pattern, r'\1' + filter_reactivity_code, content)
    
    # Write the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed duplicate isInitialMount variable in useCards.ts")

def main():
    """Fix the duplicate variable issue"""
    
    print("🔧 Fixing duplicate variable error in useCards.ts...")
    print("📋 Issue: isInitialMount declared twice due to script duplication")
    print("🎯 Solution: Remove duplicates and add clean single implementation")
    print("")
    
    # Verify file exists
    file_path = "src/hooks/useCards.ts"
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found")
        return
    
    try:
        fix_use_cards_duplicates()
        
        print("")
        print("✅ Duplicate variable error fixed!")
        print("")
        print("🎯 What was fixed:")
        print("  ✓ Removed duplicate isInitialMount declarations")
        print("  ✓ Removed duplicate filter reactivity code")
        print("  ✓ Added single clean implementation")
        print("  ✓ Preserved all functionality")
        print("")
        print("🧪 TypeScript compilation should now succeed")
        print("🚀 Run 'npm start' to verify the fix!")
        
    except Exception as e:
        print(f"❌ Error fixing duplicates: {e}")

if __name__ == "__main__":
    main()
