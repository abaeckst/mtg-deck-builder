#!/usr/bin/env python3
"""
Fix FlipCard rendering issue - cards appearing as wireframes instead of actual cards
The FlipCard wrapper is breaking normal card rendering for single-faced cards
"""

import os

def fix_flipcard_rendering():
    filepath = "src/components/DraggableCard.tsx"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    # Read current content
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    backup_path = f"{filepath}.backup_flipcard_fix"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Backup created: {backup_path}")
    
    # Find the FlipCard import and usage
    old_render_section = '''      {/* ENHANCED: FlipCard wrapper with 3D flip animation */}
      <FlipCard
        card={cardForFlipCard}
        size={size}
        scaleFactor={scaleFactor}
        showQuantity={showQuantity}
        quantity={quantity}
        availableQuantity={availableQuantity}
        selected={selected}
        selectable={selectable}
        disabled={disabled}
        // Pass through all interactions to FlipCard
        onClick={onClick}
        onDoubleClick={onDoubleClick}
      />'''
    
    # Create conditional rendering - only use FlipCard for actual double-faced cards
    new_render_section = '''      {/* CONDITIONAL: FlipCard only for double-faced cards, MagicCard for others */}
      {(() => {
        // Check if this is actually a double-faced card
        const isActuallyDoubleFaced = 'card_faces' in cardForFlipCard && 
                                     cardForFlipCard.card_faces && 
                                     Array.isArray(cardForFlipCard.card_faces) && 
                                     cardForFlipCard.card_faces.length >= 2;
        
        if (isActuallyDoubleFaced) {
          // Use FlipCard for actual double-faced cards
          return (
            <FlipCard
              card={cardForFlipCard}
              size={size}
              scaleFactor={scaleFactor}
              showQuantity={showQuantity}
              quantity={quantity}
              availableQuantity={availableQuantity}
              selected={selected}
              selectable={selectable}
              disabled={disabled}
              onClick={onClick}
              onDoubleClick={onDoubleClick}
            />
          );
        } else {
          // Use MagicCard directly for single-faced cards
          return (
            <MagicCard
              card={cardForFlipCard}
              size={size}
              scaleFactor={scaleFactor}
              showQuantity={showQuantity}
              quantity={quantity}
              availableQuantity={availableQuantity}
              selected={selected}
              selectable={selectable}
              disabled={disabled}
              onClick={onClick}
              onDoubleClick={onDoubleClick}
            />
          );
        }
      })()}'''
    
    # Add MagicCard import if not present
    if 'import MagicCard from' not in content:
        # Find the FlipCard import line and add MagicCard import
        import_line = "import FlipCard from './FlipCard';"
        if import_line in content:
            new_imports = """import FlipCard from './FlipCard';
import MagicCard from './MagicCard';"""
            content = content.replace(import_line, new_imports)
            print("✅ Added MagicCard import")
    
    # Replace the rendering section
    if old_render_section in content:
        content = content.replace(old_render_section, new_render_section)
        print("✅ Fixed FlipCard conditional rendering")
    else:
        print("⚠️ Could not find exact render section, trying alternative approach")
        # Try to find and replace just the FlipCard usage
        if '<FlipCard' in content and 'cardForFlipCard' in content:
            # This is a more complex replacement, but let's try a targeted fix
            lines = content.split('\n')
            new_lines = []
            in_flipcard_section = False
            flipcard_lines = []
            
            for line in lines:
                if '<FlipCard' in line:
                    in_flipcard_section = True
                    flipcard_lines = [line]
                elif in_flipcard_section:
                    flipcard_lines.append(line)
                    if '/>' in line or '</FlipCard>' in line:
                        # End of FlipCard section, replace it
                        new_lines.append('      {/* CONDITIONAL: FlipCard only for double-faced cards, MagicCard for others */}')
                        new_lines.append('      {(() => {')
                        new_lines.append('        const isActuallyDoubleFaced = \'card_faces\' in cardForFlipCard && ')
                        new_lines.append('                                     cardForFlipCard.card_faces && ')
                        new_lines.append('                                     Array.isArray(cardForFlipCard.card_faces) && ')
                        new_lines.append('                                     cardForFlipCard.card_faces.length >= 2;')
                        new_lines.append('        ')
                        new_lines.append('        if (isActuallyDoubleFaced) {')
                        new_lines.append('          return (')
                        for flip_line in flipcard_lines:
                            new_lines.append('            ' + flip_line)
                        new_lines.append('          );')
                        new_lines.append('        } else {')
                        new_lines.append('          return (')
                        # Convert FlipCard to MagicCard
                        for flip_line in flipcard_lines:
                            magic_line = flip_line.replace('<FlipCard', '<MagicCard').replace('</FlipCard>', '</MagicCard>')
                            new_lines.append('            ' + magic_line)
                        new_lines.append('          );')
                        new_lines.append('        }')
                        new_lines.append('      })()}')
                        in_flipcard_section = False
                        flipcard_lines = []
                else:
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
            print("✅ Applied alternative FlipCard fix")
    
    # Write the updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ FlipCard rendering issue fixed")
    print("🎯 Single-faced cards now use MagicCard directly")
    print("🎪 Double-faced cards still use FlipCard with 3D animation")
    print("🔄 Restart the app to see normal card rendering")
    
    return True

if __name__ == "__main__":
    success = fix_flipcard_rendering()
    if success:
        print("\n🎉 FlipCard rendering issue fixed!")
        print("📋 Changes made:")
        print("   - Single-faced cards now render with MagicCard directly")
        print("   - Double-faced cards still use FlipCard for 3D flip animation")
        print("   - Cards should now display properly instead of wireframes")
        print("\n💡 This preserves flip functionality for double-faced cards")
        print("   while fixing the rendering issue for normal cards")
    else:
        print("\n❌ Failed to fix FlipCard rendering issue")
