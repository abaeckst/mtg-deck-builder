// src/components/CollapsibleSection.tsx - Phase 4B: Reusable collapsible section component
import React from 'react';

interface CollapsibleSectionProps {
  title: string;
  previewText?: string;
  isExpanded: boolean;
  hasActiveFilters: boolean;
  onToggle: () => void;
  children: React.ReactNode;
  className?: string;
}

const CollapsibleSection: React.FC<CollapsibleSectionProps> = ({
  title,
  previewText = '',
  isExpanded,
  hasActiveFilters,
  onToggle,
  children,
  className = ''
}) => {
  return (
    <div className={`collapsible-section ${className}`}>
      <div 
        className={`section-header ${hasActiveFilters ? 'has-active-filters' : ''}`}
        onClick={onToggle}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            onToggle();
          }
        }}
        aria-expanded={isExpanded}
        aria-controls={`section-content-${title.toLowerCase().replace(/\s+/g, '-')}`}
      >
        <span className="section-title">
        {title} <span className="section-preview">{previewText}</span>
      </span>
        <div className="section-indicators">
          {hasActiveFilters && (
            <span 
              className="active-indicator" 
              title="This section has active filters"
              aria-label="Active filters indicator"
            >
              •
            </span>
          )}
          <span className="collapse-indicator">
            {isExpanded ? '[-]' : '[+]'}
          </span>
        </div>
      </div>
      
      {isExpanded && (
        <div 
          className="section-content"
          id={`section-content-${title.toLowerCase().replace(/\s+/g, '-')}`}
          role="region"
          aria-labelledby={`section-header-${title.toLowerCase().replace(/\s+/g, '-')}`}
        >
          {children}
        </div>
      )}
    </div>
  );
};

export default CollapsibleSection;