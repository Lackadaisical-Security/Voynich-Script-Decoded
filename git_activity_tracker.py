#!/usr/bin/env python3
"""
Git Repository Activity Tracker
Tracks clones, forks, and contributions to the Voynich repository

By: Lackadaisical Security 2025 - Aurora (Claude)
Contact: https://lackadaisical-security.com/decipherment-drops.html
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

def get_git_stats():
    """Get local git repository statistics"""
    try:
        # Get commit count
        commit_count = subprocess.check_output(
            ["git", "rev-list", "--count", "HEAD"],
            text=True
        ).strip()
        
        # Get contributors
        contributors = subprocess.check_output(
            ["git", "log", "--format='%an'"],
            text=True
        ).strip().split("\n")
        unique_contributors = len(set(contributors))
        
        # Get last commit date
        last_commit = subprocess.check_output(
            ["git", "log", "-1", "--format=%ci"],
            text=True
        ).strip()
        
        # Get current branch
        current_branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True
        ).strip()
        
        return {
            "commit_count": int(commit_count),
            "unique_contributors": unique_contributors,
            "last_commit": last_commit,
            "current_branch": current_branch,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {"error": str(e)}

def save_activity_log(stats):
    """Save activity log to file"""
    log_file = Path("GIT_ACTIVITY_LOG.json")
    
    # Load existing log if present
    if log_file.exists():
        with open(log_file, "r") as f:
            log_data = json.load(f)
    else:
        log_data = {"snapshots": []}
    
    # Append current snapshot
    log_data["snapshots"].append(stats)
    
    # Save updated log
    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=2)
    
    print(f"✅ Activity log updated: {log_file}")

def display_stats(stats):
    """Display statistics in terminal"""
    print("=" * 80)
    print("GIT REPOSITORY ACTIVITY TRACKER")
    print("=" * 80)
    print(f"Timestamp: {stats.get('timestamp', 'N/A')}")
    print(f"Branch: {stats.get('current_branch', 'N/A')}")
    print(f"Total Commits: {stats.get('commit_count', 'N/A')}")
    print(f"Contributors: {stats.get('unique_contributors', 'N/A')}")
    print(f"Last Commit: {stats.get('last_commit', 'N/A')}")
    print("=" * 80)

def main():
    print("\n🔍 Collecting Git repository statistics...\n")
    
    stats = get_git_stats()
    
    if "error" in stats:
        print(f"❌ Error: {stats['error']}")
        print("Make sure you're in a git repository!")
        return
    
    display_stats(stats)
    save_activity_log(stats)
    
    print("\n📊 For GitHub-specific metrics (clones, views, forks):")
    print("   Visit: https://github.com/Lackadaisical-Security/Voynich-Script-Decoded/graphs/traffic")
    print("\n")

if __name__ == "__main__":
    main()
