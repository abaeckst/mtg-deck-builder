import React, { useState, useEffect, useMemo } from 'react';
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
      {/* Copy button positioned at top right */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', marginTop: '-10px' }}>
        <div></div> {/* Spacer */}
        <button
          className={getCopyButtonClass()}
          onClick={handleCopyToClipboard}
          disabled={copyStatus === 'copying'}
        >
          {getCopyButtonText()}
        </button>
      </div>
      
      {copyStatus === 'success' && (
        <p style={{ color: '#28a745', fontSize: '14px', margin: '0 0 20px 0' }}>
          ✓ Deck text has been copied to your clipboard and is ready to paste into MTGO or other applications.
        </p>
      )}
      
      {copyStatus === 'error' && (
        <p style={{ color: '#dc3545', fontSize: '14px', margin: '0 0 20px 0' }}>
          ✗ Failed to copy to clipboard. Please manually select and copy the text below.
        </p>
      )}
      
      {/* MTGO Format Text */}
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
      
      {/* Close button at bottom */}
      <div className="modal-button-container" style={{ marginTop: '20px' }}>
        <button
          className="modal-button"
          onClick={onClose}
        >
          Close
        </button>
      </div>
    </Modal>
  );
};