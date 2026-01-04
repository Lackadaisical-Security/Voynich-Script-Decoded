#!/usr/bin/env python3
"""
Generate SHA-256 checksums for Voynich repository files
By: Lackadaisical Security 2025 - Aurora (Claude)
"""

import hashlib
import json
import os
from pathlib import Path
from datetime import datetime

def calculate_sha256(filepath):
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return "FILE_NOT_FOUND"
    except Exception as e:
        return f"ERROR: {str(e)}"

def get_file_size(filepath):
    """Get file size in human-readable format"""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    except:
        return "N/A"

def main():
    # Files to checksum
    files = [
        "voynich_lexicon_MASTER_FULL_ENHANCED_2025-11-27.json",
        "voynich_manuscript_corpus.json",
        "voynich_complete_lexicon.json",
        "voynich_lexicon_MASTER_2025-10-27.json",
        "voynich_lexicon_MASTER_FULL_2025-11-27.json",
        "tamil_lexicon.json",
        "Voynich_Manuscript_31_STATISTICAL_TESTS.json",
        "voynich_translator_final.py",
        "ultimate_voynich_translator.py",
        "REPRODUCTION_METHODOLOGY.md",
        "REPRODUCTION_VALIDATION_REPORT.md",
        "STATISTICAL_VALIDATION_FINAL.md",
        "VOYNICH_MANUSCRIPT_VALIDATION_REPORT.md"
    ]
    
    results = {
        "generated_date": datetime.utcnow().isoformat() + "Z",
        "algorithm": "SHA-256",
        "files": []
    }
    
    print("=" * 80)
    print("VOYNICH MANUSCRIPT REPOSITORY - FILE INTEGRITY CHECKSUMS")
    print("=" * 80)
    print(f"Generated: {results['generated_date']}")
    print(f"Algorithm: SHA-256")
    print("=" * 80)
    print()
    
    for filepath in files:
        checksum = calculate_sha256(filepath)
        size = get_file_size(filepath)
        
        file_info = {
            "filename": filepath,
            "sha256": checksum,
            "size": size
        }
        results["files"].append(file_info)
        
        print(f"File: {filepath}")
        print(f"  Size: {size}")
        print(f"  SHA-256: {checksum}")
        print()
    
    # Save to JSON
    with open("FILE_CHECKSUMS.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Save to markdown
    with open("FILE_CHECKSUMS.md", "w") as f:
        f.write("# File Integrity Checksums\n\n")
        f.write(f"**Generated:** {results['generated_date']}  \n")
        f.write(f"**Algorithm:** SHA-256  \n\n")
        f.write("## Core Data Files\n\n")
        f.write("| Filename | Size | SHA-256 Checksum |\n")
        f.write("|----------|------|------------------|\n")
        for file_info in results["files"]:
            f.write(f"| `{file_info['filename']}` | {file_info['size']} | `{file_info['sha256']}` |\n")
        f.write("\n## Verification\n\n")
        f.write("**Linux/macOS:**\n```bash\n")
        f.write("# Verify all files\nwhile IFS='|' read -r _ filename _ checksum _; do\n")
        f.write("  filename=$(echo $filename | xargs)\n")
        f.write("  checksum=$(echo $checksum | xargs)\n")
        f.write("  if [[ $filename =~ ^[a-zA-Z] ]]; then\n")
        f.write("    echo \"$checksum  $filename\" | sha256sum -c\n")
        f.write("  fi\n")
        f.write("done < <(grep '|.*\\.' FILE_CHECKSUMS.md | tail -n +2)\n")
        f.write("```\n\n")
        f.write("**Windows PowerShell:**\n```powershell\n")
        f.write("Get-FileHash <filename> -Algorithm SHA256\n")
        f.write("```\n")
    
    print("=" * 80)
    print("✅ Checksums saved to:")
    print("   - FILE_CHECKSUMS.json")
    print("   - FILE_CHECKSUMS.md")
    print("=" * 80)

if __name__ == "__main__":
    main()
