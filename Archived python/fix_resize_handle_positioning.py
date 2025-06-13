#!/usr/bin/env python3
"""
Fix resize handle positioning by ensuring parent container has position: relative
"""

# Read MTGOLayout.css
with open('src/components/MTGOLayout.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: Ensure filter panel has position: relative so resize handle positions correctly
# Find the .mtgo-filter-panel rule and add position: relative if it's missing
if 'position: relative' not in content.split('.mtgo-filter-panel')[1].split('}')[0]:
    content = content.replace(
        '.mtgo-filter-panel {',
        '.mtgo-filter-panel {\n  position: relative;'
    )

# Also ensure the main content area has position: relative
if '.mtgo-main-content {' in content and 'position: relative' not in content.split('.mtgo-main-content')[1].split('}')[0]:
    content = content.replace(
        '.mtgo-main-content {',
        '.mtgo-main-content {\n  position: relative;'
    )

# Write the updated file
with open('src/components/MTGOLayout.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed resize handle positioning by adding position: relative to parent containers")
print("✅ Filter panel resize handle should now appear on the right edge of the filter panel")
print("✅ Resize handles should now be positioned correctly relative to their parent containers")

# Read MTGOLayout.tsx to check if we need to move the resize handle inside the filter panel
with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
    tsx_content = f.read()

print("\n📋 Next steps:")
print("1. Run this script to fix the CSS positioning")
print("2. Refresh your browser")
print("3. The red line should now appear on the right edge of the filter panel instead of the screen edge")
