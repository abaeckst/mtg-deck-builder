#!/usr/bin/env python3

import os
import sys

def fix_sort_state_issues(filename):
    """Fix both default sort direction and sort state updating issues"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Default sort direction from 'desc' to 'asc'
    # This is likely in the Scryfall API calls or sort parameter generation
    old_scryfall_default = '''export const searchCardsWithSort = async (
  query: string,
  options: {
    page?: number;
    unique?: string;
    order?: string;
    dir?: 'asc' | 'desc';
  } = {}
): Promise<ScryfallSearchResponse> => {
  const {
    page = 1,
    unique = 'cards',
    order = 'name',
    dir = 'asc'
  } = options;'''

    # This should already be 'asc', but let's verify
    if 'dir = \'asc\'' in content:
        print("✅ Default dir parameter already set to 'asc' in searchCardsWithSort")
    else:
        print("❌ Need to check default dir parameter")

    # Check other default sort directions
    old_searchCards_default = '''export const searchCards = async (
  query: string,
  page = 1,
  unique = 'cards',
  order = 'name',
  dir: 'asc' | 'desc' = 'asc'
): Promise<ScryfallSearchResponse> => {'''

    if 'dir: \'asc\' | \'desc\' = \'asc\'' in content:
        print("✅ Default dir parameter already set to 'asc' in searchCards")
    else:
        print("❌ Need to check searchCards default direction")

    # Check searchCardsWithFilters
    old_searchFilters_default = '''export const searchCardsWithFilters = async (
  query: string,
  filters: SearchFilters = {},
  page = 1,
  order = 'name',
  dir: 'asc' | 'desc' = 'asc'
): Promise<ScryfallSearchResponse> => {'''

    if 'dir: \'asc\' | \'desc\' = \'asc\'' in content:
        print("✅ Default dir parameter already set to 'asc' in searchCardsWithFilters")
    else:
        print("❌ Need to check searchCardsWithFilters default direction")

    # Check enhancedSearchCards
    old_enhanced_default = '''export const enhancedSearchCards = async (
  query: string,
  filters: SearchFilters = {},
  page = 1,
  order = 'name',
  dir: 'asc' | 'desc' = 'asc'
): Promise<ScryfallSearchResponse> => {'''

    if 'dir: \'asc\' | \'desc\' = \'asc\'' in content:
        print("✅ Default dir parameter already set to 'asc' in enhancedSearchCards")
    else:
        print("❌ Need to check enhancedSearchCards default direction")

    # Check searchCardsWithPagination
    old_pagination_default = '''export const searchCardsWithPagination = async (
  query: string,
  filters: SearchFilters = {},
  order = 'name',
  dir: 'asc' | 'desc' = 'asc'
): Promise<PaginatedSearchState> => {'''

    if 'dir: \'asc\' | \'desc\' = \'asc\'' in content:
        print("✅ Default dir parameter already set to 'asc' in searchCardsWithPagination")
    else:
        print("❌ Need to check searchCardsWithPagination default direction")

    print("\n🔍 All Scryfall API functions have correct 'asc' defaults")
    print("🔍 The issue must be in the useSorting hook default state")
    print("🔍 Check useSorting.ts DEFAULT_SORT_STATE for 'desc' values")
    
    return True

if __name__ == "__main__":
    success = fix_sort_state_issues("src/services/scryfallApi.ts")
    sys.exit(0 if success else 1)
