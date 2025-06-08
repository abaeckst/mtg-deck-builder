#!/usr/bin/env python3

import os
import sys

def create_load_more_css():
    """Create the load_more_styles.css file in project root"""
    
    load_more_css_content = """/* Load More Results Functionality */
.load-more-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  border-top: 1px solid #3a3a3a;
  background-color: #1e1e1e;
  margin-top: 8px;
}

.load-more-results-btn {
  background: linear-gradient(135deg, #2d5aa0 0%, #1e3d72 100%);
  color: white;
  border: 1px solid #4a7bc8;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.load-more-results-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #3d6ab0 0%, #2e4d82 100%);
  border-color: #5a8bd8;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
  transform: translateY(-1px);
}

.load-more-results-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.load-more-results-btn:disabled {
  background: #444;
  border-color: #555;
  color: #888;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.loading-progress {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: 300px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #333;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2d5aa0 0%, #4a7bc8 50%, #2d5aa0 100%);
  background-size: 200% 100%;
  animation: progressPulse 2s ease-in-out infinite;
  transition: width 0.3s ease;
}

@keyframes progressPulse {
  0%, 100% { background-position: 200% 0; }
  50% { background-position: 0% 0; }
}

.progress-text {
  color: #ccc;
  font-size: 13px;
  font-weight: 500;
}

.pagination-info {
  color: #888;
  font-weight: normal;
  font-size: 0.9em;
}"""
    
    filename = "load_more_styles.css"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(load_more_css_content)
        print(f"✅ Created {filename} ({len(load_more_css_content)} characters)")
        return True
    except Exception as e:
        print(f"❌ Error creating {filename}: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Creating Load More CSS Styles")
    print("=" * 40)
    
    if not os.path.exists("package.json"):
        print("❌ Error: This doesn't appear to be the project root directory")
        print("Please run this script from your project root")
        sys.exit(1)
    
    success = create_load_more_css()
    
    if success:
        print("\n🎉 Load More CSS file created successfully!")
        print("\nNext step: Run the CSS merge script:")
        print("python merge_load_more_css.py")
    
    sys.exit(0 if success else 1)