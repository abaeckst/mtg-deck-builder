// src/components/GoldButton.tsx - Phase 4B: Gold multicolor button component
import React from 'react';

interface GoldButtonProps {
  isSelected: boolean;
  onClick: () => void;
  disabled?: boolean;
  className?: string;
}

const GoldButton: React.FC<GoldButtonProps> = ({
  isSelected,
  onClick,
  disabled = false,
  className = ''
}) => {
  return (
    <button
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
    >
    </button>
  );
};

export default GoldButton;