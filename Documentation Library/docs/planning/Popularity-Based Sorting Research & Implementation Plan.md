# Popularity-Based Sorting Research & Implementation Plan

**Date:** June 2, 2025 
**Status:** Research Complete - Ready for Implementation 
**Priority:** Future Phase 7 Enhancement 

## 🎯 Project Vision

Transform MTG deck builder search results from basic alphabetical/relevance sorting to **competitive play popularity-based ranking**. Users will see the most played cards in their selected format first, revolutionizing the deck building experience.

## 📊 Research Findings

### Data Source Analysis

**Primary Data Source: MTGGoldfish**

- Comprehensive metagame pages for all major formats (Standard, Modern, Pioneer, Historic, Legacy, Vintage, Commander)
- Shows recent tournament results with complete deck lists and player names from leagues and challenges
- Updates frequently with new tournament results from MTGO competitions
- **No official API available** - requires web scraping using tools like Puppeteer/Selenium
- Proven scraping approach: Multiple existing open-source scrapers demonstrate feasibility
  **Secondary Sources Available:**
- **MTGDecks.net:** Claims "more than 9388 decklists published in the last 2 weeks" from multiple sources including Tcgplayer, Mtgtop8, Mtgmelee, Starcitygames, Wizards of the Coast
- **Official MTGO:** Limited scope due to Wizards reducing published decklists (citing format "solving" concerns)
  **Key Technical Insight:** No official APIs exist for metagame data - all implementation requires web scraping with respectful rate limiting.
  
  ### Data Availability & Quality
  
  **Tournament Data Richness:**
- Complete deck lists with card names and quantities
- Tournament placement and player information
- Format-specific results (Standard, Modern, etc.)
- Both competitive tournaments and casual league results
- Historical data for trend analysis
  **Update Frequency:**
- New tournament results published multiple times per week
- 30-day rolling window provides current metagame snapshot
- Weekly data updates sufficient for meaningful popularity tracking
  
  ## 🔧 Technical Implementation Plan
  
  ### Confirmed Technical Decisions
  
  **Popularity Calculation Method: Weighted by Copy Count**
  
  ```typescript
  popularityScore = inclusionPercentage × averageCopiesWhenIncluded
  Example:
  Lightning Bolt: 45% inclusion × 3.2 avg copies = 144 popularity points
  Brainstorm: 12% inclusion × 1.8 avg copies = 21.6 popularity points
  ```
  
  **Data Scope: Comprehensive Tournament Coverage**
- Include ALL published decklists from MTGGoldfish (not just top performers)
- Provides comprehensive view of actual metagame rather than elite-only perspective
- Better represents cards that casual-competitive players encounter
  **Implementation Approach: Hybrid Development**
- Start with local Node.js scraper outputting JSON files
- Frontend reads popularity data from local JSON files
- Validate concept before building full backend infrastructure
- Upgrade to database-backed API service in later phase
  **Format Priority: Standard Format First**
- Most dynamic competitive format for testing
- Fastest iteration and validation cycle
- Expand to other formats after proof of concept
  
  ### Core Architecture Components
  
  **Backend Services (Node.js)**
  
  ```
  /popularity-service/
  ├── scraping/
  │ ├── mtgGoldfishScraper.ts // Puppeteer-based scraper
  │ ├── deckListParser.ts // Extract cards from tournament results
  │ └── dataValidator.ts // Validate scraped data quality
  ├── processing/
  │ ├── popularityCalculator.ts // Calculate weighted popularity scores
  │ ├── formatAnalyzer.ts // Format-specific processing
  │ └── rankingGenerator.ts // Generate format popularity rankings
  └── output/
  ├── jsonExporter.ts // Export to files for frontend
  └── dataManager.ts // Manage data freshness and updates
  ```
  
  **Data Schema**
  
  ```typescript
  interface PopularityData {
  cardName: string;
  scryfallId: string;
  format: string;
  popularityScore: number; // Weighted score (inclusion % × avg copies)
  inclusionPercentage: number; // % of decks containing this card
  averageCopies: number; // Average copies when included
  totalDecksAnalyzed: number; // Sample size for this calculation
  weeklyRank: number; // Rank within format (1 = most popular)
  lastUpdated: Date;
  dataSource: 'mtggoldfish';
  }
  ```
  
  **Frontend Integration Points**
  
  ```typescript
  // Extend existing useSorting.ts hook
  type SortCriteria = 'name' | 'mana' | 'color' | 'rarity' | 'type' | 'popularity';
  // New API service
  interface PopularityService {
  getFormatPopularity(format: string): Promise<PopularityData[]>;
  getCardPopularity(cardName: string, format: string): Promise<PopularityData | null>;
  refreshPopularityData(): Promise<void>;
  }
  ```
  
  ### Development Phases
  
  **Phase 7A: Proof of Concept (2-3 weeks)**
1. **Week 1:** MTGGoldfish scraper development
   - Puppeteer-based scraper for Standard format tournament results
   - Parse deck lists and extract card quantities
   - Output raw tournament data to JSON files
2. **Week 2:** Popularity calculation engine
   - Process raw deck data into popularity scores
   - Calculate inclusion percentages and average copy counts
   - Generate weighted popularity rankings for Standard format
3. **Week 3:** Frontend integration
   - Modify existing React app to read popularity JSON files
   - Add "Popularity" sort option to collection area
   - Integrate with existing useSorting.ts hook
   - Make popularity sorting default for collection area
     **Phase 7B: Backend Service (3-4 weeks)**
- Full Node.js/Express API with database caching
- Automated weekly data collection and processing
- Multiple format support (Modern, Pioneer, Commander)
- RESTful API endpoints for frontend consumption
  **Phase 7C: Advanced Features (2-3 weeks)**
- Visual popularity indicators (badges, tier systems)
- Historical popularity trends
- Format-specific optimizations
- Performance optimization for large datasets
  
  ## 🚀 Implementation Requirements
  
  ### Technical Prerequisites
- Node.js development environment
- Puppeteer for web scraping
- Integration with existing React TypeScript application
- Respectful rate limiting to avoid overwhelming MTGGoldfish servers
  
  ### Rate Limiting & Compliance
- Implement 50-100ms delays between requests (following Scryfall API guidelines)
- Use appropriate User-Agent headers identifying the application
- Monitor for rate limiting responses and implement backoff strategies
- Weekly batch processing during low-traffic hours
  
  ### Data Quality Measures
- Validate scraped data for completeness and accuracy
- Handle missing or malformed deck list data gracefully
- Cross-reference card names with Scryfall API for consistency
- Implement data freshness indicators and fallback mechanisms
  
  ## 📈 Expected User Experience Impact
  
  ### Primary Benefits
1. **Competitive Relevance:** Users see tournament-viable cards first
2. **Meta Awareness:** Deck builders understand current competitive landscape
3. **Discovery Enhancement:** Popular cards users might have missed become visible
4. **Format-Specific Intelligence:** Popularity rankings change based on selected format
   
   ### User Workflow Enhancement
   
   ```
   Current Experience:
   Search "red burn spell" → Alphabetical results → Manual evaluation needed
   Enhanced Experience:
   Search "red burn spell" → Lightning Bolt (85% of decks) → Shock (45% of decks) → etc.
   Collection browsing → Most played cards in format appear first
   ```
   
   ### Visual Design Opportunities
- Popularity percentage badges (e.g., "45% of decks")
- Tier indicators (S/A/B/C ranking system)
- Trending indicators for cards gaining/losing popularity
- Format-specific popularity comparisons
  
  ## 🔄 Future Enhancement Opportunities
  
  ### Advanced Analytics
- Historical popularity trends and meta shifts
- Deck archetype correlation (cards popular together)
- Price correlation with popularity data
- Tournament success correlation with card inclusion
  
  ### Cross-Format Analysis
- Card popularity comparison across formats
- Format rotation impact tracking
- Banned card historical popularity analysis
  
  ### Community Features
- User deck popularity comparison with meta
- Popularity-based deck recommendations
- Meta prediction based on rising card trends
  
  ## 📋 Success Metrics
  
  ### Technical Success Criteria
- Scraper successfully collects 90%+ of published tournament results
- Popularity calculations complete within acceptable time limits (< 5 minutes)
- Frontend integration maintains existing application performance
- Data freshness maintained with weekly updates
  
  ### User Experience Success Criteria
- Collection area defaults to popularity-based sorting
- Search results prioritize competitively relevant cards
- Format-specific popularity rankings provide actionable insights
- No regressions in existing deck building functionality
  
  ## 🎯 Implementation Readiness
  
  **Current Status:** Research Complete - Ready for Implementation 
  **Next Step:** Phase 7A proof of concept development 
  **Prerequisites:** Confirm local development environment setup 
  **Estimated Timeline:** 8-10 weeks for complete implementation (Phases 7A-7C) 
  **Key Decision Points:**
- Local development vs. cloud hosting for scraper service
- JSON file approach vs. database backend for data storage
- Manual vs. automated data update scheduling
- Single format vs. multi-format initial implementation

---

**Documentation Status:** Complete research and planning phase 
**Implementation Priority:** Phase 7 future enhancement 
**Complexity Level:** Advanced - requires backend service development 
**Impact Level:** High - revolutionary enhancement to deck building experience
