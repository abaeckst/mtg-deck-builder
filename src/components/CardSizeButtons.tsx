// src/components/CardSizeButtons.tsx
// Three-button card size selector with MTGO-style design

import React from 'react';
import { CardSizeMode } from '../types/card';

interface CardSizeButtonsProps {
  currentMode: CardSizeMode;
  onModeChange: (mode: CardSizeMode) => void;
  className?: string;
}

/**
 * Card size button group component
 * Provides Small/Normal/Large options matching search toggle pattern
 */
export const CardSizeButtons: React.FC<CardSizeButtonsProps> = ({
  currentMode,
  onModeChange,
  className = '',
}) => {
  const sizeOptions: { mode: CardSizeMode; label: string; icon: string }[] = [
    { mode: 'small', label: 'S', icon: '🔸' },
    { mode: 'normal', label: 'N', icon: '🔹' },
    { mode: 'large', label: 'L', icon: '🔷' },
  ];

  return (
    <div className={`card-size-buttons ${className}`}>
      {sizeOptions.map(({ mode, label, icon }) => (
        <button
          key={mode}
          className={`size-button ${currentMode === mode ? 'active' : ''}`}
          onClick={() => onModeChange(mode)}
          title={`${mode.charAt(0).toUpperCase() + mode.slice(1)} cards`}
          type="button"
        >
          <span className="size-icon">{icon}</span>
          <span className="size-label">{label}</span>
        </button>
      ))}
    </div>
  );
};

export default CardSizeButtons;