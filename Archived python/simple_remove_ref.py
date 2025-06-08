#!/usr/bin/env python3
"""
Simple fix: Remove the problematic ref that's causing compilation error
"""

import re

# Read the MTGOLayout.tsx file
with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the ref line that's causing the error
content = re.sub(r'\s*ref=\{scrollContainerRef\}\s*\n', '\n', content)

# Also remove any scroll preservation logic that was added incorrectly
content = re.sub(r'// Preserve scroll position during Load More operations.*?}, \[pagination\.isLoadingMore, savedScrollPosition\]\);', '', content, flags=re.DOTALL)

# Remove any ref declarations that were added
content = re.sub(r'const scrollContainerRef = useRef<HTMLDivElement>\(null\);\s*', '', content)
content = re.sub(r'const \[savedScrollPosition, setSavedScrollPosition\] = useState<number>\(0\);\s*', '', content)

# Write the updated content back
with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Removed problematic ref and scroll logic")
print("Load More should work now, but will still reset scroll position.")
print("We can add proper scroll preservation later once the basic functionality is working.")
