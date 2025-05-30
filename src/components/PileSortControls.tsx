// ===== FILE 3: src/components/PileSortControls.tsx - FIXED VERSION =====
import React from 'react';
import { SortCriteria } from './PileView'; // FIXED: Import shared type

interface PileSortControlsProps {
  currentSort: SortCriteria;
  onSortChange: (criteria: SortCriteria) => void;
  zone: 'deck' | 'sideboard';
}

const PileSortControls: React.FC<PileSortControlsProps> = ({
  currentSort,
  onSortChange,
  zone,
}) => {
  const sortOptions: Array<{ value: SortCriteria; label: string; description: string }> = [
    { value: 'mana', label: 'Mana Value', description: 'Sort by converted mana cost' },
    { value: 'color', label: 'Color', description: 'Sort by color identity' },
    { value: 'rarity', label: 'Rarity', description: 'Sort by card rarity' },
    { value: 'type', label: 'Card Type', description: 'Sort by card type' },
  ];

  const handleSortChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newSort = event.target.value as SortCriteria;
    
    if (newSort === currentSort) {
      return; // No change needed
    }
    
    if (!sortOptions.some(option => option.value === newSort)) {
      console.warn(`Invalid sort criteria: ${newSort}`);
      return;
    }
    
    onSortChange(newSort);
  };

  const currentOption = sortOptions.find(option => option.value === currentSort);

  return (
    <div className="pile-sort-controls">
      <label htmlFor={`sort-select-${zone}`} className="sort-label">
        Sort:
      </label>
      <select
        id={`sort-select-${zone}`}
        className="sort-dropdown"
        value={currentSort}
        onChange={handleSortChange}
        title={`${currentOption?.description || 'Sort criteria'} for ${zone}`}
      >
        {sortOptions.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default PileSortControls;