#!/usr/bin/env python3
"""
Fix Load More scroll position reset issue - preserve user's scroll position
"""

import re

# Read the MTGOLayout.tsx file
with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the key prop that's causing the scroll reset
# and replace it with a more targeted solution
pattern = r'key=\{`collection-grid-\$\{cards\.length\}`\}\s*'
content = re.sub(pattern, '', content)

# Add a useEffect to handle scroll position preservation during Load More
useEffect_pattern = r'(// Load popular cards on mount\s*useEffect\(\(\) => \{\s*loadPopularCards\(\);\s*\}, \[loadPopularCards\]\);)'

useEffect_addition = r'''\1

  // Preserve scroll position during Load More operations
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [savedScrollPosition, setSavedScrollPosition] = useState<number>(0);

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

content = re.sub(useEffect_pattern, useEffect_addition, content)

# Add the ref to the collection grid div
grid_pattern = r'(<div\s+className="collection-grid"\s+style=\{\{)'
grid_replacement = r'<div\n                ref={scrollContainerRef}\n                className="collection-grid"\n                style={{'

content = re.sub(grid_pattern, grid_replacement, content)

# Add the necessary imports at the top
import_pattern = r'(import React, \{ useState, useCallback, useEffect, useRef, useMemo \} from \'react\';)'
import_replacement = r'import React, { useState, useCallback, useEffect, useRef, useMemo } from \'react\';'

# Check if useRef is already imported, if not add it
if 'useRef' not in content:
    content = re.sub(r'(import React, \{ [^}]+ \} from \'react\';)', 
                     lambda m: m.group(1).replace('}', ', useRef }'), content)

# Write the updated content back
with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed scroll position preservation for Load More")
print("Changes made:")
print("1. Removed the key prop that was causing full grid re-render")
print("2. Added useRef and scroll position preservation logic")
print("3. Added ref to collection-grid div")
print("4. Scroll position is now saved before Load More and restored after")
print("\nLoad More should now work without resetting scroll position!")
