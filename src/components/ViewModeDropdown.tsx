import React, { useState, useRef, useEffect, memo } from 'react';

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

  // Detect if dropdown is in overflow menu context
  const isInOverflowContext = () => {
    if (!buttonRef.current) return false;
    
    // Check if button is inside overflow menu
    const overflowMenu = buttonRef.current.closest('.overflow-menu');
    const overflowContainer = buttonRef.current.closest('.overflow-menu-container');
    
    return !!(overflowMenu || overflowContainer);
  };

  const handleToggle = () => {
    if (!isOpen) {
      calculateMenuPosition();
    }
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (value: 'card' | 'pile' | 'list') => {
    onViewChange(value);
    setIsOpen(false);
  };


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
            zIndex: isInOverflowContext() ? 2000000 : 600000 // Nuclear z-index with context detection
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

// Performance optimization: Prevent unnecessary re-renders during search operations
const MemoizedViewModeDropdown = memo(ViewModeDropdown);

export default MemoizedViewModeDropdown;