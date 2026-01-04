#!/usr/bin/env python3
"""
ULTIMATE VOYNICH MANUSCRIPT TRANSLATOR
Lackadaisical Security - 2025-01-03

Combines:
- Master lexicon (7,593 entries)
- Tamil Siddha cross-validation
- Sanskrit pre-forms
- Embedded cipher rules
- Morphological decomposition
- Domain-aware sentence generation
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from datetime import datetime


class UltimateVoynichTranslator:
    """
    Complete Voynich translation engine with multi-source validation
    and coherent sentence generation
    """
    
    def __init__(self, 
                 lexicon_path: str,
                 corpus_path: str,
                 tamil_path: str = None,
                 preforms_path: str = None):
        
        print("🔥 ULTIMATE VOYNICH TRANSLATOR v2.0")
        print("="*70)
        
        # Load master lexicon
        self._load_master_lexicon(lexicon_path)
        
        # Load cross-validation sources
        self._load_tamil_lexicon(tamil_path) if tamil_path else None
        self._load_preforms(preforms_path) if preforms_path else None
        
        # Load corpus
        with open(corpus_path, 'r', encoding='utf-8') as f:
            self.corpus = json.load(f)
        
        # Section domain mapping
        self.section_domains = {
            'botanical': range(1, 50),     # f1r - f49v: Herbal medicine
            'astronomical': range(50, 75),  # f50r - f74v: Medical astrology
            'biological': range(75, 90),    # f75r - f89v: Hydrotherapy
            'pharmaceutical': range(90, 200) # f90r+: Recipes
        }
        
        print(f"\n✅ Loaded {len(self.corpus.get('folios', {}))} folios")
        print("="*70)
    
    def _load_master_lexicon(self, path: str):
        """Load master lexicon with verified and full entries"""
        print("\n📚 Loading Master Lexicon...")
        
        with open(path, 'r', encoding='utf-8') as f:
            lex_data = json.load(f)
        
        self.lexicon = {}
        verified_lex = lex_data.get('verified_lexicon', {})
        full_lex_list = lex_data.get('full_lexicon', [])
        
        # Load full lexicon first
        for entry in full_lex_list:
            token = entry.get('token', entry.get('eva', ''))
            if not token:
                continue
            
            english = entry.get('english_meanings', entry.get('english', ''))
            if isinstance(english, list):
                english = english[0] if english else ''
            
            # Skip corrupted long entries
            if isinstance(english, str) and len(english) > 200:
                continue
            
            field = entry.get('semantic_fields', entry.get('field', ''))
            if isinstance(field, list):
                field = field[0] if field else ''
            
            self.lexicon[token] = {
                'token': token,
                'english': english,
                'latin': entry.get('latin_base', ''),
                'field': field,
                'confidence': entry.get('confidence', 0.8),
                'morphology': entry.get('morphology', ''),
                'cipher_rules': entry.get('cipher_rules', []),
                'medical_use': entry.get('medical_use', ''),
                'contextual_variations': entry.get('contextual_variations', {}),
                'etymology': entry.get('etymology', '')
            }
        
        # Overlay verified lexicon (high confidence)
        for token, data in verified_lex.items():
            english = data.get('english', '')
            
            self.lexicon[token] = {
                'token': token,
                'english': english,
                'latin': data.get('latin', ''),
                'field': data.get('field', ''),
                'confidence': data.get('confidence', 1.0),
                'morphology': '',
                'cipher_rules': [],
                'medical_use': '',
                'etymology': data.get('etymology', '')
            }
        
        print(f"  ✓ Loaded {len(self.lexicon)} total entries")
        print(f"    - {len(full_lex_list)} from full lexicon")
        print(f"    - {len(verified_lex)} high-confidence verified")
    
    def _load_tamil_lexicon(self, path: str):
        """Load Tamil Siddha medicine lexicon"""
        if not path:
            self.tamil_lexicon = {}
            return
        
        print("\n🇮🇳 Loading Tamil Siddha Lexicon...")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                tamil_data = json.load(f)
            
            self.tamil_lexicon = {}
            for entry in tamil_data.get('entries', []):
                trans = entry.get('transliteration', '').lower()
                if trans:
                    self.tamil_lexicon[trans] = {
                        'script': entry.get('script_symbol', ''),
                        'translation': entry.get('translation', ''),
                        'pos': entry.get('pos', ''),
                        'semantic_field': entry.get('semantic_field', '')
                    }
            
            print(f"  ✓ Loaded {len(self.tamil_lexicon)} Tamil entries")
        except FileNotFoundError:
            print("  ⚠ Tamil lexicon not found")
            self.tamil_lexicon = {}
    
    def _load_preforms(self, path: str):
        """Load Sanskrit pre-forms for consciousness terminology"""
        if not path:
            self.preforms = {}
            return
        
        print("\n🕉️  Loading Sanskrit Pre-forms...")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                preforms_raw = json.load(f)
            
            self.preforms = {}
            for category in preforms_raw.keys():
                if category.startswith('_'):
                    continue
                
                if isinstance(preforms_raw[category], dict):
                    for key, entry in preforms_raw[category].items():
                        phonetic = entry.get('phonetic', '').lower()
                        if phonetic:
                            self.preforms[phonetic] = {
                                'symbol': entry.get('symbol', ''),
                                'meaning': entry.get('meaning', ''),
                                'function': entry.get('function', ''),
                                'confidence': entry.get('confidence', 0)
                            }
            
            print(f"  ✓ Loaded {len(self.preforms)} Sanskrit pre-forms")
        except FileNotFoundError:
            print("  ⚠ Pre-forms not found")
            self.preforms = {}
    
    def apply_cipher_morphology(self, token: str) -> Tuple[str, List[str]]:
        """
        Apply Voynich cipher morphology rules
        Returns: (base_form, [features])
        """
        features = []
        base = token
        
        # SUFFIX RULES (right to left)
        if base.endswith('aiin'):
            features.append('botanical_medicine')
            base = base[:-4]
        elif base.endswith('saiin'):
            features.append('stem_resin_medicine')
            base = base[:-5]
        elif base.endswith('raiin'):
            features.append('botanical_medicine_extended')
            base = base[:-5]
        elif base.endswith('eedy'):
            features.append('process_intensive')
            base = base[:-4]
        elif base.endswith('edy'):
            features.append('process_verb')
            base = base[:-3]
        elif base.endswith('dy'):
            features.append('completed')
            base = base[:-2]
        elif base.endswith('ky'):
            features.append('celestial_quality')
            base = base[:-2]
        elif base.endswith('ol'):
            features.append('purpose_powder')
            base = base[:-2]
        elif base.endswith('ain'):
            features.append('quality_descriptor')
            base = base[:-3]
        elif base.endswith('eey'):
            features.append('quality_property')
            base = base[:-3]
        elif base.endswith('ey'):
            features.append('adjectival')
            base = base[:-2]
        elif base.endswith('ar'):
            features.append('source_from')
            base = base[:-2]
        elif base.endswith('or'):
            features.append('conjunction_with')
            base = base[:-2]
        
        # PREFIX RULES (left to right)
        if base.startswith('qo'):
            features.insert(0, 'volatile_celestial')
            base = base[2:]
        elif base.startswith('o') and len(base) > 1:
            features.insert(0, 'plant_organic')
            base = base[1:]
        
        if base.startswith('ch'):
            features.insert(0, 'cut_process')
            base = base[2:]
        elif base.startswith('sh'):
            features.insert(0, 'prepared_purified')
            base = base[2:]
        elif base.startswith('d') and len(base) > 1:
            features.insert(0, 'base_root')
            base = base[1:]
        elif base.startswith('s') and len(base) > 1:
            features.insert(0, 'hot_thermal')
            base = base[1:]
        elif base.startswith('t') and len(base) > 1:
            features.insert(0, 'complete_finished')
            base = base[1:]
        elif base.startswith('y') and len(base) > 1:
            features.insert(0, 'quality_adj')
            base = base[1:]
        elif base.startswith('k') and len(base) > 1:
            features.insert(0, 'work_active')
            base = base[1:]
        elif base.startswith('p') and len(base) > 1:
            features.insert(0, 'prepare_make')
            base = base[1:]
        elif base.startswith('f') and len(base) > 1:
            features.insert(0, 'strong_potent')
            base = base[1:]
        
        return base, features
    
    def cleanup_gloss(self, gloss: str, domain: str) -> str:
        """
        Convert technical morphological glosses into natural medical language
        """
        if not gloss:
            return gloss
        
        # Remove corrupted fragments
        corrupted_patterns = [
            r'\(Labels - \d+% of text\):\*\*',
            r'Pentads: do, dol, dor',
            r'\*\*.*?\*\*',  # Any text in **asterisks**
            r'\([^)]*%[^)]*\)',  # Percentage notes in parens
        ]
        
        result = gloss
        for pattern in corrupted_patterns:
            result = re.sub(pattern, '', result)
        
        # Pattern replacements for pharmaceutical/medical context
        patterns = [
            # Process patterns
            (r'cut/process/action\s+for/purpose/tool', 'processing tool'),
            (r'cut/process/action\s+completed', 'extract'),
            (r'cut/process/action', 'extract'),
            (r'to cut/extract/separate', 'extract'),
            
            # Plant/organic patterns
            (r'plant/organic\s+from/source', 'plant extract'),
            (r'plant/organic\s+for/purpose/tool', 'plant preparation'),
            (r'plant/organic', 'plant'),
            
            # Temperature/thermal patterns
            (r'hot/fever/conditional\s+adjectival/of', 'heating property'),
            (r'hot/fever/conditional\s+thermal/complete\s+quality', 'heat treatment'),
            (r'hot/fever/conditional\s+in/within', 'heated'),
            (r'hot/fever/conditional', 'heat'),
            (r'heat/fever\s+source', 'heating'),
            
            # State/quality patterns
            (r'prepared/state/purified\s+quality/property', 'prepared state'),
            (r'prepared/ready\s+state', 'prepared'),
            (r'prepared/ready', 'prepared'),
            (r'quality/with', 'quality'),
            (r'quality/adjectival', 'quality'),
            (r'quality/property', 'property'),
            (r'adjectival/of', 'property'),
            (r'adjectival/genitive', 'of'),
            (r'adjectival', 'property'),
            
            # Foundation/base patterns
            (r'base/foundation/root', 'base'),
            (r'root/seed/base\s+medicine', 'root medicine'),
            
            # Compound patterns
            (r'for/purpose/tool', 'for use'),
            (r'for/purpose', 'for'),
            (r'completed/done', 'finished'),
            (r'and/with', 'with'),
            (r'from/source', 'from'),
            (r'to make/create/calcine', 'make'),
            (r'volatile/celestial/with', 'distilled'),
            (r'celestial/stellar\s+quality', 'stellar'),
            (r'celestial/volatile', 'distilled'),
            
            # Medical terms
            (r'leaf/foliage\s+medicine', 'leaf extract'),
            (r'flower/bloom\s+medicine', 'flower extract'),
            (r'whole\s+plant\s+medicine', 'whole plant'),
            (r'stem/stalk\s+quality', 'stem'),
            (r'medicine/medicinal\s+substance', 'medicine'),
            (r'thermal/complete', 'thermal'),
            (r'thermal\s+process\s+quality', 'heat process'),
            (r'process/make', 'make'),
            
            # Process verbs
            (r'work/action/active', 'work'),
            (r'process/make', 'process'),
        ]
        
        for pattern, replacement in patterns:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # Clean up remaining slashes (choose first option)
        if '/' in result:
            parts = result.split('/')
            result = parts[0].strip()
        
        # Remove extra spaces
        result = re.sub(r'\s+', ' ', result)
        
        return result.strip()
    
    def interpret_features(self, base_meaning: str, features: List[str]) -> str:
        """
        Convert morphological features into natural language interpretation
        """
        if not features:
            return base_meaning
        
        # Feature interpretation mappings
        feature_map = {
            'botanical_medicine': 'medicine',
            'stem_resin_medicine': 'resin extract',
            'botanical_medicine_extended': 'compound medicine',
            'process_intensive': 'thoroughly process',
            'process_verb': 'process',
            'completed': 'finished',
            'celestial_quality': 'lunar/stellar',
            'purpose_powder': 'for use',
            'quality_descriptor': 'quality',
            'quality_property': 'property',
            'adjectival': 'property',
            'source_from': 'from',
            'conjunction_with': 'with',
            'volatile_celestial': 'distilled/mercury',
            'plant_organic': 'plant',
            'cut_process': 'extract',
            'prepared_purified': 'prepared',
            'base_root': 'root',
            'hot_thermal': 'heated',
            'complete_finished': 'completed',
            'quality_adj': 'quality',
            'work_active': 'processed',
            'prepare_make': 'prepare',
            'strong_potent': 'potent'
        }
        
        # Interpret features
        interpreted = []
        for feat in features:
            if feat in feature_map:
                interpreted.append(feature_map[feat])
            else:
                # Keep as-is if no mapping
                interpreted.append(feat)
        
        # Build natural phrase based on feature combinations
        result_parts = []
        
        # Check for common patterns
        if 'plant' in interpreted or 'botanical_medicine' in features:
            result_parts.append('plant')
        
        if 'extract' in interpreted or 'cut_process' in features:
            if base_meaning:
                return f"extract {base_meaning}"
            return "extract"
        
        if 'prepared' in interpreted or 'completed' in interpreted:
            if base_meaning:
                return f"prepared {base_meaning}"
            return "preparation"
        
        if 'medicine' in interpreted:
            if base_meaning and base_meaning != 'medicine':
                return f"{base_meaning} medicine"
            return "medicine"
        
        if 'heated' in interpreted or 'hot_thermal' in features:
            if base_meaning:
                return f"heat {base_meaning}"
            return "heating"
        
        if 'distilled/mercury' in interpreted or 'volatile_celestial' in features:
            if base_meaning:
                return f"distilled {base_meaning}"
            return "distillation"
        
        # Default: combine interpreted features with base
        if interpreted and base_meaning:
            return f"{' '.join(interpreted[:2])} {base_meaning}"
        elif interpreted:
            return ' '.join(interpreted[:2])
        else:
            return base_meaning
    
    def translate_token(self, token: str, context: str = 'general') -> Dict:
        """Translate a single token with all validation sources"""
        token = token.strip().lower()
        
        # PRIORITY 1: Exact lexicon match
        if token in self.lexicon:
            entry = self.lexicon[token]
            
            # Check for context-specific meaning
            if entry.get('contextual_variations'):
                ctx_meaning = entry['contextual_variations'].get(context)
                if ctx_meaning:
                    cleaned = self.cleanup_gloss(ctx_meaning, context)
                    return {
                        'token': token,
                        'english': cleaned,
                        'field': entry['field'],
                        'confidence': entry['confidence'],
                        'source': 'lexicon_contextual'
                    }
            
            # Clean up the english gloss
            cleaned_english = self.cleanup_gloss(entry['english'], context)
            
            return {
                'token': token,
                'english': cleaned_english,
                'latin': entry['latin'],
                'field': entry['field'],
                'confidence': entry['confidence'],
                'morphology': entry['morphology'],
                'source': 'lexicon_direct'
            }
        
        # PRIORITY 2: Morphological decomposition
        base, features = self.apply_cipher_morphology(token)
        
        # Check if base is in lexicon after morphology
        if base in self.lexicon:
            entry = self.lexicon[base]
            # Interpret features into natural language
            interpreted = self.interpret_features(entry['english'], features)
            return {
                'token': token,
                'base': base,
                'base_meaning': entry['english'],
                'english': interpreted,  # Use interpreted version
                'features': features,
                'field': entry['field'],
                'confidence': entry['confidence'] * 0.9,
                'source': 'lexicon_morphological'
            }
        
        # PRIORITY 3: Cross-validation
        # Check Tamil
        if hasattr(self, 'tamil_lexicon') and base in self.tamil_lexicon:
            tamil_entry = self.tamil_lexicon[base]
            interpreted = self.interpret_features(tamil_entry['translation'], features)
            return {
                'token': token,
                'base': base,
                'base_meaning': tamil_entry['translation'],
                'english': interpreted,
                'features': features,
                'field': tamil_entry.get('semantic_field', 'tamil_siddha'),
                'confidence': 0.7,
                'source': 'tamil_crossval'
            }
        
        # Check Sanskrit pre-forms
        if hasattr(self, 'preforms') and base in self.preforms:
            preform = self.preforms[base]
            interpreted = self.interpret_features(preform['meaning'], features)
            return {
                'token': token,
                'base': base,
                'base_meaning': preform['meaning'],
                'english': interpreted,
                'features': features,
                'field': 'sanskrit_consciousness',
                'confidence': preform.get('confidence', 0.6),
                'source': 'sanskrit_preform'
            }
        
        # FALLBACK: Unknown - use feature interpretation
        interpreted = self.interpret_features(base if base else token, features)
        return {
            'token': token,
            'base': base,
            'base_meaning': base if base else token,
            'english': interpreted,
            'features': features,
            'field': 'unknown',
            'confidence': 0.3,
            'source': 'morphological_construct'
        }
    
    def build_coherent_sentence(self, translations: List[Dict], domain: str) -> str:
        """
        Build domain-specific coherent sentence from word translations
        """
        if not translations:
            return ""
        
        # Extract semantic components
        substances = []
        processes = []
        qualities = []
        states = []
        
        for t in translations:
            source = t.get('source', '')
            # Use interpreted 'english' field, fallback to base_meaning
            english = t.get('english', t.get('base_meaning', ''))
            field = t.get('field', '')
            features = t.get('features', [])
            
            if not english:
                continue
            
            # Categorize by field and features
            if field in ['botanical_medicine', 'botanical_part']:
                substances.append(english)
            elif field in ['process_verb', 'process']:
                processes.append(english)
            elif 'medicine' in english.lower():
                substances.append(english)
            elif 'extract' in english.lower() or 'process' in english.lower():
                processes.append(english)
            elif 'quality' in english.lower() or 'property' in english.lower():
                qualities.append(english)
            elif 'prepared' in english.lower() or 'completed' in english.lower():
                states.append(english)
            else:
                # Default: treat as substance/ingredient
                substances.append(english)
        
        # Build sentence per domain
        if domain == 'botanical':
            return self._build_botanical(substances, processes, qualities, states)
        elif domain == 'pharmaceutical':
            return self._build_pharmaceutical(substances, processes, qualities, states)
        elif domain == 'astronomical':
            return self._build_astronomical(substances, processes, qualities, states)
        elif domain == 'biological':
            return self._build_biological(substances, processes, qualities, states)
        else:
            # Generic
            parts = []
            if processes: parts.append(processes[0])
            if substances: parts.append(' + '.join(substances[:2]))
            if qualities: parts.append(f"[{qualities[0]}]")
            return ' '.join(parts) + '.' if parts else "Preparation."
    
    def _build_botanical(self, subs, procs, quals, states):
        """Botanical section: plant identification and uses"""
        if not subs and not procs:
            return "Plant material."
        
        parts = []
        if subs:
            parts.append(subs[0])
            if len(subs) > 1:
                parts.append(f"with {subs[1]}")
        
        if procs:
            parts.append(f"- {procs[0]}")
        
        if quals:
            parts.append(f"({quals[0]})")
        
        result = ' '.join(parts)
        return result + '.' if not result.endswith('.') else result
    
    def _build_pharmaceutical(self, subs, procs, quals, states):
        """Pharmaceutical section: recipes and formulations"""
        if not subs and not procs:
            return "Recipe preparation."
        
        parts = []
        
        if procs:
            parts.append(procs[0].capitalize())
        
        if subs:
            if len(subs) == 1:
                parts.append(subs[0])
            else:
                parts.append(f"{subs[0]} + {subs[1]}")
        
        if states:
            state_clean = states[0].replace('_', ' ')
            parts.append(f"[{state_clean}]")
        
        result = ' '.join(parts)
        return result + '.' if not result.endswith('.') else result
    
    def _build_astronomical(self, subs, procs, quals, states):
        """Astronomical section: timing and celestial references"""
        parts = []
        
        if quals:
            parts.append(f"During {quals[0]}")
        
        if procs:
            parts.append(procs[0])
        
        if subs:
            parts.append(f"with {subs[0]}")
        
        result = ' '.join(parts) if parts else "Celestial timing"
        return result + '.' if not result.endswith('.') else result
    
    def _build_biological(self, subs, procs, quals, states):
        """Biological section: hydrotherapy and baths"""
        parts = []
        
        if procs:
            parts.append(f"{procs[0].capitalize()} treatment")
        
        if subs:
            parts.append(f"using {subs[0]}")
        
        if quals:
            parts.append(f"({quals[0]} temp)")
        
        result = ' '.join(parts) if parts else "Bath preparation"
        return result + '.' if not result.endswith('.') else result
    
    def get_folio_domain(self, folio_id: str) -> str:
        """Determine section domain for a folio"""
        match = re.search(r'f(\d+)', folio_id)
        if not match:
            return 'unknown'
        
        folio_num = int(match.group(1))
        for domain, folio_range in self.section_domains.items():
            if folio_num in folio_range:
                return domain
        return 'unknown'
    
    def translate_folio(self, folio_id: str, max_lines: int = None) -> Dict:
        """Translate complete folio with coherent sentences"""
        if folio_id not in self.corpus.get('folios', {}):
            return {'error': f'Folio {folio_id} not found'}
        
        folio = self.corpus['folios'][folio_id]
        domain = self.get_folio_domain(folio_id)
        
        result = {
            'folio_id': folio_id,
            'domain': domain,
            'metadata': folio.get('metadata', {}),
            'line_count': folio.get('line_count', 0),
            'translations': []
        }
        
        lines = folio.get('lines', [])
        if max_lines:
            lines = lines[:max_lines]
        
        for line_data in lines:
            line_id = line_data.get('line_id', '')
            line_text = line_data.get('text', '')
            
            if not line_text:
                continue
            
            # Split into words
            words = re.split(r'[\s.]+', line_text.strip())
            words = [w for w in words if w]
            
            # Translate each word
            word_trans = [self.translate_token(w, domain) for w in words]
            
            # Build coherent sentence
            sentence = self.build_coherent_sentence(word_trans, domain)
            
            # Calculate coverage
            known_words = sum(1 for t in word_trans if t['confidence'] > 0.5)
            coverage = known_words / len(words) if words else 0
            
            result['translations'].append({
                'line_id': line_id,
                'eva': line_text,
                'word_count': len(words),
                'sentence': sentence,
                'coverage': coverage,
                'avg_confidence': sum(t['confidence'] for t in word_trans) / len(word_trans) if word_trans else 0
            })
        
        return result
    
    def translate_all_folios(self, output_path: str, sample_size: int = None):
        """Translate entire corpus"""
        print(f"\n🚀 TRANSLATING FULL CORPUS")
        print("="*70)
        
        folios = list(self.corpus.get('folios', {}).keys())
        if sample_size:
            folios = folios[:sample_size]
            print(f"🎯 Processing sample: {sample_size} folios")
        else:
            print(f"📊 Processing ALL: {len(folios)} folios")
        
        results = {
            'metadata': {
                'translation_date': datetime.now().isoformat(),
                'translator': 'Lackadaisical Security - Ultimate Engine v2.0',
                'total_folios': len(folios),
                'lexicon_size': len(self.lexicon),
                'tamil_entries': len(getattr(self, 'tamil_lexicon', {})),
                'preform_entries': len(getattr(self, 'preforms', {}))
            },
            'folios': {}
        }
        
        domain_stats = defaultdict(int)
        total_lines = 0
        total_coverage = 0
        
        for i, folio_id in enumerate(folios, 1):
            translation = self.translate_folio(folio_id)
            results['folios'][folio_id] = translation
            
            domain_stats[translation['domain']] += 1
            total_lines += translation['line_count']
            
            # Calculate average coverage for this folio
            if translation['translations']:
                folio_coverage = sum(t['coverage'] for t in translation['translations']) / len(translation['translations'])
                total_coverage += folio_coverage
            
            print(f"  [{i}/{len(folios)}] {folio_id:8s} | {translation['domain']:15s} | {translation['line_count']:3d} lines")
        
        # Save results
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*70)
        print("✅ TRANSLATION COMPLETE!")
        print("="*70)
        print(f"📄 Output: {output_path}")
        print(f"\n📊 Statistics:")
        print(f"  Total folios: {len(folios)}")
        print(f"  Total lines: {total_lines}")
        print(f"  Avg coverage: {total_coverage/len(folios)*100:.1f}%")
        print(f"\n🗂️  By Domain:")
        for domain, count in sorted(domain_stats.items()):
            print(f"    {domain.capitalize():15s}: {count:3d} folios")
        
        return results


def main():
    """Main execution"""
    
    # Initialize translator
    translator = UltimateVoynichTranslator(
        lexicon_path='/mnt/user-data/uploads/voynich_lexicon_MASTER_FULL_ENHANCED_2025-11-27.json',
        corpus_path='/mnt/user-data/uploads/voynich_full_corpus.json',
        tamil_path='/mnt/user-data/uploads/tamil_lexicon.json',
        preforms_path='/mnt/user-data/uploads/pre-forms.json'
    )
    
    # Test with sample folio
    print("\n" + "="*70)
    print("🧪 TEST TRANSLATION")
    print("="*70)
    
    test_result = translator.translate_folio('f100r', max_lines=10)
    
    print(f"\nFolio: {test_result['folio_id']}")
    print(f"Domain: {test_result['domain'].upper()}")
    print(f"Lines: {test_result['line_count']}\n")
    
    for trans in test_result['translations'][:10]:
        print(f"Line {trans['line_id']}")
        print(f"  EVA: {trans['eva'][:60]}{'...' if len(trans['eva']) > 60 else ''}")
        print(f"  →   {trans['sentence']}")
        print(f"      Coverage: {trans['coverage']*100:.0f}% | Confidence: {trans['avg_confidence']:.2f}")
        print()
    
    # Ask for full run
    print("="*70)
    choice = input("\n🔥 Run FULL translation (all 184 folios)? (y/n): ")
    
    if choice.lower() == 'y':
        output_file = '/mnt/user-data/outputs/voynich_ultimate_translation_2025.json'
        translator.translate_all_folios(output_file)
    else:
        print("\n👍 Test complete! Run with 'y' when ready.")


if __name__ == '__main__':
    main()
