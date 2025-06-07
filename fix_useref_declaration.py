#!/usr/bin/env python3
"""
Fix the missing useRef declaration in MTGOLayout.tsx
"""

import re

# Read the MTGOLayout.tsx file
with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the existing useEffect where we added scroll logic and add the ref declarations before it
# Look for the scroll preservation logic we added and add the ref declarations before it

pattern = r'(// Preserve scroll position during Load More operations\s+const scrollContainerRef = useRef<HTMLDivElement>\(null\);)'

# If this pattern exists, it means the ref is already declared, so we just need to check if it's properly imported
if re.search(pattern, content):
    print("✅ useRef declaration already exists")
else:
    # Add the ref declarations right after the existing useEffect for popular cards
    useEffect_pattern = r'(// Load popular cards on mount\s+useEffect\(\(\) => \{\s+loadPopularCards\(\);\s+\}, \[loadPopularCards\]\);)'
    
    ref_addition = r'''\1

  // Refs for scroll position preservation
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [savedScrollPosition, setSavedScrollPosition] = useState<number>(0);'''
    
    content = re.sub(useEffect_pattern, ref_addition, content)
    print("✅ Added useRef declaration")

# Ensure useRef is in the React import
if 'useRef' not in content.split('\n')[0]:
    # Find the React import line and add useRef if it's missing
    react_import_pattern = r'import React, \{ ([^}]+) \} from \'react\';'
    
    def add_useref_to_import(match):
        imports = match.group(1)
        if 'useRef' not in imports:
            return f"import React, {{ {imports}, useRef }} from 'react';"
        return match.group(0)
    
    content = re.sub(react_import_pattern, add_useref_to_import, content)
    print("✅ Added useRef to React imports")

# Now add the useEffect logic if it doesn't exist
scroll_logic_pattern = r'// Preserve scroll position during Load More operations'

if not re.search(scroll_logic_pattern, content):
    # Add the scroll preservation useEffects
    ref_pattern = r'(const scrollContainerRef = useRef<HTMLDivElement>\(null\);\s+const \[savedScrollPosition, setSavedScrollPosition\] = useState<number>\(0\);)'
    
    scroll_effects = r'''\1

  // Preserve scroll position during Load More operations
  useEffect(() => {
    const scrollContainer = scrollContainerRef.current?.closest('.mtgo-collection-area');
    if (scrollContainer && pagination.isLoadingMore) {
      // Save current scroll position when Load More starts
      setSavedScrollPosition(scrollContainer.scrollTop);
    }
  }, [pagination.isLoadingMore]);

  useEffect(() => {
    const scrollContainer = scrollContainerRef.current?.closest('.mtgo-collection-area');
    if (scrollContainer && savedScrollPosition > 0 && !pagination.isLoadingMore) {
      // Restore scroll position after Load More completes
      setTimeout(() => {
        scrollContainer.scrollTop = savedScrollPosition;
        setSavedScrollPosition(0);
      }, 50); // Small delay to ensure DOM is updated
    }
  }, [pagination.isLoadingMore, savedScrollPosition]);'''
    
    content = re.sub(ref_pattern, scroll_effects, content)
    print("✅ Added scroll preservation useEffect logic")

# Write the updated content back
with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed useRef declaration and scroll preservation")
print("The scrollContainerRef should now be properly declared and available.")
