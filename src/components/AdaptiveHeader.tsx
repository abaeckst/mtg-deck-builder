// src/components/AdaptiveHeader.tsx - Responsive Header Component
import React, { useState, useCallback, useMemo, useRef, useEffect } from 'react';

export interface HeaderControl {
  id: string;
  type: 'button' | 'slider' | 'dropdown' | 'buttonGroup';
  priority: number; // 1=highest, 5=lowest
  minWidth: number;
  content: React.ReactNode;
  iconMode?: React.ReactNode;
}

interface AdaptiveHeaderProps {
  title: string;
  controls: HeaderControl[];
  availableWidth: number;
  onControlAction: (controlId: string, value?: any) => void;
  className?: string;
}

const AdaptiveHeader: React.FC<AdaptiveHeaderProps> = ({
  title,
  controls,
  availableWidth,
  onControlAction,
  className = '',
}) => {
  const [showDropdown, setShowDropdown] = useState(false);
  const [useIconMode, setUseIconMode] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);

  // Calculate which controls are visible vs in dropdown
  const { visibleControls, overflowControls } = useMemo(() => {
    // Sort controls by priority (1 = highest priority)
    const sortedControls = [...controls].sort((a, b) => a.priority - b.priority);
    
    // Estimate title width (rough approximation)
    const titleWidth = title.length * 8 + 20; // Rough character width + padding
    const dropdownButtonWidth = 40; // Width of overflow button
    
    let usedWidth = titleWidth;
    const visible: HeaderControl[] = [];
    const overflow: HeaderControl[] = [];
    
    // Determine if we should use icon mode
    const shouldUseIconMode = availableWidth < 600;
    setUseIconMode(shouldUseIconMode);
    
    for (const control of sortedControls) {
      const controlWidth = shouldUseIconMode && control.iconMode ? 40 : control.minWidth;
      
      // Reserve space for dropdown button if there are more controls
      const remainingControls = sortedControls.length - visible.length - 1;
      const needsDropdownButton = remainingControls > 0;
      const requiredWidth = usedWidth + controlWidth + (needsDropdownButton ? dropdownButtonWidth : 0);
      
      if (requiredWidth <= availableWidth) {
        visible.push(control);
        usedWidth += controlWidth;
      } else {
        overflow.push(control);
      }
    }
    
    return { 
      visibleControls: visible, 
      overflowControls: overflow 
    };
  }, [controls, availableWidth, title]);

  // Handle control actions
  const handleControlAction = useCallback((controlId: string, value?: any) => {
    onControlAction(controlId, value);
    // Close dropdown after action
    setShowDropdown(false);
  }, [onControlAction]);

  // Handle dropdown toggle
  const handleDropdownToggle = useCallback(() => {
    setShowDropdown(prev => !prev);
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };

    if (showDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showDropdown]);

  // Render a single control
  const renderControl = useCallback((control: HeaderControl, inDropdown = false) => {
    const isIconMode = useIconMode && !inDropdown && control.iconMode;
    
    return (
      <div
        key={control.id}
        className={`header-control header-control-${control.type} ${inDropdown ? 'in-dropdown' : ''}`}
        style={{
          minWidth: isIconMode ? '40px' : `${control.minWidth}px`,
        }}
      >
        {isIconMode ? control.iconMode : control.content}
      </div>
    );
  }, [useIconMode]);

  return (
    <div 
      ref={headerRef}
      className={`adaptive-header ${className}`}
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        width: '100%',
        height: '40px',
        padding: '0 12px',
        backgroundColor: '#333333',
        borderBottom: '1px solid #555555',
      }}
    >
      {/* Title */}
      <div className="header-title">
        <h3 style={{ 
          margin: 0, 
          fontSize: '14px', 
          fontWeight: 600, 
          color: '#ffffff',
          whiteSpace: 'nowrap',
          overflow: 'hidden',
          textOverflow: 'ellipsis',
        }}>
          {title}
        </h3>
      </div>

      {/* Controls */}
      <div className="header-controls" style={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: '6px',
        flexShrink: 0,
      }}>
        {/* Visible controls */}
        {visibleControls.map(control => renderControl(control))}
        
        {/* Overflow dropdown */}
        {overflowControls.length > 0 && (
          <div className="header-dropdown-container" ref={dropdownRef} style={{ position: 'relative' }}>
            <button
              className="header-dropdown-toggle"
              onClick={handleDropdownToggle}
              style={{
                background: '#404040',
                color: '#ffffff',
                border: '1px solid #555555',
                padding: '4px 8px',
                borderRadius: '3px',
                fontSize: '12px',
                cursor: 'pointer',
                minWidth: '32px',
                height: '28px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              ⋯
            </button>
            
            {showDropdown && (
              <div
                className="header-dropdown-menu"
                style={{
                  position: 'absolute',
                  top: '100%',
                  right: 0,
                  backgroundColor: '#333333',
                  border: '1px solid #555555',
                  borderRadius: '4px',
                  boxShadow: '0 4px 8px rgba(0,0,0,0.3)',
                  zIndex: 1000,
                  minWidth: '200px',
                  maxWidth: '300px',
                  overflow: 'hidden',
                  marginTop: '2px',
                }}
              >
                {overflowControls.map((control, index) => (
                  <div
                    key={control.id}
                    className="dropdown-item"
                    style={{
                      padding: '8px 12px',
                      borderBottom: index < overflowControls.length - 1 ? '1px solid #555555' : 'none',
                      cursor: 'pointer',
                      transition: 'background-color 0.2s ease',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor = '#4a4a4a';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = 'transparent';
                    }}
                  >
                    {renderControl(control, true)}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdaptiveHeader;