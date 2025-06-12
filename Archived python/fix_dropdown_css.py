#!/usr/bin/env python3
"""
Fix ViewModeDropdown CSS visibility issues
Add necessary CSS to make dropdown menu visible and properly positioned.
"""

def add_dropdown_css():
    """Add ViewModeDropdown CSS to MTGOLayout.css"""
    print("=== Adding ViewModeDropdown CSS to MTGOLayout.css ===")
    
    # CSS to add at the end of MTGOLayout.css
    dropdown_css = """

/* ===== VIEWMODE DROPDOWN STYLES ===== */

/* ViewModeDropdown container - ensure relative positioning */
.view-mode-dropdown {
  position: relative !important;
  display: inline-block;
  z-index: 10;
}

/* ViewModeDropdown button - ensure proper styling */
.view-dropdown-button {
  background: #333333 !important;
  border: 1px solid #555555 !important;
  color: #ffffff !important;
  font-size: 12px !important;
  cursor: pointer !important;
  border-radius: 2px !important;
  min-width: 85px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 4px !important;
  padding: 4px 8px !important;
  position: relative !important;
  z-index: 10 !important;
}

.view-dropdown-button:hover {
  background: #4a4a4a !important;
}

/* ViewModeDropdown menu - HIGH Z-INDEX AND ESCAPE CLIPPING */
.view-dropdown-menu {
  position: fixed !important; /* Use fixed instead of absolute to escape all containers */
  background: #2a2a2a !important;
  border: 1px solid #555555 !important;
  border-radius: 2px !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.5) !important;
  z-index: 9999 !important; /* Higher than resize handles (1001) and context menu (1000) */
  min-width: 100px !important;
  margin-top: 1px !important;
  overflow: visible !important;
}

/* ViewModeDropdown options */
.view-dropdown-option {
  display: block !important;
  width: 100% !important;
  padding: 6px 10px !important;
  background: transparent !important;
  border: none !important;
  color: #ffffff !important;
  font-size: 12px !important;
  text-align: left !important;
  cursor: pointer !important;
  white-space: nowrap !important;
}

.view-dropdown-option:hover {
  background: #3a3a3a !important;
}

.view-dropdown-option.active {
  background: #4a4a4a !important;
}

/* CRITICAL: Ensure parent containers don't clip dropdown */
.mtgo-header {
  overflow: visible !important;
}

.deck-controls {
  overflow: visible !important;
  position: relative !important;
}

/* Ensure dropdown arrow rotates properly */
.view-dropdown-button svg {
  transition: transform 0.15s ease !important;
}

/* ===== END VIEWMODE DROPDOWN STYLES ===== */
"""
    
    try:
        # Read current MTGOLayout.css
        with open("src/components/MTGOLayout.css", "r", encoding="utf-8") as f:
            current_css = f.read()
        
        # Check if dropdown styles already exist
        if "VIEWMODE DROPDOWN STYLES" in current_css:
            print("✅ ViewModeDropdown styles already exist in MTGOLayout.css")
            return True
        
        # Add dropdown CSS to the end
        updated_css = current_css + dropdown_css
        
        # Write updated CSS
        with open("src/components/MTGOLayout.css", "w", encoding="utf-8") as f:
            f.write(updated_css)
        
        print("✅ ViewModeDropdown CSS added to MTGOLayout.css")
        print("📋 Added styles:")
        print("   - High z-index (9999) to escape all containers")
        print("   - Fixed positioning to break out of clipping containers") 
        print("   - Overflow visible on parent containers")
        print("   - MTGO-style theming consistent with app")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding CSS: {e}")
        return False

def update_dropdown_component():
    """Update ViewModeDropdown component to use fixed positioning"""
    print("\n=== Updating ViewModeDropdown Component for Fixed Positioning ===")
    
    # Enhanced component with fixed positioning logic
    fixed_component = '''import React, { useState, useRef, useEffect } from 'react';

interface ViewModeDropdownProps {
  currentView: 'card' | 'pile' | 'list';
  onViewChange: (view: 'card' | 'pile' | 'list') => void;
  className?: string;
}

const ViewModeDropdown: React.FC<ViewModeDropdownProps> = ({
  currentView,
  onViewChange,
  className = ''
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [menuPosition, setMenuPosition] = useState({ top: 0, left: 0 });
  const dropdownRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const viewOptions = [
    { value: 'card' as const, label: 'Card View' },
    { value: 'pile' as const, label: 'Pile View' },
    { value: 'list' as const, label: 'List View' }
  ];

  const currentOption = viewOptions.find(option => option.value === currentView);

  // Calculate menu position when opening
  const calculateMenuPosition = () => {
    if (buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      setMenuPosition({
        top: rect.bottom + window.scrollY + 1,
        left: rect.left + window.scrollX
      });
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [isOpen]);

  const handleToggle = () => {
    console.log('🔧 ViewModeDropdown toggle - before:', isOpen);
    if (!isOpen) {
      calculateMenuPosition();
    }
    setIsOpen(!isOpen);
    console.log('🔧 ViewModeDropdown toggle - after:', !isOpen);
  };

  const handleOptionClick = (value: 'card' | 'pile' | 'list') => {
    console.log('🔧 ViewModeDropdown option clicked:', value);
    onViewChange(value);
    setIsOpen(false);
  };

  console.log('🔧 ViewModeDropdown render:', { currentView, isOpen, currentOption: currentOption?.label });

  return (
    <div ref={dropdownRef} className={`view-mode-dropdown ${className}`}>
      {/* Dropdown Button */}
      <button
        ref={buttonRef}
        type="button"
        onClick={handleToggle}
        className="view-dropdown-button"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        title={`Current view: ${currentOption?.label || 'View'}`}
      >
        <span>{currentOption?.label.replace(' View', '') || 'View'}</span>
        <svg
          style={{
            width: '12px',
            height: '12px',
            transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 0.15s ease'
          }}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown Menu - Fixed Positioning */}
      {isOpen && (
        <div 
          className="view-dropdown-menu"
          style={{
            position: 'fixed',
            top: `${menuPosition.top}px`,
            left: `${menuPosition.left}px`,
            zIndex: 9999
          }}
        >
          {viewOptions.map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => handleOptionClick(option.value)}
              className={`view-dropdown-option ${option.value === currentView ? 'active' : ''}`}
            >
              {option.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default ViewModeDropdown;'''

    try:
        # Write the updated component
        with open("src/components/ViewModeDropdown.tsx", "w", encoding="utf-8") as f:
            f.write(fixed_component)
            
        print("✅ ViewModeDropdown.tsx updated with fixed positioning")
        print("📋 Key fixes:")
        print("   - Fixed positioning calculation relative to button")
        print("   - Menu position calculated on open")
        print("   - High z-index (9999) in inline styles")
        print("   - Enhanced console logging for debugging")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating component: {e}")
        return False

def main():
    """Apply both CSS and component fixes"""
    print("🔧 Fixing ViewModeDropdown Visibility Issues")
    print("=" * 50)
    
    # Apply CSS fixes
    css_success = add_dropdown_css()
    
    # Apply component fixes  
    component_success = update_dropdown_component()
    
    if css_success and component_success:
        print("\n" + "=" * 50)
        print("✅ ALL FIXES APPLIED SUCCESSFULLY!")
        print("\n🎯 Next Steps:")
        print("1. Run 'npm start' to start the development server")
        print("2. Click the View dropdown button in the deck area")
        print("3. The dropdown menu should now appear properly")
        print("4. Check browser console for debug logs")
        print("\n💡 Key Changes Made:")
        print("- Added high z-index CSS (9999) to escape all containers")
        print("- Used fixed positioning to break out of clipping containers")
        print("- Added overflow: visible to parent containers")
        print("- Enhanced component with position calculation")
    else:
        print("\n❌ Some fixes failed - check error messages above")

if __name__ == "__main__":
    main()