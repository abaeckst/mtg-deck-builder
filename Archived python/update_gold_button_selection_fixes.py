#!/usr/bin/env python3

import os
import sys

def update_gold_button_selection_fixes():
    """Fix gold button selection indicators and improve blue circle visibility"""
    
    # Update GoldButton.tsx to use proper CSS classes and add immediate feedback
    gold_button_file = "src/components/GoldButton.tsx"
    if not os.path.exists(gold_button_file):
        print(f"Error: {gold_button_file} not found")
        return False
    
    with open(gold_button_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the entire button element to use proper CSS classes and immediate feedback
    old_button = '''    <button
      className={`color-button color-gold ${isSelected ? 'selected' : ''} ${disabled ? 'disabled' : ''} ${className}`}
      onClick={onClick}
      disabled={disabled}
      title={
        disabled 
          ? "Gold (multicolor) mode cannot be used with colorless" 
          : isSelected 
            ? "Remove multicolor filter" 
            : "Filter for multicolor cards"
      }
      aria-label={`Gold multicolor filter ${isSelected ? 'active' : 'inactive'}`}
      aria-pressed={isSelected}
      style={{
        backgroundColor: isSelected ? '#FFD700' : 'transparent',
        border: '2px solid #FFD700',
        color: isSelected ? '#000000' : '#FFD700',
        fontWeight: 'bold',
        transition: 'all 0.2s ease',
        opacity: disabled ? 0.5 : 1,
        cursor: disabled ? 'not-allowed' : 'pointer',
        boxShadow: isSelected ? '0 0 8px rgba(255, 215, 0, 0.6)' : 'none',
      }}
    >'''

    new_button = '''    <button
      className={`color-button color-gold ${isSelected ? 'selected' : ''} ${disabled ? 'disabled' : ''} ${className}`}
      onClick={onClick}
      disabled={disabled}
      title={
        disabled 
          ? "Gold (multicolor) mode cannot be used with colorless" 
          : isSelected 
            ? "Remove multicolor filter" 
            : "Filter for multicolor cards"
      }
      aria-label={`Gold multicolor filter ${isSelected ? 'active' : 'inactive'}`}
      aria-pressed={isSelected}
    >'''

    if old_button in content:
        content = content.replace(old_button, new_button)
        print("✅ Updated GoldButton to use CSS classes instead of inline styles")
    else:
        print("❌ Could not find GoldButton button element to update")
        return False
    
    # Write the updated content
    with open(gold_button_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Update FilterPanel.css to add prominent blue circles for all color buttons
    css_file = "src/components/FilterPanel.css"
    if not os.path.exists(css_file):
        print(f"Error: {css_file} not found")
        return False
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Add enhanced blue circle styling for all color buttons including gold
    enhanced_selection_css = '''
/* Enhanced Blue Circle Selection Indicators - More Prominent and Responsive */
.color-button {
  position: relative;
  transition: all 0.1s ease !important; /* Immediate visual feedback */
}

.color-button.selected::after {
  content: '';
  position: absolute;
  top: -6px;
  right: -6px;
  width: 16px;
  height: 16px;
  background: #3b82f6;
  border: 3px solid #ffffff;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.6);
  z-index: 10;
  animation: blueCircleAppear 0.2s ease;
}

@keyframes blueCircleAppear {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Gold Button Enhanced Styling to Match Other Color Buttons */
.color-button.color-gold {
  font-family: 'Segoe UI', Arial, sans-serif;
  font-size: 11px;
  font-weight: bold;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid #FFD700;
  cursor: pointer;
  transition: all 0.1s ease !important; /* Immediate feedback */
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  text-shadow: none;
  background: linear-gradient(135deg, #FFD700 0%, #FFC107 100%);
  color: #000000;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.color-button.color-gold:hover:not(.disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
  background: linear-gradient(135deg, #FFED4A 0%, #FFB84D 100%);
}

.color-button.color-gold.selected {
  border: 2px solid #FFD700;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
}

/* Gold button gets the same blue circle as other color buttons */
.color-button.color-gold.selected::after {
  content: '';
  position: absolute;
  top: -6px;
  right: -6px;
  width: 16px;
  height: 16px;
  background: #3b82f6;
  border: 3px solid #ffffff;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.6);
  z-index: 10;
  animation: blueCircleAppear 0.2s ease;
}

.color-button.color-gold.disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: #666666;
  border-color: #888888;
  color: #cccccc;
  box-shadow: none;
  transform: none;
}

/* Enhanced responsiveness for all color buttons */
.color-button:active:not(.disabled) {
  transform: scale(0.95);
}

/* Immediate visual feedback on click before state updates */
.color-button:active:not(.selected):not(.disabled) {
  border-color: #3b82f6 !important;
  box-shadow: 0 0 0 1px #3b82f6 !important;
}
'''
    
    # Find the end of the existing color button styles and add our enhanced styles
    insertion_point = css_content.find("/* Enhanced Filter Panel Layout */")
    if insertion_point == -1:
        # If not found, add at the end
        css_content += enhanced_selection_css
        print("✅ Added enhanced blue circle styling at end of CSS file")
    else:
        # Insert before the "Enhanced Filter Panel Layout" section
        css_content = css_content[:insertion_point] + enhanced_selection_css + "\n" + css_content[insertion_point:]
        print("✅ Added enhanced blue circle styling before Enhanced Filter Panel Layout section")
    
    # Write the updated CSS
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print("✅ Successfully updated gold button selection indicators and blue circle visibility")
    print("🎯 Changes made:")
    print("   - Gold button now uses CSS classes instead of inline styles")
    print("   - Blue circles are larger (16px) and more prominent")
    print("   - Added immediate visual feedback with faster transitions (0.1s)")
    print("   - Gold button gets same blue circle as other color buttons")
    print("   - Enhanced border and shadow effects for better visibility")
    print("   - Added click animation for instant feedback")
    return True

if __name__ == "__main__":
    success = update_gold_button_selection_fixes()
    sys.exit(0 if success else 1)