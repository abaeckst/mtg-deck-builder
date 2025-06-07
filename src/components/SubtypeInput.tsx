// src/components/SubtypeInput.tsx - Phase 4B: Autocomplete multi-select for subtypes
import React, { useState, useRef, useEffect, useMemo } from 'react';
import subtypeData from '../data/subtypes.json';

interface SubtypeInputProps {
  selectedSubtypes: string[];
  onSubtypeAdd: (subtype: string) => void;
  onSubtypeRemove: (subtype: string) => void;
  placeholder?: string;
  className?: string;
}

const SubtypeInput: React.FC<SubtypeInputProps> = ({
  selectedSubtypes,
  onSubtypeAdd,
  onSubtypeRemove,
  placeholder = "Type subtypes...",
  className = ''
}) => {
  const [inputValue, setInputValue] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  // Flatten all subtypes for autocomplete
  const allSubtypes = useMemo(() => {
    const types = new Set<string>();
    
    // Add all creature types
    subtypeData.creature_types.forEach(type => types.add(type));
    
    // Add all planeswalker types
    subtypeData.planeswalker_types.forEach(type => types.add(type));
    
    // Add all artifact types
    subtypeData.artifact_types.forEach(type => types.add(type));
    
    // Add all enchantment types
    subtypeData.enchantment_types.forEach(type => types.add(type));
    
    // Add all instant/sorcery types
    subtypeData.instant_sorcery_types.forEach(type => types.add(type));
    
    // Add all land types
    subtypeData.land_types.forEach(type => types.add(type));
    
    return Array.from(types).sort();
  }, []);

  // Filter suggestions based on input
  const suggestions = useMemo(() => {
    if (!inputValue.trim()) return [];
    
    const query = inputValue.toLowerCase();
    return allSubtypes
      .filter(subtype => 
        subtype.toLowerCase().includes(query) && 
        !selectedSubtypes.includes(subtype)
      )
      .slice(0, 8); // Limit to 8 suggestions
  }, [inputValue, allSubtypes, selectedSubtypes]);

  // Handle input change
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInputValue(value);
    setShowSuggestions(value.trim().length > 0);
    setHighlightedIndex(-1);
  };

  // Handle input key down
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!showSuggestions) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setHighlightedIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : 0
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setHighlightedIndex(prev => 
          prev > 0 ? prev - 1 : suggestions.length - 1
        );
        break;
      case 'Enter':
        e.preventDefault();
        if (highlightedIndex >= 0 && suggestions[highlightedIndex]) {
          addSubtype(suggestions[highlightedIndex]);
        } else if (inputValue.trim()) {
          // Allow custom subtypes
          addSubtype(inputValue.trim());
        }
        break;
      case 'Escape':
        setShowSuggestions(false);
        setHighlightedIndex(-1);
        break;
      case 'Tab':
        if (highlightedIndex >= 0 && suggestions[highlightedIndex]) {
          e.preventDefault();
          addSubtype(suggestions[highlightedIndex]);
        }
        break;
    }
  };

  // Add subtype
  const addSubtype = (subtype: string) => {
    const trimmedSubtype = subtype.trim();
    if (trimmedSubtype && !selectedSubtypes.includes(trimmedSubtype)) {
      onSubtypeAdd(trimmedSubtype);
      setInputValue('');
      setShowSuggestions(false);
      setHighlightedIndex(-1);
    }
  };

  // Handle suggestion click
  const handleSuggestionClick = (subtype: string) => {
    addSubtype(subtype);
    inputRef.current?.focus();
  };

  // Handle chip removal
  const handleChipRemove = (subtype: string, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onSubtypeRemove(subtype);
  };

  // Handle input blur
  const handleBlur = (e: React.FocusEvent) => {
    // Delay hiding suggestions to allow clicking on them
    setTimeout(() => {
      if (!suggestionsRef.current?.contains(document.activeElement)) {
        setShowSuggestions(false);
        setHighlightedIndex(-1);
      }
    }, 150);
  };

  // Handle input focus
  const handleFocus = () => {
    if (inputValue.trim()) {
      setShowSuggestions(true);
    }
  };

  return (
    <div className={`subtype-input-container ${className}`}>
      {/* Selected subtypes as chips */}
      {selectedSubtypes.length > 0 && (
        <div className="subtype-chips">
          {selectedSubtypes.map(subtype => (
            <span key={subtype} className="subtype-chip">
              {subtype}
              <button
                type="button"
                className="chip-remove"
                onClick={(e) => handleChipRemove(subtype, e)}
                aria-label={`Remove ${subtype} filter`}
                title={`Remove ${subtype}`}
              >
                ×
              </button>
            </span>
          ))}
        </div>
      )}
      
      {/* Input field */}
      <div className="subtype-input-wrapper">
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onBlur={handleBlur}
          onFocus={handleFocus}
          placeholder={placeholder}
          className="subtype-input"
          autoComplete="off"
          aria-label="Subtype filter input"
          aria-expanded={showSuggestions}
          aria-haspopup="listbox"
          role="combobox"
        />
        
        {/* Suggestions dropdown */}
        {showSuggestions && suggestions.length > 0 && (
          <div 
            ref={suggestionsRef}
            className="subtype-suggestions"
            role="listbox"
          >
            {suggestions.map((suggestion, index) => (
              <div
                key={suggestion}
                className={`subtype-suggestion ${index === highlightedIndex ? 'highlighted' : ''}`}
                onClick={() => handleSuggestionClick(suggestion)}
                role="option"
                aria-selected={index === highlightedIndex}
              >
                {suggestion}
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Helper text */}
      {selectedSubtypes.length === 0 && !inputValue && (
        <div className="subtype-help-text">
          Type to search for creature types, planeswalker types, and other subtypes
        </div>
      )}
    </div>
  );
};

export default SubtypeInput;