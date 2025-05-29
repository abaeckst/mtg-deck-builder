// src/App.tsx - Fixed MagicCard props
import React, { useState, useCallback } from 'react';
import './App.css';
import { useCards } from './hooks/useCards';
import { MagicCard } from './components/MagicCard';
import { ScryfallCard } from './types/card';

type CardSize = 'small' | 'normal' | 'large';

const App: React.FC = () => {
  const {
    cards,
    loading,
    error,
    searchForCards,
    loadPopularCards,
    loadRandomCard,
    selectCard,
    deselectCard,
    isCardSelected,
    getSelectedCardsData,
    clearSelection,
    totalCards,
  } = useCards();

  const [searchInput, setSearchInput] = useState('');
  const [cardSize, setCardSize] = useState<CardSize>('normal');

  // Debounced search
  const handleSearch = useCallback(async (query: string) => {
    if (query.trim()) {
      await searchForCards(query);
    }
  }, [searchForCards]);

  const handleCardClick = (card: ScryfallCard) => {
    if (isCardSelected(card.id)) {
      deselectCard(card.id);
    } else {
      selectCard(card.id);
    }
  };

  const selectedCards = getSelectedCardsData();
  const showSingleCardDetails = selectedCards.length === 1;

  return (
    <div className="app">
      <header className="app-header">
        <h1>MTG Deck Builder</h1>
        <p className="subtitle">Phase 1: Foundation & Card Search</p>
      </header>

      <div className="search-section">
        <div className="search-controls">
          <input
            type="text"
            placeholder="Search for Magic cards..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                handleSearch(searchInput);
              }
            }}
            className="search-input"
          />
          <button onClick={() => handleSearch(searchInput)} className="search-button">
            Search
          </button>
        </div>

        <div className="quick-actions">
          <button onClick={loadPopularCards} className="action-button">
            Popular Cards
          </button>
          <button onClick={loadRandomCard} className="action-button">
            Random Card
          </button>
          <button onClick={clearSelection} className="action-button">
            Clear Selection ({selectedCards.length})
          </button>
        </div>

        {totalCards > 0 && (
          <div className="results-info">
            Found {totalCards} cards
          </div>
        )}
      </div>

      <div className="size-controls">
        <label>Card Size:</label>
        <button
          className={`size-button ${cardSize === 'small' ? 'active' : ''}`}
          onClick={() => setCardSize('small')}
        >
          Small
        </button>
        <button
          className={`size-button ${cardSize === 'normal' ? 'active' : ''}`}
          onClick={() => setCardSize('normal')}
        >
          Normal
        </button>
        <button
          className={`size-button ${cardSize === 'large' ? 'active' : ''}`}
          onClick={() => setCardSize('large')}
        >
          Large
        </button>
      </div>

      {loading && <div className="loading">Loading cards...</div>}
      {error && <div className="error">Error: {error}</div>}

      <div className="main-content">
        <div className="cards-grid">
          {cards.map((card) => (
            <MagicCard
              key={card.id}
              card={card}
              size={cardSize}
              selected={isCardSelected(card.id)}
              onClick={() => handleCardClick(card)}
              showQuantity={true}
              quantity={4} // Available quantity (simplified for Phase 1)
            />
          ))}
        </div>

        {showSingleCardDetails && (
          <div className="card-details">
            <h3>Card Details</h3>
            <div className="selected-card-info">
              <h4>{selectedCards[0].name}</h4>
              <p><strong>Type:</strong> {selectedCards[0].type_line}</p>
              {selectedCards[0].mana_cost && (
                <p><strong>Mana Cost:</strong> {selectedCards[0].mana_cost}</p>
              )}
              {selectedCards[0].oracle_text && (
                <p><strong>Text:</strong> {selectedCards[0].oracle_text}</p>
              )}
              <p><strong>Set:</strong> {selectedCards[0].set_name} ({selectedCards[0].set})</p>
              <p><strong>Rarity:</strong> {selectedCards[0].rarity}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;