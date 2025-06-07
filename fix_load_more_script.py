#!/usr/bin/env python3
"""
Fix Load More coordination between extracted hooks
Addresses the state coordination issue found in Session 1
"""

import os
import re

def read_file(filepath):
    """Read file content safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def write_file(filepath, content):
    """Write file content safely"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False

def fix_useCards_coordinator():
    """Fix the useCards coordinator hook to properly coordinate Load More"""
    
    filepath = "src/hooks/useCards.ts"
    content = read_file(filepath)
    
    if not content:
        return False
    
    # Enhanced useCards coordinator with proper Load More coordination
    new_content = """import { useCallback } from 'react';
import { useSearch } from './useSearch';
import { usePagination } from './usePagination';
import { useCardSelection } from './useCardSelection';
import { useSearchSuggestions } from './useSearchSuggestions';
import { useFilters } from './useFilters';
import type { ScryfallCard, DeckCardInstance } from '../types/car