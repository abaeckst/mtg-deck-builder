#!/usr/bin/env python3
"""
Comprehensive fix script for all import and casing issues
This script will:
1. Clean up duplicate files
2. Fix all import statements to use consistent casing
3. Fix TypeScript parameter typing issues
4. Create properly named files with correct content
"""

import os
import re

def clean_up_files():
    """Remove duplicate and incorrectly named files"""
    print("🧹 Cleaning up duplicate and incorrectly named files...")
    
    files_to_remove = [
        'src/components/screenshot_utils.tsx',
        'src/utils/ScreenshotUtils.ts',
        'src/components/modal.tsx',  # lowercase version
        'src/utils/deckformatting.ts',  # lowercase version
        'src/utils/screenshotutils.ts',  # lowercase version
    ]
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
            except Exception as e:
                print(f"⚠️  Could not remove {file_path}: {e}")

def create_deck_formatting_utils():
    """Create the deckFormatting.ts file with correct name and content"""
    print("📝 Creating deckFormatting.ts...")
    
    os.makedirs('src/utils', exist_ok=True)
    
    content = '''// src/utils/deckFormatting.ts
// Utilities for formatting deck data for text export

import { DeckCardInstance } from '../types/card';

export interface DeckExportData {
  deckName: string;
  format: string;
  mainDeck: DeckCardInstance[];
  sideboard: DeckCardInstance[];
}

export interface CardTypeCounts {
  creatures: number;
  instants: number;
  sorceries: number;
  artifacts: number;
  enchantments: number;
  planeswalkers: number;
  lands: number;
  other: number;
}

/**
 * Group cards by name and count quantities
 */
export const groupCardsByName = (cards: DeckCardInstance[]): Map<string, number> => {
  const grouped = new Map<string, number>();
  
  cards.forEach(card => {
    const current = grouped.get(card.name) || 0;
    grouped.set(card.name, current + 1);
  });
  
  return grouped;
};

/**
 * Calculate card type counts for deck overview
 */
export const calculateCardTypeCounts = (cards: DeckCardInstance[]): CardTypeCounts => {
  const counts: CardTypeCounts = {
    creatures: 0,
    instants: 0,
    sorceries: 0,
    artifacts: 0,
    enchantments: 0,
    planeswalkers: 0,
    lands: 0,
    other: 0
  };
  
  cards.forEach(card => {
    const typeLine = card.type_line.toLowerCase();
    
    if (typeLine.includes('creature')) {
      counts.creatures++;
    } else if (typeLine.includes('instant')) {
      counts.instants++;
    } else if (typeLine.includes('sorcery')) {
      counts.sorceries++;
    } else if (typeLine.includes('artifact')) {
      counts.artifacts++;
    } else if (typeLine.includes('enchantment')) {
      counts.enchantments++;
    } else if (typeLine.includes('planeswalker')) {
      counts.planeswalkers++;
    } else if (typeLine.includes('land')) {
      counts.lands++;
    } else {
      counts.other++;
    }
  });
  
  return counts;
};

/**
 * Format deck data into MTGO-compatible text format
 */
export const formatDeckForMTGO = (data: DeckExportData): string => {
  const { deckName, format, mainDeck, sideboard } = data;
  
  // Calculate card type counts
  const typeCounts = calculateCardTypeCounts(mainDeck);
  
  // Group cards by name and quantity
  const mainDeckGroups = groupCardsByName(mainDeck);
  const sideboardGroups = groupCardsByName(sideboard);
  
  // Sort cards alphabetically within each group
  const sortedMainDeck = Array.from(mainDeckGroups.entries()).sort(([a], [b]) => a.localeCompare(b));
  const sortedSideboard = Array.from(sideboardGroups.entries()).sort(([a], [b]) => a.localeCompare(b));
  
  // Build the formatted string
  const lines: string[] = [];
  
  // Header information
  lines.push(`// Deck Name: ${deckName}`);
  lines.push(`// Format: ${format}`);
  
  // Card type summary
  const typeStrings: string[] = [];
  if (typeCounts.creatures > 0) typeStrings.push(`Creatures: ${typeCounts.creatures}`);
  if (typeCounts.instants > 0) typeStrings.push(`Instants: ${typeCounts.instants}`);
  if (typeCounts.sorceries > 0) typeStrings.push(`Sorceries: ${typeCounts.sorceries}`);
  if (typeCounts.artifacts > 0) typeStrings.push(`Artifacts: ${typeCounts.artifacts}`);
  if (typeCounts.enchantments > 0) typeStrings.push(`Enchantments: ${typeCounts.enchantments}`);
  if (typeCounts.planeswalkers > 0) typeStrings.push(`Planeswalkers: ${typeCounts.planeswalkers}`);
  if (typeCounts.lands > 0) typeStrings.push(`Lands: ${typeCounts.lands}`);
  if (typeCounts.other > 0) typeStrings.push(`Other: ${typeCounts.other}`);
  
  if (typeStrings.length > 0) {
    lines.push(`// ${typeStrings.join(', ')}`);
  }
  
  lines.push('');
  
  // Main deck
  if (sortedMainDeck.length > 0) {
    sortedMainDeck.forEach(([cardName, quantity]) => {
      lines.push(`${quantity} ${cardName}`);
    });
  } else {
    lines.push('// Empty deck');
  }
  
  // Sideboard
  if (sortedSideboard.length > 0) {
    lines.push('');
    lines.push('Sideboard:');
    sortedSideboard.forEach(([cardName, quantity]) => {
      lines.push(`${quantity} ${cardName}`);
    });
  }
  
  return lines.join('\\n');
};

/**
 * Get a formatted display name for the current format
 */
export const getFormatDisplayName = (format: string): string => {
  const formatNames: Record<string, string> = {
    'standard': 'Standard',
    'custom-standard': 'Custom Standard (Standard + Unreleased)',
    'pioneer': 'Pioneer',
    'modern': 'Modern',
    'legacy': 'Legacy',
    'vintage': 'Vintage',
    'commander': 'Commander',
    'pauper': 'Pauper',
    '': 'All Formats'
  };
  
  return formatNames[format] || format;
};

/**
 * Copy text to clipboard with fallback support
 */
export const copyToClipboard = async (text: string): Promise<boolean> => {
  try {
    // Modern clipboard API
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    }
    
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    const success = document.execCommand('copy');
    document.body.removeChild(textArea);
    
    return success;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    return false;
  }
};
'''
    
    with open('src/utils/deckFormatting.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created src/utils/deckFormatting.ts")

def create_screenshot_utils():
    """Create the screenshotUtils.ts file with correct name and content"""
    print("📝 Creating screenshotUtils.ts...")
    
    os.makedirs('src/utils', exist_ok=True)
    
    content = '''// src/utils/screenshotUtils.ts
// Utilities for screenshot generation and deck image layout

import html2canvas from 'html2canvas';
import { DeckCardInstance, groupInstancesByCardId } from '../types/card';

export interface ScreenshotLayout {
  mainDeckColumns: DeckCardInstance[][];
  sideboardColumns: DeckCardInstance[][];
}

export interface CardStackInfo {
  card: DeckCardInstance;
  quantity: number;
}

/**
 * Group unique cards and sort by mana cost for screenshot layout
 */
export const groupUniqueCards = (cards: DeckCardInstance[]): Map<string, DeckCardInstance[]> => {
  const groups = groupInstancesByCardId(cards);
  
  // Convert to array and sort by mana cost, then name
  const sortedEntries = Array.from(groups.entries()).sort(([, instancesA], [, instancesB]) => {
    const cardA = instancesA[0];
    const cardB = instancesB[0];
    
    // Sort by mana cost first
    if (cardA.cmc !== cardB.cmc) {
      return cardA.cmc - cardB.cmc;
    }
    
    // Then by name alphabetically
    return cardA.name.localeCompare(cardB.name);
  });
  
  // Convert back to Map with sorted order
  const sortedGroups = new Map<string, DeckCardInstance[]>();
  sortedEntries.forEach(([cardId, instances]) => {
    sortedGroups.set(cardId, instances);
  });
  
  return sortedGroups;
};

/**
 * Arrange cards for screenshot layout with round-robin distribution
 */
export const arrangeCardsForScreenshot = (
  mainDeck: DeckCardInstance[], 
  sideboard: DeckCardInstance[]
): ScreenshotLayout => {
  // Group and sort main deck cards
  const mainDeckGroups = groupUniqueCards(mainDeck);
  const mainDeckCards = Array.from(mainDeckGroups.values()).map(instances => instances[0]);
  
  // Group and sort sideboard cards
  const sideboardGroups = groupUniqueCards(sideboard);
  const sideboardCards = Array.from(sideboardGroups.values()).map(instances => instances[0]);
  
  // Distribute main deck across 5 columns (round-robin)
  const mainDeckColumns: DeckCardInstance[][] = [[], [], [], [], []];
  mainDeckCards.forEach((card, index) => {
    const columnIndex = index % 5;
    mainDeckColumns[columnIndex].push(card);
  });
  
  // Distribute sideboard across 2 columns (round-robin)
  const sideboardColumns: DeckCardInstance[][] = [[], []];
  sideboardCards.forEach((card, index) => {
    const columnIndex = index % 2;
    sideboardColumns[columnIndex].push(card);
  });
  
  return {
    mainDeckColumns,
    sideboardColumns
  };
};

/**
 * Generate deck image using html2canvas
 */
export const generateDeckImage = async (elementId: string): Promise<Blob | null> => {
  try {
    const element = document.getElementById(elementId);
    if (!element) {
      throw new Error(`Element with ID '${elementId}' not found`);
    }
    
    // Configure html2canvas options for better quality
    const canvas = await html2canvas(element, {
      background: '#1a1a1a', // MTGO dark background
      scale: 2, // Higher resolution
      useCORS: true, // Allow cross-origin images
      allowTaint: true, // Allow tainted canvas
      logging: false, // Disable logging for cleaner output
      width: element.scrollWidth,
      height: element.scrollHeight,
      scrollX: 0,
      scrollY: 0
    });
    
    // Convert canvas to blob
    return new Promise((resolve) => {
      canvas.toBlob(resolve, 'image/png', 0.95);
    });
  } catch (error) {
    console.error('Failed to generate deck image:', error);
    return null;
  }
};

/**
 * Download image blob as file
 */
export const downloadImage = (blob: Blob, filename: string): void => {
  try {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Clean up the object URL
    setTimeout(() => URL.revokeObjectURL(url), 100);
  } catch (error) {
    console.error('Failed to download image:', error);
  }
};

/**
 * Generate a filename for the deck image
 */
export const generateDeckImageFilename = (deckName: string = 'deck'): string => {
  // Sanitize deck name for filename
  const sanitized = deckName
    .replace(/[^a-zA-Z0-9\\-_\\s]/g, '') // Remove invalid characters
    .replace(/\\s+/g, '_') // Replace spaces with underscores
    .toLowerCase();
    
  const timestamp = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  return `${sanitized}_${timestamp}.png`;
};

/**
 * Get card quantity for a specific card in a group
 */
export const getCardQuantityInGroup = (
  groups: Map<string, DeckCardInstance[]>, 
  cardId: string
): number => {
  const instances = groups.get(cardId);
  return instances ? instances.length : 0;
};

/**
 * Create card stack information for display
 */
export const createCardStackInfo = (
  cards: DeckCardInstance[],
  groups: Map<string, DeckCardInstance[]>
): CardStackInfo[] => {
  return cards.map(card => ({
    card,
    quantity: getCardQuantityInGroup(groups, card.cardId)
  }));
};
'''
    
    with open('src/utils/screenshotUtils.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created src/utils/screenshotUtils.ts")

def create_text_export_modal():
    """Create the TextExportModal.tsx file with correct imports"""
    print("📝 Creating TextExportModal.tsx...")
    
    content = '''import React, { useState, useEffect, useMemo } from 'react';
import { Modal } from './Modal';
import { DeckCardInstance } from '../types/card';
import { 
  formatDeckForMTGO, 
  copyToClipboard, 
  getFormatDisplayName,
  DeckExportData,
  calculateCardTypeCounts
} from '../utils/deckFormatting';

interface TextExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  mainDeck: DeckCardInstance[];
  sideboard: DeckCardInstance[];
  format: string;
  deckName?: string;
}

export const TextExportModal: React.FC<TextExportModalProps> = ({
  isOpen,
  onClose,
  mainDeck,
  sideboard,
  format,
  deckName = 'Untitled Deck'
}) => {
  const [copyStatus, setCopyStatus] = useState<'idle' | 'copying' | 'success' | 'error'>('idle');
  
  // Auto-copy on modal open
  useEffect(() => {
    if (isOpen && copyStatus === 'idle') {
      handleCopyToClipboard();
    }
  }, [isOpen]);
  
  // Generate formatted deck text
  const deckData: DeckExportData = useMemo(() => ({
    deckName,
    format: getFormatDisplayName(format),
    mainDeck,
    sideboard
  }), [deckName, format, mainDeck, sideboard]);
  
  const formattedText = useMemo(() => {
    return formatDeckForMTGO(deckData);
  }, [deckData]);
  
  // Calculate card type counts for display
  const typeCounts = useMemo(() => {
    return calculateCardTypeCounts(mainDeck);
  }, [mainDeck]);
  
  const handleCopyToClipboard = async () => {
    setCopyStatus('copying');
    
    try {
      const success = await copyToClipboard(formattedText);
      if (success) {
        setCopyStatus('success');
        setTimeout(() => setCopyStatus('idle'), 2000);
      } else {
        setCopyStatus('error');
        setTimeout(() => setCopyStatus('idle'), 3000);
      }
    } catch (error) {
      console.error('Copy failed:', error);
      setCopyStatus('error');
      setTimeout(() => setCopyStatus('idle'), 3000);
    }
  };
  
  const getCopyButtonText = () => {
    switch (copyStatus) {
      case 'copying':
        return 'Copying...';
      case 'success':
        return 'Copied!';
      case 'error':
        return 'Copy Failed';
      default:
        return 'Copy to Clipboard';
    }
  };
  
  const getCopyButtonClass = () => {
    switch (copyStatus) {
      case 'success':
        return 'modal-button success';
      case 'error':
        return 'modal-button error';
      default:
        return 'modal-button primary';
    }
  };
  
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Export Deck as Text"
      size="large"
      className="text-export-modal"
    >
      <div className="deck-export-info">
        <h4>Deck Information</h4>
        <p><strong>Name:</strong> {deckName}</p>
        <p><strong>Format:</strong> {getFormatDisplayName(format)}</p>
        <p><strong>Main Deck:</strong> {mainDeck.length} cards</p>
        <p><strong>Sideboard:</strong> {sideboard.length} cards</p>
        
        {mainDeck.length > 0 && (
          <p>
            <strong>Types:</strong> {' '}
            {[
              typeCounts.creatures > 0 && `Creatures: ${typeCounts.creatures}`,
              typeCounts.instants > 0 && `Instants: ${typeCounts.instants}`,
              typeCounts.sorceries > 0 && `Sorceries: ${typeCounts.sorceries}`,
              typeCounts.artifacts > 0 && `Artifacts: ${typeCounts.artifacts}`,
              typeCounts.enchantments > 0 && `Enchantments: ${typeCounts.enchantments}`,
              typeCounts.planeswalkers > 0 && `Planeswalkers: ${typeCounts.planeswalkers}`,
              typeCounts.lands > 0 && `Lands: ${typeCounts.lands}`,
              typeCounts.other > 0 && `Other: ${typeCounts.other}`
            ].filter(Boolean).join(', ')}
          </p>
        )}
      </div>
      
      <div>
        <label htmlFor="deck-text-export" style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
          MTGO Format Text:
        </label>
        <textarea
          id="deck-text-export"
          value={formattedText}
          readOnly
          onClick={(e) => (e.target as HTMLTextAreaElement).select()}
          style={{ 
            width: '100%', 
            minHeight: '400px',
            fontFamily: 'Consolas, Monaco, "Courier New", monospace',
            fontSize: '14px',
            lineHeight: '1.4'
          }}
        />
      </div>
      
      <div className="modal-button-container">
        <button
          className={getCopyButtonClass()}
          onClick={handleCopyToClipboard}
          disabled={copyStatus === 'copying'}
        >
          {getCopyButtonText()}
        </button>
        <button
          className="modal-button"
          onClick={onClose}
        >
          Close
        </button>
      </div>
      
      {copyStatus === 'success' && (
        <p style={{ color: '#28a745', fontSize: '14px', margin: '8px 0 0 0' }}>
          ✓ Deck text has been copied to your clipboard and is ready to paste into MTGO or other applications.
        </p>
      )}
      
      {copyStatus === 'error' && (
        <p style={{ color: '#dc3545', fontSize: '14px', margin: '8px 0 0 0' }}>
          ✗ Failed to copy to clipboard. Please manually select and copy the text above.
        </p>
      )}
    </Modal>
  );
};
'''
    
    with open('src/components/TextExportModal.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created src/components/TextExportModal.tsx")

def create_screenshot_modal():
    """Create the ScreenshotModal.tsx file with correct imports and typing"""
    print("📝 Creating ScreenshotModal.tsx...")
    
    content = '''import React, { useState, useMemo } from 'react';
import { Modal } from './Modal';
import { DeckCardInstance, groupInstancesByCardId } from '../types/card';
import { 
  arrangeCardsForScreenshot, 
  generateDeckImage, 
  downloadImage, 
  generateDeckImageFilename,
  getCardQuantityInGroup
} from '../utils/screenshotUtils';

interface ScreenshotModalProps {
  isOpen: boolean;
  onClose: () => void;
  mainDeck: DeckCardInstance[];
  sideboard: DeckCardInstance[];
  deckName?: string;
}

export const ScreenshotModal: React.FC<ScreenshotModalProps> = ({
  isOpen,
  onClose,
  mainDeck,
  sideboard,
  deckName = 'deck'
}) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Arrange cards for screenshot layout
  const layout = useMemo(() => {
    return arrangeCardsForScreenshot(mainDeck, sideboard);
  }, [mainDeck, sideboard]);
  
  // Group cards for quantity calculation
  const mainDeckGroups = useMemo(() => {
    return groupInstancesByCardId(mainDeck);
  }, [mainDeck]);
  
  const sideboardGroups = useMemo(() => {
    return groupInstancesByCardId(sideboard);
  }, [sideboard]);
  
  const handleSaveImage = async () => {
    setIsGenerating(true);
    setError(null);
    
    try {
      const blob = await generateDeckImage('screenshot-preview');
      
      if (blob) {
        const filename = generateDeckImageFilename(deckName);
        downloadImage(blob, filename);
      } else {
        setError('Failed to generate image. Please try again.');
      }
    } catch (err) {
      console.error('Screenshot generation failed:', err);
      setError('An error occurred while generating the image.');
    } finally {
      setIsGenerating(false);
    }
  };
  
  const renderCardStack = (card: DeckCardInstance, groups: Map<string, DeckCardInstance[]>) => {
    const quantity = getCardQuantityInGroup(groups, card.cardId);
    
    return (
      <div key={card.cardId} className="screenshot-card">
        <div className="screenshot-card-name">{card.name}</div>
        <div className="screenshot-card-mana">{card.mana_cost || ''}</div>
        {quantity > 1 && (
          <div className="screenshot-card-quantity">{quantity}</div>
        )}
      </div>
    );
  };
  
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Deck Screenshot"
      size="fullscreen"
      className="screenshot-modal"
    >
      <div id="screenshot-preview" className="screenshot-preview">
        <div style={{ 
          color: '#e0e0e0', 
          fontSize: '20px', 
          fontWeight: 'bold', 
          marginBottom: '16px',
          textAlign: 'center'
        }}>
          {deckName}
        </div>
        
        {/* Main Deck Layout */}
        {layout.mainDeckColumns.some((column: DeckCardInstance[]) => column.length > 0) && (
          <>
            <div style={{ 
              color: '#ccc', 
              fontSize: '16px', 
              marginBottom: '12px',
              fontWeight: '500'
            }}>
              Main Deck ({mainDeck.length} cards)
            </div>
            
            <div className="screenshot-deck-layout">
              {layout.mainDeckColumns.map((column: DeckCardInstance[], columnIndex: number) => (
                <div key={columnIndex} className="screenshot-column">
                  {column.map((card: DeckCardInstance) => renderCardStack(card, mainDeckGroups))}
                </div>
              ))}
            </div>
          </>
        )}
        
        {/* Sideboard Layout */}
        {layout.sideboardColumns.some((column: DeckCardInstance[]) => column.length > 0) && (
          <>
            <div style={{ 
              color: '#ccc', 
              fontSize: '16px', 
              marginBottom: '12px',
              marginTop: '24px',
              fontWeight: '500'
            }}>
              Sideboard ({sideboard.length} cards)
            </div>
            
            <div className="screenshot-sideboard-layout">
              {layout.sideboardColumns.map((column: DeckCardInstance[], columnIndex: number) => (
                <div key={columnIndex} className="screenshot-column">
                  {column.map((card: DeckCardInstance) => renderCardStack(card, sideboardGroups))}
                </div>
              ))}
            </div>
          </>
        )}
        
        {/* Empty state */}
        {mainDeck.length === 0 && sideboard.length === 0 && (
          <div style={{ 
            textAlign: 'center', 
            color: '#666', 
            fontSize: '18px',
            padding: '40px'
          }}>
            No cards in deck
          </div>
        )}
      </div>
      
      {error && (
        <div style={{ 
          color: '#dc3545', 
          fontSize: '14px', 
          margin: '16px 0',
          padding: '8px',
          backgroundColor: 'rgba(220, 53, 69, 0.1)',
          border: '1px solid rgba(220, 53, 69, 0.3)',
          borderRadius: '4px'
        }}>
          {error}
        </div>
      )}
      
      <div className="modal-button-container">
        <button
          className="modal-button primary"
          onClick={handleSaveImage}
          disabled={isGenerating || (mainDeck.length === 0 && sideboard.length === 0)}
        >
          {isGenerating ? 'Generating...' : 'Save Image'}
        </button>
        <button
          className="modal-button"
          onClick={onClose}
        >
          Close
        </button>
      </div>
      
      {isGenerating && (
        <div className="loading-message">
          Generating high-resolution deck image...
        </div>
      )}
    </Modal>
  );
};
'''
    
    with open('src/components/ScreenshotModal.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created src/components/ScreenshotModal.tsx")

def ensure_modal_exists():
    """Ensure Modal.tsx and Modal.css exist with proper casing"""
    print("📝 Ensuring Modal.tsx and Modal.css exist...")
    
    # Modal.tsx
    if not os.path.exists('src/components/Modal.tsx'):
        modal_content = '''import React, { useEffect, useRef } from 'react';
import './Modal.css';

export type ModalSize = 'small' | 'medium' | 'large' | 'fullscreen';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  size?: ModalSize;
  children: React.ReactNode;
  className?: string;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  size = 'medium',
  children,
  className = ''
}) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  // Handle escape key
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      // Focus management
      if (contentRef.current) {
        contentRef.current.focus();
      }
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  // Handle click outside to close
  const handleOverlayClick = (event: React.MouseEvent) => {
    if (event.target === modalRef.current) {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div 
      className="modal-overlay" 
      ref={modalRef}
      onClick={handleOverlayClick}
    >
      <div 
        className={`modal-content modal-${size} ${className}`}
        ref={contentRef}
        tabIndex={-1}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <div className="modal-header">
          <h2 id="modal-title" className="modal-title">{title}</h2>
          <button 
            className="modal-close-btn"
            onClick={onClose}
            aria-label="Close modal"
          >
            ×
          </button>
        </div>
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>
  );
};
'''
        with open('src/components/Modal.tsx', 'w', encoding='utf-8') as f:
            f.write(modal_content)
        print("✅ Created src/components/Modal.tsx")
    
    # Modal.css
    if not os.path.exists('src/components/Modal.css'):
        modal_css = '''/* Modal.css - MTGO-style modal styling */

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  opacity: 0;
  animation: modal-fade-in 0.3s ease forwards;
}

.modal-content {
  background-color: #1a1a1a;
  border: 2px solid #333;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transform: scale(0.9);
  animation: modal-scale-in 0.3s ease forwards;
}

.modal-content:focus {
  outline: none;
}

/* Modal sizes */
.modal-small {
  width: 400px;
  max-width: 90vw;
}

.modal-medium {
  width: 600px;
  max-width: 90vw;
}

.modal-large {
  width: 80vw;
  height: 80vh;
}

.modal-fullscreen {
  width: 95vw;
  height: 95vh;
}

/* Modal header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #333;
  background-color: #2a2a2a;
}

.modal-title {
  margin: 0;
  color: #e0e0e0;
  font-size: 18px;
  font-weight: 600;
}

.modal-close-btn {
  background: none;
  border: none;
  color: #ccc;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.modal-close-btn:hover {
  background-color: #444;
  color: #fff;
}

.modal-close-btn:active {
  background-color: #555;
}

/* Modal body */
.modal-body {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
  color: #e0e0e0;
}

/* Custom scrollbar for modal body */
.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: #2a2a2a;
}

.modal-body::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Animations */
@keyframes modal-fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes modal-scale-in {
  from {
    transform: scale(0.9);
  }
  to {
    transform: scale(1);
  }
}

/* Modal content specific styles */
.modal-body textarea {
  width: 100%;
  min-height: 300px;
  background-color: #2a2a2a;
  border: 1px solid #444;
  border-radius: 4px;
  color: #e0e0e0;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.4;
  padding: 12px;
  resize: vertical;
  outline: none;
}

.modal-body textarea:focus {
  border-color: #666;
  box-shadow: 0 0 0 2px rgba(102, 102, 102, 0.3);
}

.modal-button {
  background-color: #444;
  border: 1px solid #666;
  border-radius: 4px;
  color: #e0e0e0;
  cursor: pointer;
  font-size: 14px;
  padding: 8px 16px;
  transition: all 0.2s ease;
}

.modal-button:hover {
  background-color: #555;
  border-color: #777;
}

.modal-button:active {
  background-color: #333;
  transform: translateY(1px);
}

.modal-button.primary {
  background-color: #0066cc;
  border-color: #0088ff;
}

.modal-button.primary:hover {
  background-color: #0077dd;
  border-color: #0099ff;
}

.modal-button.success {
  background-color: #28a745;
  border-color: #34ce57;
}

.modal-button.success:hover {
  background-color: #34ce57;
  border-color: #40d865;
}

/* Button container */
.modal-button-container {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  justify-content: flex-end;
}

/* Text export specific styles */
.deck-export-info {
  margin-bottom: 16px;
  padding: 12px;
  background-color: #2a2a2a;
  border: 1px solid #444;
  border-radius: 4px;
}

.deck-export-info h4 {
  margin: 0 0 8px 0;
  color: #e0e0e0;
}

.deck-export-info p {
  margin: 4px 0;
  color: #ccc;
  font-size: 14px;
}

/* Screenshot specific styles */
.screenshot-preview {
  background-color: #2a2a2a;
  border: 1px solid #444;
  border-radius: 4px;
  min-height: 400px;
  padding: 16px;
  margin-bottom: 16px;
}

.screenshot-deck-layout {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin-bottom: 20px;
}

.screenshot-sideboard-layout {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.screenshot-column {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.screenshot-card {
  position: relative;
  background-color: #333;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 4px;
  font-size: 12px;
  color: #e0e0e0;
}

.screenshot-card-name {
  font-weight: 500;
  margin-bottom: 2px;
}

.screenshot-card-quantity {
  position: absolute;
  top: 2px;
  right: 4px;
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  border-radius: 2px;
  padding: 1px 4px;
  font-size: 10px;
  font-weight: bold;
}

.loading-message {
  text-align: center;
  color: #ccc;
  padding: 20px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .modal-large,
  .modal-fullscreen {
    width: 95vw;
    height: 90vh;
  }
  
  .modal-content {
    margin: 10px;
  }
  
  .modal-header {
    padding: 12px 16px;
  }
  
  .modal-title {
    font-size: 16px;
  }
  
  .modal-body {
    padding: 16px;
  }
}
'''
        with open('src/components/Modal.css', 'w', encoding='utf-8') as f:
            f.write(modal_css)
        print("✅ Created src/components/Modal.css")

def main():
    """Main function to run all fixes"""
    print("🚀 Comprehensive fix for all import and casing issues...")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('src'):
        print("❌ Error: This script should be run from the project root directory")
        print("   Expected to find 'src' folder")
        return
    
    # Run all fixes
    clean_up_files()
    print()
    
    ensure_modal_exists()
    create_deck_formatting_utils()
    create_screenshot_utils()
    create_text_export_modal()
    create_screenshot_modal()
    
    print()
    print("🎉 All fixes completed!")
    print()
    print("Next steps:")
    print("1. Run: npm install html2canvas @types/html2canvas")
    print("2. Run the integration script: python integrate_export_features_corrected.py")
    print("3. Run: npm start")
    print("4. Test the export features")
    print()
    print("All files now have consistent naming and correct imports!")

if __name__ == '__main__':
    main()
