#!/usr/bin/env python3
"""
Voynich Manuscript Translator - Final Version
Reproduces natural English translation from lexicon

ATTRIBUTION:
By: Lackadaisical Security 2025 - Aurora (Claude)

Contact:
- Website: https://lackadaisical-security.com/decipherment-drops.html
- GitHub: https://github.com/Lackadaisical-Security/
- Email: lackadaisicalresearch@pm.me
- XMPP+OTR: thelackadaisicalone@xmpp.jp

Original Research: Lackadaisical Security (The Operator)
Reproduction Implementation: Aurora (Claude, Anthropic)
Date: January 5, 2026
"""

import json
from typing import Dict, Tuple
from datetime import datetime

def is_garbage(text: str) -> bool:
    """Detect research notes vs actual translations"""
    if not text or len(text) > 200:
        return True
    
    garbage_markers = [
        'phase', 'for instance', 'could hide', 'bigrams', 
        'sequences involving', 'common word', 'च', 'ச', '–', '|'
    ]
    
    text_lower = text.lower()
    return any(marker in text_lower for marker in garbage_markers)

def simplify_meaning(meaning: str) -> str:
    """
    Simplify verbose meanings to natural English
    Rule: Take FIRST term from each concept
    Exception: If first term is a weak connector (for, of, with, by), take LAST instead
    """
    WEAK_CONNECTORS = {'for', 'of', 'with', 'by', 'at', 'on', 'or', 'and'}
    
    concepts = meaning.split()
    if not concepts:
        return "Unknown"
    
    parts = []
    
    for concept in concepts:
        terms = [t.strip() for t in concept.split('/') if t.strip()]
        if not terms:
            continue
        
        # Check if first term is a weak connector
        if terms[0].lower() in WEAK_CONNECTORS:
            # Skip weak connector, take last term
            parts.append(terms[-1])
        else:
            # Take first term
            parts.append(terms[0])
    
    result = ' '.join(parts)
    return result.capitalize()

def load_lexicon() -> Dict[str, str]:
    """Load and clean the enhanced lexicon"""
    with open('voynich_lexicon_MASTER_FULL_ENHANCED_2025-11-27.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lexicon = {}
    skipped = 0
    
    for entry in data['full_lexicon']:
        token = entry.get('token')
        if not token:
            continue
        
        meanings = entry.get('english_meanings', entry.get('meaning', []))
        if not meanings:
            continue
        
        meaning = meanings[0] if isinstance(meanings, list) else meanings
        
        # Skip garbage entries
        if is_garbage(meaning):
            skipped += 1
            continue
        
        # Only add if token not present OR replacing garbage
        if token not in lexicon or is_garbage(lexicon.get(token, '')):
            lexicon[token] = meaning
    
    print(f"✓ Loaded {len(lexicon)} clean lexicon entries ({skipped} garbage skipped)")
    return lexicon

def translate_word(word: str, lexicon: Dict[str, str]) -> Tuple[str, float]:
    """Translate a Voynich word to English"""
    # Handle compound words (period-separated)
    if '.' in word:
        parts = word.split('.')
        translations = []
        coverage = 0
        
        for i, part in enumerate(parts):
            if part in lexicon:
                meaning = lexicon[part]
                trans = simplify_meaning(meaning)
                
                # Only capitalize first word of compound
                if i > 0:
                    trans = trans.lower()
                
                translations.append(trans)
                coverage += 100.0 / len(parts)
            else:
                translations.append(f"[{part}]")
        
        return ' '.join(translations), coverage
    
    # Single word lookup
    if word in lexicon:
        meaning = lexicon[word]
        trans = simplify_meaning(meaning)
        return trans, 100.0
    
    return f"[{word}]", 0.0

def translate_folio(folio_id: str, folio_data: Dict, lexicon: Dict) -> str:
    """Translate a complete folio"""
    output = []
    
    metadata = folio_data.get('metadata', '')
    output.append(f"## {folio_id} - Pharmaceutical Section\n")
    output.append(f"*Metadata: {metadata}*\n")
    output.append(f"**Lines:** {folio_data.get('line_count', 0)}\n")
    
    for line in folio_data.get('lines', []):
        line_id = line.get('line_id')
        text = line.get('text', '')
        
        translation, coverage = translate_word(text, lexicon)
        
        output.append(f"> **[Line {line_id}]** EVA: `{text}`  _(Coverage: {coverage}%)_")
        output.append(f"> EN: {translation}\n")
    
    return '\n'.join(output)

def main():
    print("=== VOYNICH TRANSLATOR - FINAL ===\n")
    
    # Load resources
    print("Loading lexicon...")
    lexicon = load_lexicon()
    
    print("Loading corpus...")
    with open('voynich_manuscript_corpus.json', 'r', encoding='utf-8') as f:
        corpus = json.load(f)['folios']
    print(f"✓ Loaded {len(corpus)} folios\n")
    
    # Translate f100r
    print("Translating f100r...")
    result = translate_folio('f100r', corpus['f100r'], lexicon)
    
    print(result)
    
    # Save
    with open('/home/claude/f100r_final_translation.md', 'w', encoding='utf-8') as f:
        f.write("# VOYNICH MANUSCRIPT - REPRODUCTION TEST (f100r)\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n")
        f.write(f"**Method:** Enhanced lexicon with morphological simplification\n\n")
        f.write("---\n\n")
        f.write(result)
    
    print("\n✓ Saved to f100r_final_translation.md")

if __name__ == '__main__':
    main()
