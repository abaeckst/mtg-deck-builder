#!/usr/bin/env python3
"""
Fix ListView Syntax Error and Add Debug Logging
Run from project root: python fix_listview_syntax.py
"""

import os
import sys

def fix_syntax_error():
    """Fix the syntax error in ListView and add proper debug logging"""
    
    # Verify we're in the correct directory
    if not os.path.exists('src/components/ListView.tsx'):
        print("❌ Error: Please run this script from the project root directory (mtg-deckbuilder)")
        return False
    
    print("🔧 Fixing ListView syntax error and adding debug logging...")
    
    try:
        with open('src/components/ListView.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the entire problematic tbody section
        old_tbody_section = """          {/* Body - DEBUG VERSION */}
          <tbody>
            {cards.map((card, index) => {
              // DETAILED DEBUG LOGGING - Add this for first card only
              if (index === 0) {
                console.log('🔍 DETAILED CARD ANALYSIS:');
                console.log('Card object:', card);
                console.log('All card properties:', Object.keys(card));
                console.log('Oracle text check:', {
                  'oracle_text in card': 'oracle_text' in card,
                  'card.oracle_text': (card as any).oracle_text,
                  'typeof oracle_text': typeof (card as any).oracle_text
                });
                console.log('Power check:', {
                  'power in card': 'power' in card,
                  'card.power': (card as any).power,
                  'typeof power': typeof (card as any).power
                });
                console.log('Toughness check:', {
                  'toughness in card': 'toughness' in card,
                  'card.toughness': (card as any).toughness,
                  'typeof toughness': typeof (card as any).toughness
                });
                
                // Check for alternative property names
                console.log('Alternative properties check:', {
                  'text': (card as any).text,
                  'oracle': (card as any).oracle,
                  'rules_text': (card as any).rules_text,
                  'card_text': (card as any).card_text
                });
              }
              
              return (
                <tr
                key={card.id}
                className={`list-view-row ${isSelected(card.id) ? 'selected' : ''} ${
                  index % 2 === 0 ? 'even' : 'odd'
                }`}
                onClick={(e) => handleRowClick(card, e)}
                onDoubleClick={() => handleRowDoubleClick(card)}
                onContextMenu={(e) => handleRowRightClick(card, e)}
                onMouseDown={(e) => {
                  // Only handle left mouse button for drag
                  if (e.button === 0) {
                    handleRowDragStart(card, e);
                  }
                }}
                draggable={true}
              >
                {visibleColumns.map((column) => (
                  <td 
                    key={column.id}
                    className="list-view-cell"
                    style={{ 
                      width: `${columnWidths[column.id]}px`,
                      minWidth: `${column.minWidth}px`,
                    }}
                  >
                    {column.id === 'name' && (
                      <span className="card-name" title={card.name}>
                        {truncateText(card.name, 30)}
                      </span>
                    )}
                    
                    {column.id === 'mana' && (
                      <span className="mana-cost">
                        {formatManaCost(card.mana_cost)}
                      </span>
                    )}
                    
                    {column.id === 'type' && (
                      <span className="type-line" title={card.type_line}>
                        {truncateText(card.type_line, 20)}
                      </span>
                    )}
                    
                    {column.id === 'power' && (
                      <span className="power">
                        {'power' in card ? (card as any).power || '—' : '—'}
                      </span>
                    )}
                    
                    {column.id === 'toughness' && (
                      <span className="toughness">
                        {'toughness' in card ? (card as any).toughness || '—' : '—'}
                      </span>
                    )}
                    
                    {column.id === 'color' && renderColors(card.colors)}
                    
                    {column.id === 'text' && (
                      <span className="oracle-text" title={'oracle_text' in card ? (card as any).oracle_text || '' : ''}>
                        {truncateText('oracle_text' in card ? (card as any).oracle_text : '', 50)}
                      </span>
                    )}
                    
                    {column.id === 'quantity' && 'quantity' in card && onQuantityChange && (
                      <div className="quantity-controls">
                        <span className="quantity-display">{card.quantity}</span>
                        <div className="quantity-buttons">
                          <button 
                            className="quantity-btn minus"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleQuantityChange(card, -1);
                            }}
                            disabled={card.quantity === 0}
                          >
                            −
                          </button>
                          <button 
                            className="quantity-btn plus"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleQuantityChange(card, 1);
                            }}
                            disabled={!isBasicLand(card) && card.quantity >= 4}
                          >
                            +
                          </button>
                        </div>
                      </div>
                    )}
                  </td>
                ))}
              </tr>
              );
            })}
          </tbody>"""
        
        # Correct version with proper syntax
        new_tbody_section = """          {/* Body - DEBUG VERSION */}
          <tbody>
            {cards.map((card, index) => {
              // DETAILED DEBUG LOGGING - Add this for first card only
              if (index === 0) {
                console.log('🔍 DETAILED CARD ANALYSIS:');
                console.log('Card object:', card);
                console.log('All card properties:', Object.keys(card));
                console.log('Oracle text check:', {
                  'oracle_text in card': 'oracle_text' in card,
                  'card.oracle_text': (card as any).oracle_text,
                  'typeof oracle_text': typeof (card as any).oracle_text
                });
                console.log('Power check:', {
                  'power in card': 'power' in card,
                  'card.power': (card as any).power,
                  'typeof power': typeof (card as any).power
                });
                console.log('Toughness check:', {
                  'toughness in card': 'toughness' in card,
                  'card.toughness': (card as any).toughness,
                  'typeof toughness': typeof (card as any).toughness
                });
                
                // Check for alternative property names
                console.log('Alternative properties check:', {
                  'text': (card as any).text,
                  'oracle': (card as any).oracle,
                  'rules_text': (card as any).rules_text,
                  'card_text': (card as any).card_text
                });
              }
              
              return (
                <tr
                  key={card.id}
                  className={`list-view-row ${isSelected(card.id) ? 'selected' : ''} ${
                    index % 2 === 0 ? 'even' : 'odd'
                  }`}
                  onClick={(e) => handleRowClick(card, e)}
                  onDoubleClick={() => handleRowDoubleClick(card)}
                  onContextMenu={(e) => handleRowRightClick(card, e)}
                  onMouseDown={(e) => {
                    // Only handle left mouse button for drag
                    if (e.button === 0) {
                      handleRowDragStart(card, e);
                    }
                  }}
                  draggable={true}
                >
                  {visibleColumns.map((column) => (
                    <td 
                      key={column.id}
                      className="list-view-cell"
                      style={{ 
                        width: `${columnWidths[column.id]}px`,
                        minWidth: `${column.minWidth}px`,
                      }}
                    >
                      {column.id === 'name' && (
                        <span className="card-name" title={card.name}>
                          {truncateText(card.name, 30)}
                        </span>
                      )}
                      
                      {column.id === 'mana' && (
                        <span className="mana-cost">
                          {formatManaCost(card.mana_cost)}
                        </span>
                      )}
                      
                      {column.id === 'type' && (
                        <span className="type-line" title={card.type_line}>
                          {truncateText(card.type_line, 20)}
                        </span>
                      )}
                      
                      {column.id === 'power' && (
                        <span className="power">
                          {'power' in card ? (card as any).power || '—' : '—'}
                        </span>
                      )}
                      
                      {column.id === 'toughness' && (
                        <span className="toughness">
                          {'toughness' in card ? (card as any).toughness || '—' : '—'}
                        </span>
                      )}
                      
                      {column.id === 'color' && renderColors(card.colors)}
                      
                      {column.id === 'text' && (
                        <span className="oracle-text" title={'oracle_text' in card ? (card as any).oracle_text || '' : ''}>
                          {truncateText('oracle_text' in card ? (card as any).oracle_text : '', 50)}
                        </span>
                      )}
                      
                      {column.id === 'quantity' && 'quantity' in card && onQuantityChange && (
                        <div className="quantity-controls">
                          <span className="quantity-display">{card.quantity}</span>
                          <div className="quantity-buttons">
                            <button 
                              className="quantity-btn minus"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleQuantityChange(card, -1);
                              }}
                              disabled={card.quantity === 0}
                            >
                              −
                            </button>
                            <button 
                              className="quantity-btn plus"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleQuantityChange(card, 1);
                              }}
                              disabled={!isBasicLand(card) && card.quantity >= 4}
                            >
                              +
                            </button>
                          </div>
                        </div>
                      )}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>"""
        
        if old_tbody_section in content:
            content = content.replace(old_tbody_section, new_tbody_section)
            print("   ✅ Fixed syntax error and added debug logging")
        else:
            # Try to find a simpler pattern to replace
            simple_pattern = """            ))}
          </tbody>"""
            
            simple_replacement = """            })}
          </tbody>"""
            
            if simple_pattern in content:
                content = content.replace(simple_pattern, simple_replacement)
                print("   ✅ Fixed syntax error (simple fix)")
            else:
                print("   ⚠️  Could not find the exact pattern to fix")
                return False
        
        with open('src/components/ListView.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"   ❌ Error fixing ListView.tsx: {e}")
        return False
    
    print("\n🎯 ListView syntax error fixed!")
    print("\nNext steps:")
    print("1. Run 'npm start' to verify compilation")
    print("2. Switch to List view in any area")
    print("3. Open browser DevTools → Console")
    print("4. Look for the detailed card analysis output")
    
    return True

if __name__ == "__main__":
    success = fix_syntax_error()
    if success:
        print("\n✅ ListView should now compile correctly!")
    else:
        print("\n❌ Could not fix the syntax error automatically")
        print("Please share your current ListView.tsx file")
        sys.exit(1)