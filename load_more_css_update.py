#!/usr/bin/env python3

import os
import sys

def update_mtgo_css():
    """Add enhanced Load More button styles for collection area placement"""
    
    filename = "src/components/MTGOLayout.css"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if Load More styles already exist
    if '.load-more-section' in content:
        print("✅ Load More styles already exist in CSS")
        print("✅ No CSS changes needed")
        return True
    
    # Add Load More styles at the end of the file
    load_more_css = '''

/* Load More Results Section */
.load-more-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  margin-top: 16px;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  border: 1px solid #444;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.load-more-results-btn {
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  color: white;
  border: 1px solid #0077dd;
  border-radius: 6px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 200px;
  text-align: center;
}

.load-more-results-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #0077dd 0%, #0055aa 100%);
  border-color: #0088ee;
  box-shadow: 0 2px 8px rgba(0, 119, 221, 0.3);
  transform: translateY(-1px);
}

.load-more-results-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(0, 119, 221, 0.2);
}

.load-more-results-btn:disabled {
  background: #666;
  border-color: #555;
  cursor: not-allowed;
  opacity: 0.6;
}

.loading-progress {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  min-width: 300px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #333;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid #555;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #0066cc 0%, #00aaff 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
  box-shadow: 0 0 8px rgba(0, 170, 255, 0.4);
}

.progress-text {
  color: #ccc;
  font-size: 13px;
  font-weight: 500;
  text-align: center;
}

/* Collection area specific positioning */
.mtgo-collection-area .load-more-section {
  margin: 16px 8px 8px 8px;
  background: rgba(26, 26, 26, 0.95);
  backdrop-filter: blur(4px);
}

/* Responsive design for Load More */
@media (max-width: 768px) {
  .load-more-section {
    padding: 16px;
    margin-top: 12px;
  }
  
  .load-more-results-btn {
    padding: 10px 20px;
    font-size: 13px;
    min-width: 180px;
  }
  
  .loading-progress {
    min-width: 250px;
  }
}'''
    
    # Add the styles to the end of the file
    content += load_more_css
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    print("✅ Added Load More button styles")
    print("✅ Styles include hover effects, progress bar, and responsive design")
    return True

if __name__ == "__main__":
    success = update_mtgo_css()
    sys.exit(0 if success else 1)