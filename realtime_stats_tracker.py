#!/usr/bin/env python3
"""
Real-Time Repository Statistics Tracker
Tracks local git stats and queries GitHub API for live metrics

By: Lackadaisical Security 2025 - Aurora (Claude)
Contact: https://lackadaisical-security.com/decipherment-drops.html
"""

import subprocess
import json
import os
from datetime import datetime, timedelta, UTC
from pathlib import Path
import urllib.request
import urllib.error

class RepoStatsTracker:
    def __init__(self, repo_owner="Lackadaisical-Security", repo_name="Voynich-Script-Decoded"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_api_base = "https://api.github.com"
        self.stats_file = Path("REALTIME_STATS.json")
        self.history_file = Path("STATS_HISTORY.json")
        
    def get_github_token(self):
        """Try to get GitHub token from environment"""
        return os.environ.get('GITHUB_TOKEN', None)
    
    def github_api_request(self, endpoint):
        """Make GitHub API request with optional authentication"""
        url = f"{self.github_api_base}{endpoint}"
        headers = {'Accept': 'application/vnd.github.v3+json'}
        
        token = self.get_github_token()
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            # Try to get detailed error message from response body
            error_msg = None
            try:
                error_body = e.read().decode()
                error_data = json.loads(error_body)
                error_msg = error_data.get('message', '')
            except:
                pass
            
            if e.code == 403:
                if error_msg:
                    print(f"⚠️  GitHub API error (403): {error_msg}")
                    if 'rate limit' in error_msg.lower():
                        print(f"💡 Set GITHUB_TOKEN env var for higher rate limits.")
                    elif 'credentials' in error_msg.lower() or 'token' in error_msg.lower():
                        print(f"💡 Check that GITHUB_TOKEN has the correct permissions.")
                else:
                    print(f"⚠️  GitHub API access denied (403). Set GITHUB_TOKEN env var with proper permissions.")
                return None
            elif e.code == 404:
                print(f"⚠️  GitHub API endpoint not found (404): {endpoint}")
                return None
            else:
                if error_msg:
                    print(f"⚠️  GitHub API error {e.code}: {error_msg}")
                else:
                    print(f"⚠️  GitHub API error {e.code}: {e.reason}")
                return None
        except Exception as e:
            print(f"⚠️  Error fetching from GitHub API: {e}")
            return None
    
    def get_local_git_stats(self):
        """Get local git repository statistics"""
        try:
            # Get commit count
            commit_count = subprocess.check_output(
                ["git", "rev-list", "--count", "HEAD"],
                text=True, stderr=subprocess.DEVNULL
            ).strip()
            
            # Get contributors
            contributors = subprocess.check_output(
                ["git", "log", "--format=%an"],
                text=True, stderr=subprocess.DEVNULL
            ).strip().split("\n")
            unique_contributors = len(set(contributors))
            
            # Get last commit info
            last_commit_date = subprocess.check_output(
                ["git", "log", "-1", "--format=%ci"],
                text=True, stderr=subprocess.DEVNULL
            ).strip()
            
            last_commit_msg = subprocess.check_output(
                ["git", "log", "-1", "--format=%s"],
                text=True, stderr=subprocess.DEVNULL
            ).strip()
            
            # Get current branch
            current_branch = subprocess.check_output(
                ["git", "branch", "--show-current"],
                text=True, stderr=subprocess.DEVNULL
            ).strip()
            
            # Get total lines of code (approximation)
            try:
                lines = subprocess.check_output(
                    ["git", "ls-files", "-z"],
                    text=True, stderr=subprocess.DEVNULL
                )
                file_count = len([f for f in lines.split('\0') if f])
            except:
                file_count = 0
            
            return {
                "commit_count": int(commit_count),
                "unique_contributors": unique_contributors,
                "last_commit_date": last_commit_date,
                "last_commit_message": last_commit_msg,
                "current_branch": current_branch,
                "tracked_files": file_count,
                "timestamp": datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }
        except Exception as e:
            print(f"⚠️  Error getting local git stats: {e}")
            return None
    
    def get_github_stats(self):
        """Get GitHub repository statistics via API"""
        stats = {}
        
        # Get repository info
        repo_data = self.github_api_request(f"/repos/{self.repo_owner}/{self.repo_name}")
        if repo_data:
            stats.update({
                "stars": repo_data.get("stargazers_count", 0),
                "watchers": repo_data.get("watchers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "open_issues": repo_data.get("open_issues_count", 0),
                "size_kb": repo_data.get("size", 0),
                "created_at": repo_data.get("created_at", ""),
                "updated_at": repo_data.get("updated_at", ""),
                "default_branch": repo_data.get("default_branch", "main"),
            })
        
        # Get traffic stats (requires push access)
        views_data = self.github_api_request(f"/repos/{self.repo_owner}/{self.repo_name}/traffic/views")
        if views_data:
            stats["views_total"] = views_data.get("count", 0)
            stats["views_unique"] = views_data.get("uniques", 0)
        
        clones_data = self.github_api_request(f"/repos/{self.repo_owner}/{self.repo_name}/traffic/clones")
        if clones_data:
            stats["clones_total"] = clones_data.get("count", 0)
            stats["clones_unique"] = clones_data.get("uniques", 0)
        
        # Get contributors count
        contributors_data = self.github_api_request(f"/repos/{self.repo_owner}/{self.repo_name}/contributors")
        if contributors_data:
            stats["github_contributors"] = len(contributors_data)
        
        # Get releases count
        releases_data = self.github_api_request(f"/repos/{self.repo_owner}/{self.repo_name}/releases")
        if releases_data:
            stats["releases"] = len(releases_data)
        
        return stats
    
    def collect_stats(self):
        """Collect all statistics"""
        print("🔍 Collecting repository statistics...\n")
        
        stats = {
            "timestamp": datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "local": self.get_local_git_stats(),
            "github": self.get_github_stats()
        }
        
        return stats
    
    def save_stats(self, stats):
        """Save current stats and update history"""
        # Save current stats
        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        # Update history
        history = []
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                history = json.load(f)
        
        history.append(stats)
        
        # Keep last 100 snapshots
        history = history[-100:]
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        print(f"✅ Stats saved to {self.stats_file}")
        print(f"✅ History updated in {self.history_file}")
    
    def generate_markdown_badge(self, stats):
        """Generate markdown badges for README"""
        badges = []
        
        if stats.get("github"):
            gh = stats["github"]
            badges.append(f'<img src="https://img.shields.io/github/stars/{self.repo_owner}/{self.repo_name}?style=flat-square">')
            badges.append(f'<img src="https://img.shields.io/github/forks/{self.repo_owner}/{self.repo_name}?style=flat-square">')
            badges.append(f'<img src="https://img.shields.io/github/issues/{self.repo_owner}/{self.repo_name}?style=flat-square">')
            
            if gh.get("views_total"):
                badges.append(f'<img src="https://img.shields.io/badge/views-{gh["views_total"]}-blue?style=flat-square">')
            if gh.get("clones_total"):
                badges.append(f'<img src="https://img.shields.io/badge/clones-{gh["clones_total"]}-green?style=flat-square">')
        
        if stats.get("local"):
            local = stats["local"]
            badges.append(f'<img src="https://img.shields.io/badge/commits-{local["commit_count"]}-orange?style=flat-square">')
        
        return "\n".join(badges)
    
    def display_stats(self, stats):
        """Display statistics in terminal"""
        print("\n" + "=" * 80)
        print("📊 VOYNICH MANUSCRIPT REPOSITORY - REAL-TIME STATISTICS")
        print("=" * 80)
        print(f"⏰ Generated: {stats['timestamp']}")
        print("=" * 80)
        
        # Local stats
        if stats.get("local"):
            print("\n📁 LOCAL GIT STATISTICS:")
            print("-" * 80)
            local = stats["local"]
            print(f"  Branch:             {local.get('current_branch', 'N/A')}")
            print(f"  Total Commits:     {local.get('commit_count', 'N/A')}")
            print(f"  Contributors:      {local.get('unique_contributors', 'N/A')}")
            print(f"  Tracked Files:     {local.get('tracked_files', 'N/A')}")
            print(f"  Last Commit:       {local.get('last_commit_date', 'N/A')}")
            print(f"  Last Message:      {local.get('last_commit_message', 'N/A')[:60]}...")
        
        # GitHub stats
        if stats.get("github"):
            print("\n🌐 GITHUB STATISTICS:")
            print("-" * 80)
            gh = stats["github"]
            print(f"  ⭐ Stars:          {gh.get('stars', 'N/A')}")
            print(f"  🔱 Forks:          {gh.get('forks', 'N/A')}")
            print(f"  👁️  Watchers:       {gh.get('watchers', 'N/A')}")
            print(f"  🐛 Open Issues:    {gh.get('open_issues', 'N/A')}")
            print(f"  📦 Size:           {gh.get('size_kb', 0) / 1024:.2f} MB")
            
            if gh.get('views_total'):
                print(f"  👀 Total Views:    {gh.get('views_total', 'N/A')} (unique: {gh.get('views_unique', 'N/A')})")
            if gh.get('clones_total'):
                print(f"  📥 Total Clones:   {gh.get('clones_total', 'N/A')} (unique: {gh.get('clones_unique', 'N/A')})")
            
            print(f"  👥 Contributors:   {gh.get('github_contributors', 'N/A')}")
            print(f"  🏷️  Releases:       {gh.get('releases', 'N/A')}")
            print(f"  📅 Created:        {gh.get('created_at', 'N/A')[:10]}")
            print(f"  🔄 Last Updated:   {gh.get('updated_at', 'N/A')[:10]}")
        
        print("\n" + "=" * 80)
    
    def generate_stats_markdown(self, stats):
        """Generate markdown file with stats"""
        md = f"""# Repository Statistics - Real-Time

**Last Updated:** {stats['timestamp']}

## 📊 Current Statistics

"""
        
        if stats.get("github"):
            gh = stats["github"]
            md += f"""### GitHub Metrics

| Metric | Value |
|--------|-------|
| ⭐ Stars | {gh.get('stars', 0)} |
| 🔱 Forks | {gh.get('forks', 0)} |
| 👁️ Watchers | {gh.get('watchers', 0)} |
| 🐛 Open Issues | {gh.get('open_issues', 0)} |
| 📦 Repository Size | {gh.get('size_kb', 0) / 1024:.2f} MB |
"""
            
            if gh.get('views_total'):
                md += f"| 👀 Total Views (14 days) | {gh.get('views_total', 0)} ({gh.get('views_unique', 0)} unique) |\n"
            if gh.get('clones_total'):
                md += f"| 📥 Total Clones (14 days) | {gh.get('clones_total', 0)} ({gh.get('clones_unique', 0)} unique) |\n"
            
            md += f"""| 👥 Contributors | {gh.get('github_contributors', 0)} |
| 🏷️ Releases | {gh.get('releases', 0)} |
| 📅 Repository Created | {gh.get('created_at', 'N/A')[:10]} |

"""
        
        if stats.get("local"):
            local = stats["local"]
            md += f"""### Local Repository

| Metric | Value |
|--------|-------|
| 🌿 Current Branch | `{local.get('current_branch', 'N/A')}` |
| 📝 Total Commits | {local.get('commit_count', 0)} |
| 👥 Contributors | {local.get('unique_contributors', 0)} |
| 📄 Tracked Files | {local.get('tracked_files', 0)} |
| 🕐 Last Commit | {local.get('last_commit_date', 'N/A')[:19]} |
| 💬 Last Message | {local.get('last_commit_message', 'N/A')} |

"""
        
        md += f"""---

## 📈 Badges

Add these to your README.md:

```markdown
{self.generate_markdown_badge(stats)}
```

---

**Generated by:** Real-Time Repository Stats Tracker  
**By:** Lackadaisical Security 2025 - Aurora (Claude)  
**Repository:** https://github.com/{self.repo_owner}/{self.repo_name}
"""
        
        with open("REALTIME_STATS.md", 'w') as f:
            f.write(md)
        
        print(f"✅ Markdown report saved to REALTIME_STATS.md")
    
    def run(self):
        """Main execution"""
        stats = self.collect_stats()
        self.display_stats(stats)
        self.save_stats(stats)
        self.generate_stats_markdown(stats)
        
        print("\n💡 TIP: Set GITHUB_TOKEN environment variable for traffic stats:")
        print("   export GITHUB_TOKEN='your_github_token_here'")
        print("\n📊 View detailed stats at:")
        print(f"   https://github.com/{self.repo_owner}/{self.repo_name}/graphs/traffic")
        print("\n")

def main():
    tracker = RepoStatsTracker()
    tracker.run()

if __name__ == "__main__":
    main()
