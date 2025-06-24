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
    >
    </button>
  );
};

export default GoldButton;