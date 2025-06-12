import re

def update_collectionarea_mtgo_styling():
    """
    Apply MTGO styling to CollectionArea.tsx header for consistency with DeckArea
    Based on actual current file structure
    """
    
    file_path = "src/components/CollectionArea.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"📁 Reading {file_path}...")
        
        # 1. Replace panel-header class with MTGO header styling
        # Current: <div className="panel-header">
        # Target: <div className="mtgo-header" style={{...mtgo styling...}}>
        
        mtgo_header_style = '''{
        background: 'linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%)',
        border: '1px solid #444',
        borderTop: '1px solid #666',
        boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
        padding: '12px 16px',
        color: '#ffffff',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '16px',
        fontSize: '14px'
      }}'''
        
        # Replace panel-header with MTGO styling
        panel_header_pattern = r'<div className="panel-header">'
        mtgo_header_replacement = f'<div className="mtgo-header" style={mtgo_header_style}>'
        
        if re.search(panel_header_pattern, content):
            content = re.sub(panel_header_pattern, mtgo_header_replacement, content)
            print("✅ Applied MTGO header styling")
        
        # 2. Update h3 title styling to match MTGO theme
        title_pattern = r'(<h3>)'
        title_replacement = r'<h3 style={{fontSize: "16px", fontWeight: "600", color: "#ffffff", textShadow: "0 1px 2px rgba(0,0,0,0.3)", margin: 0}}>'
        
        if re.search(title_pattern, content):
            content = re.sub(title_pattern, title_replacement, content)
            print("✅ Applied MTGO title styling")
        
        # 3. Update view-controls div to match MTGO styling
        view_controls_pattern = r'<div className="view-controls">'
        view_controls_replacement = '''<div className="view-controls" style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        fontSize: '13px'
      }}>'''
        
        if re.search(view_controls_pattern, content):
            content = re.sub(view_controls_pattern, view_controls_replacement, content)
            print("✅ Applied MTGO view controls styling")
        
        # 4. Style the "Size:" and "View:" labels
        size_label_pattern = r'<span>Size: </span>'
        size_label_replacement = '<span style={{color: "#cccccc"}}>Size: </span>'
        
        view_label_pattern = r'<span>View: </span>'
        view_label_replacement = '<span style={{color: "#cccccc"}}>View: </span>'
        
        content = re.sub(size_label_pattern, size_label_replacement, content)
        content = re.sub(view_label_pattern, view_label_replacement, content)
        print("✅ Applied MTGO label styling")
        
        # 5. Apply MTGO button styling to all buttons
        # Define MTGO button style
        mtgo_button_style = '''{
          padding: '4px 8px',
          background: '#333333',
          border: '1px solid #555555',
          color: '#ffffff',
          fontSize: '12px',
          cursor: 'pointer',
          borderRadius: '2px'
        }'''
        
        # Update view mode buttons (Card/List)
        card_button_pattern = r'(<button[\s]*className=\{viewMode === \'grid\' \? \'active\' : \'\'\})'
        card_button_replacement = f'\\1 style={{{mtgo_button_style}, background: viewMode === "grid" ? "#4a4a4a" : "#333333"}}'
        
        list_button_pattern = r'(<button[\s]*className=\{viewMode === \'list\' \? \'active\' : \'\'\})'
        list_button_replacement = f'\\1 style={{{mtgo_button_style}, background: viewMode === "list" ? "#4a4a4a" : "#333333"}}'
        
        content = re.sub(card_button_pattern, card_button_replacement, content)
        content = re.sub(list_button_pattern, list_button_replacement, content)
        print("✅ Applied MTGO button styling to view buttons")
        
        # 6. Update sort button styling
        sort_button_pattern = r'(<button[\s]*className="sort-toggle-btn")'
        sort_button_replacement = f'\\1 style={mtgo_button_style}'
        
        if re.search(sort_button_pattern, content):
            content = re.sub(sort_button_pattern, sort_button_replacement, content)
            print("✅ Applied MTGO styling to sort button")
        
        # 7. Update Load More button styling if present
        load_more_pattern = r'(<button[\s]*className="load-more-results-btn")'
        load_more_replacement = f'\\1 style={{{mtgo_button_style}, padding: "8px 12px"}}'
        
        if re.search(load_more_pattern, content):
            content = re.sub(load_more_pattern, load_more_replacement, content)
            print("✅ Applied MTGO styling to Load More button")
        
        # 8. Update size slider styling to match MTGO theme
        size_slider_pattern = r'className="size-slider"'
        size_slider_replacement = '''className="size-slider" style={{
            width: '80px',
            height: '4px',
            background: '#555555',
            outline: 'none',
            borderRadius: '2px'
          }}'''
        
        if re.search(size_slider_pattern, content):
            content = re.sub(size_slider_pattern, size_slider_replacement, content)
            print("✅ Applied MTGO styling to size slider")
        
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"\n🎉 Successfully updated {file_path}")
        print("📋 Changes applied:")
        print("   • Applied MTGO header styling for consistency")
        print("   • Updated title and label styling with MTGO theme")
        print("   • Applied MTGO button styling to all buttons")
        print("   • Updated size slider styling")
        print("   • Consistent styling with DeckArea and SideboardArea")
        
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
    except Exception as e:
        print(f"❌ Error updating file: {e}")

if __name__ == "__main__":
    update_collectionarea_mtgo_styling()