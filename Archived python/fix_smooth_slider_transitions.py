#!/usr/bin/env python3
"""
Fix Smooth Slider Transitions - Add CSS transitions to eliminate card jumping
Makes slider adjustments feel smooth and professional
"""

def fix_magic_card_transitions():
    file_path = "src/components/MagicCard.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Reading MagicCard.tsx")
        
        # Fix the card container styles to include smooth transitions
        old_card_styles = """  const cardStyles: React.CSSProperties = {
    ...sizeStyles,
    ...style,
    position: 'relative',
    borderRadius: '8px',
    border: `2px solid ${selected ? '#3b82f6' : rarityColor}`,
    backgroundColor: '#1a1a1a',
    cursor: selectable || onClick ? 'pointer' : 'default',
    opacity: disabled ? 0.5 : 1,
    transition: 'all 0.2s ease-in-out',
    overflow: 'hidden',
    boxShadow: selected 
      ? '0 0 0 2px #3b82f6, 0 4px 8px rgba(0,0,0,0.3)' 
      : '0 2px 4px rgba(0,0,0,0.3)',
  };"""
        
        new_card_styles = """  const cardStyles: React.CSSProperties = {
    ...sizeStyles,
    ...style,
    position: 'relative',
    borderRadius: '8px',
    border: `2px solid ${selected ? '#3b82f6' : rarityColor}`,
    backgroundColor: '#1a1a1a',
    cursor: selectable || onClick ? 'pointer' : 'default',
    opacity: disabled ? 0.5 : 1,
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    overflow: 'hidden',
    boxShadow: selected 
      ? '0 0 0 2px #3b82f6, 0 4px 8px rgba(0,0,0,0.3)' 
      : '0 2px 4px rgba(0,0,0,0.3)',
  };"""
        
        if old_card_styles in content:
            content = content.replace(old_card_styles, new_card_styles)
            print("✅ Enhanced card transition timing in MagicCard.tsx")
        else:
            print("⚠️  Card styles in MagicCard.tsx not found in expected format")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"❌ Error fixing MagicCard.tsx: {str(e)}")
        return False

def fix_css_grid_transitions():
    file_path = "src/components/MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Reading MTGOLayout.css")
        
        # Add smooth transitions to grid containers - find collection-grid
        old_collection_grid_css = """.collection-grid {
  padding: 12px;
  overflow-y: auto;
  flex: 1; /* Take remaining space after header */
  display: grid;
  /* Grid columns and gap set dynamically by JavaScript */
  align-content: start;
}"""
        
        new_collection_grid_css = """.collection-grid {
  padding: 12px;
  overflow-y: auto;
  flex: 1; /* Take remaining space after header */
  display: grid;
  /* Grid columns and gap set dynamically by JavaScript */
  align-content: start;
  transition: gap 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}"""
        
        if old_collection_grid_css in content:
            content = content.replace(old_collection_grid_css, new_collection_grid_css)
            print("✅ Added smooth transitions to collection grid")
        else:
            print("⚠️  Collection grid CSS not found in expected format")
        
        # Add smooth transitions to deck grid
        old_deck_grid_css = """.deck-grid {
  display: grid;
  /* Grid columns and gap will be set dynamically by individual card grids */
  align-content: start;
  min-height: 150px;
  padding-bottom: 40px;
}"""
        
        new_deck_grid_css = """.deck-grid {
  display: grid;
  /* Grid columns and gap will be set dynamically by individual card grids */
  align-content: start;
  min-height: 150px;
  padding-bottom: 40px;
  transition: gap 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}"""
        
        if old_deck_grid_css in content:
            content = content.replace(old_deck_grid_css, new_deck_grid_css)
            print("✅ Added smooth transitions to deck grid")
        else:
            print("⚠️  Deck grid CSS not found in expected format")
        
        # Add smooth transitions to sideboard grid
        old_sideboard_grid_css = """.sideboard-grid {
  display: grid;
  /* Grid columns and gap will be set dynamically by individual card grids */
  align-content: start;
  min-height: 150px;
  padding-bottom: 40px;
}"""
        
        new_sideboard_grid_css = """.sideboard-grid {
  display: grid;
  /* Grid columns and gap will be set dynamically by individual card grids */
  align-content: start;
  min-height: 150px;
  padding-bottom: 40px;
  transition: gap 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}"""
        
        if old_sideboard_grid_css in content:
            content = content.replace(old_sideboard_grid_css, new_sideboard_grid_css)
            print("✅ Added smooth transitions to sideboard grid")
        else:
            print("⚠️  Sideboard grid CSS not found in expected format")
        
        # Enhance existing draggable card transitions 
        old_draggable_transitions = """.draggable-card {
  position: relative;
  display: inline-block;
  transition: transform 0.2s ease, opacity 0.2s ease;
  cursor: grab;
}"""
        
        new_draggable_transitions = """.draggable-card {
  position: relative;
  display: inline-block;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: grab;
}"""
        
        if old_draggable_transitions in content:
            content = content.replace(old_draggable_transitions, new_draggable_transitions)
            print("✅ Enhanced draggable card transitions")
        else:
            print("⚠️  Draggable card transitions not found in expected format")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"❌ Error fixing MTGOLayout.css: {str(e)}")
        return False

def add_smooth_slider_css():
    """Add additional CSS for ultra-smooth slider interactions"""
    file_path = "src/components/MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add new CSS section for smooth grid scaling
        smooth_scaling_css = """
/* SMOOTH SLIDER SCALING - Eliminates card jumping during size changes */
.collection-grid > *,
.deck-grid > *,
.sideboard-grid > * {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Enhanced grid container smoothness */
.collection-grid,
.deck-grid,
.sideboard-grid {
  transition: gap 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              grid-template-columns 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Smooth slider handle transitions */
.size-slider {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.size-slider::-webkit-slider-thumb {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.size-slider::-moz-range-thumb {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}"""
        
        # Find the end of the file and add the new CSS
        if "/* Reduced motion support */" in content:
            insertion_point = content.find("/* Reduced motion support */")
            content = content[:insertion_point] + smooth_scaling_css + "\n\n" + content[insertion_point:]
            print("✅ Added smooth scaling CSS section")
        else:
            # Fallback: add at the very end
            content += smooth_scaling_css
            print("✅ Added smooth scaling CSS at end of file")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return True
    except Exception as e:
        print(f"❌ Error adding smooth CSS: {str(e)}")
        return False

def main():
    print("🎯 Adding smooth transitions to eliminate card jumping during slider use")
    print("="*75)
    
    magic_card_success = fix_magic_card_transitions()
    css_transitions_success = fix_css_grid_transitions()
    smooth_css_success = add_smooth_slider_css()
    
    if magic_card_success and css_transitions_success and smooth_css_success:
        print(f"\n🎯 SUCCESS: Added smooth transitions to eliminate jumping")
        print("✅ MagicCard.tsx: Enhanced card transition timing")
        print("✅ MTGOLayout.css: Added grid transition smoothness")
        print("✅ MTGOLayout.css: Added comprehensive smooth scaling CSS")
        print("\nTransition Improvements:")
        print("• Card size changes: 0.3s smooth cubic-bezier easing")
        print("• Grid gap changes: 0.3s smooth cubic-bezier easing") 
        print("• Grid column changes: 0.3s smooth cubic-bezier easing")
        print("• All card properties: Smooth transitions during scaling")
        print("• Slider handles: Enhanced visual feedback")
        print("\nCubic-Bezier Timing:")
        print("• Using cubic-bezier(0.4, 0, 0.2, 1) - Material Design easing")
        print("• Feels natural and professional")
        print("• Eliminates jarring jumps and snapping")
        print("\nExpected Result:")
        print("• Smooth, fluid slider adjustments")
        print("• Cards resize gracefully without jumping")
        print("• Grid repositioning feels natural")
        print("• Professional, polished user experience")
        print("\nTest with 'npm start' and move sliders - should feel much smoother!")
    else:
        print(f"\n❌ Some fixes failed - check the output above")

if __name__ == "__main__":
    main()
