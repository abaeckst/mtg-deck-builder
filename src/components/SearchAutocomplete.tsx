import React, { useState, useRef, useEffect } from 'react';
import './SearchAutocomplete.css';

interface SearchAutocompleteProps {
  value: string;
  onChange: (value: string) => void;
  onSearch: (value: string) => void;
  suggestions: string[];
  showSuggestions: boolean;
  onSuggestionSelect: (suggestion: string) => void;
  onSuggestionsRequested: (query: string) => void;
  onSuggestionsClear: () => void;
  placeholder?: string;
  className?: string;
}

const SearchAutocomplete: React.FC<SearchAutocompleteProps> = ({
  value,
  onChange,
  onSearch,
  suggestions,
  showSuggestions,
  onSuggestionSelect,
  onSuggestionsRequested,
  onSuggestionsClear,
  placeholder = "Search cards...",
  className = ""
}) => {
  const [activeSuggestionIndex, setActiveSuggestionIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    onChange(newValue);
    
    // Request suggestions after short delay
    setTimeout(() => {
      onSuggestionsRequested(newValue);
    }, 200);
    
    setActiveSuggestionIndex(-1);
  };

  // Handle key navigation
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!showSuggestions || suggestions.length === 0) {
      if (e.key === 'Enter') {
        onSearch(value);
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveSuggestionIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : 0
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveSuggestionIndex(prev => 
          prev > 0 ? prev - 1 : suggestions.length - 1
        );
        break;
      case 'Enter':
        e.preventDefault();
        if (activeSuggestionIndex >= 0) {
          onSuggestionSelect(suggestions[activeSuggestionIndex]);
        } else {
          onSearch(value);
          onSuggestionsClear(); // Hide autocomplete after search
        }
        break;
      case 'Escape':
        onSuggestionsClear();
        setActiveSuggestionIndex(-1);
        break;
    }
  };

  // Handle suggestion click
  const handleSuggestionClick = (suggestion: string, index: number) => {
    onSuggestionSelect(suggestion);
    setActiveSuggestionIndex(-1);
  };

  // Handle input blur
  const handleBlur = () => {
    // Delay to allow suggestion clicks to register
    setTimeout(() => {
      onSuggestionsClear();
      setActiveSuggestionIndex(-1);
    }, 200);
  };

  // Click outside to close suggestions
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (suggestionsRef.current && !suggestionsRef.current.contains(event.target as Node) &&
          inputRef.current && !inputRef.current.contains(event.target as Node)) {
        onSuggestionsClear();
        setActiveSuggestionIndex(-1);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onSuggestionsClear]);

  return (
    <div className={`search-autocomplete ${className}`}>
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        onBlur={handleBlur}
        placeholder={placeholder}
        className="search-autocomplete-input"
        autoComplete="off"
      />
      
      {showSuggestions && suggestions.length > 0 && (
        <div ref={suggestionsRef} className="search-suggestions">
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              className={`search-suggestion ${index === activeSuggestionIndex ? 'active' : ''}`}
              onClick={() => handleSuggestionClick(suggestion, index)}
              onMouseEnter={() => setActiveSuggestionIndex(index)}
            >
              {suggestion.startsWith('"') || suggestion.includes(':') || suggestion.startsWith('-') ? (
                <span className="suggestion-operator">{suggestion}</span>
              ) : (
                <span className="suggestion-text">{suggestion}</span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchAutocomplete;