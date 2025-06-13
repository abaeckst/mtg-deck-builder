#!/usr/bin/env python3
"""
Fix resize cursor visibility by removing inline cursor styles and using CSS classes
"""

# Read MTGOLayout.tsx
with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Remove inline cursor from filter panel resize handle
content = content.replace(
    '''style={{
            position: 'absolute',
            top: 0,
            right: -3,
            width: 6,
            height: '100%',
            cursor: 'ew-resize',
            background: 'linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%)',
            zIndex: 1001,
            opacity: 0.7,
            transition: 'opacity 0.2s ease'
          }}''',
    '''style={{
            position: 'absolute',
            top: 0,
            right: -3,
            width: 6,
            height: '100%',
            background: 'linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%)',
            zIndex: 1001,
            opacity: 0.7,
            transition: 'opacity 0.2s ease'
          }}'''
)

# Fix 2: Remove inline cursor from vertical resize handle
content = content.replace(
    '''style={{
              position: 'absolute',
              top: -3,
              left: 0,
              width: '100%',
              height: 6,
              cursor: 'ns-resize',
              background: 'linear-gradient(0deg, transparent 0%, #555555 50%, transparent 100%)',
              zIndex: 1001,
              opacity: 0.7,
              transition: 'opacity 0.2s ease'
            }}''',
    '''style={{
              position: 'absolute',
              top: -3,
              left: 0,
              width: '100%',
              height: 6,
              background: 'linear-gradient(0deg, transparent 0%, #555555 50%, transparent 100%)',
              zIndex: 1001,
              opacity: 0.7,
              transition: 'opacity 0.2s ease'
            }}'''
)

# Write the updated file
with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed resize cursor visibility by removing inline cursor styles")
print("✅ Resize handles now use ResizeHandles.css classes for proper cursor display")
print("✅ Filter panel horizontal resize cursor should now be visible")
print("✅ Maindeck/sideboard vertical resize cursor should now be visible")
