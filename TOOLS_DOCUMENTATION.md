# Repository Tools Documentation

## Overview

This repository includes comprehensive tools for tracking repository statistics and verifying file integrity. All tools are designed to work with zero external dependencies using only Python standard library.

## 🔐 File Integrity Verification

### `generate_checksums.py`

Generates SHA-256 checksums for all core repository files to verify integrity and detect tampering.

**Usage:**
```bash
./generate_checksums.py
# or
python3 generate_checksums.py
```

**Output:**
- `FILE_CHECKSUMS.json` - Machine-readable checksums
- `FILE_CHECKSUMS.md` - Human-readable checksums with verification instructions

**Files Checked:**
- All JSON lexicons and data files
- Python translator scripts
- Validation and methodology documentation

**Verification:**

Linux/macOS:
```bash
sha256sum -c <(cat FILE_CHECKSUMS.md | grep '|.*\.json' | awk '{print $6 " " $2}')
```

Windows PowerShell:
```powershell
Get-FileHash <filename> -Algorithm SHA256
```

---

## 📊 Repository Statistics Tracking

### `git_activity_tracker.py`

Tracks local git repository activity and maintains a historical log.

**Usage:**
```bash
./git_activity_tracker.py
# or
python3 git_activity_tracker.py
```

**Features:**
- Tracks total commit count
- Counts unique contributors
- Records last commit date and time
- Saves current branch information
- Maintains activity history in `GIT_ACTIVITY_LOG.json`

**Output:**
```
================================================================================
GIT REPOSITORY ACTIVITY TRACKER
================================================================================
Timestamp: 2026-01-04T22:32:11.597217Z
Branch: main
Total Commits: 150
Contributors: 3
Last Commit: 2026-01-04 22:31:53 +0000
================================================================================
✅ Activity log updated: GIT_ACTIVITY_LOG.json
```

---

### `realtime_stats_tracker.py`

Comprehensive statistics tracker that combines local git stats with GitHub API metrics.

**Usage:**
```bash
./realtime_stats_tracker.py
# or
python3 realtime_stats_tracker.py
```

**Features:**

**Local Git Statistics:**
- Current branch
- Total commits
- Unique contributors
- Tracked files count
- Last commit details

**GitHub API Statistics** (requires GITHUB_TOKEN):
- Stars, forks, watchers
- Open issues count
- Repository size
- Traffic stats (views/clones in last 14 days)
- Contributors count
- Releases count
- Creation and update dates

**Environment Variable:**
```bash
export GITHUB_TOKEN='your_github_personal_access_token'
```

**Output Files:**
- `REALTIME_STATS.json` - Current snapshot
- `STATS_HISTORY.json` - Historical tracking (last 100 snapshots)
- `REALTIME_STATS.md` - Human-readable report with badges

**Display:**
```
================================================================================
📊 VOYNICH MANUSCRIPT REPOSITORY - REAL-TIME STATISTICS
================================================================================
⏰ Generated: 2026-01-04T22:32:18.994900Z
================================================================================

📁 LOCAL GIT STATISTICS:
--------------------------------------------------------------------------------
  Branch:             main
  Total Commits:     150
  Contributors:      3
  Tracked Files:     55
  Last Commit:       2026-01-04 22:31:53 +0000
  Last Message:      Add comprehensive statistics tracking...

🌐 GITHUB STATISTICS:
--------------------------------------------------------------------------------
  ⭐ Stars:          245
  🔱 Forks:          18
  👁️  Watchers:       32
  🐛 Open Issues:    3
  📦 Size:           15.23 MB
  👀 Total Views:    1,234 (unique: 567)
  📥 Total Clones:   89 (unique: 45)
  👥 Contributors:   3
  🏷️  Releases:       2
  📅 Created:        2025-08-15
  🔄 Last Updated:   2026-01-04
================================================================================
```

---

## ⚙️ Automated Tracking

### `setup_cron_tracker.sh`

Sets up automated local tracking using cron (Linux/macOS only).

**Usage:**
```bash
./setup_cron_tracker.sh
```

**Configuration:**
- Runs every 6 hours automatically
- Logs output to `stats_tracker.log`
- Can be customized by editing `CRON_SCHEDULE` variable

**Manage Cron:**
```bash
# View current cron jobs
crontab -l

# Edit cron jobs
crontab -e

# Remove all cron jobs (careful!)
crontab -r
```

---

### GitHub Actions Workflow

Automated statistics tracking using GitHub Actions.

**File:** `.github/workflows/stats-tracker.yml`

**Triggers:**
- Every 6 hours (scheduled)
- Manual trigger via GitHub UI
- Push to main branch

**What it does:**
1. Checks out repository with full git history
2. Sets up Python 3.10
3. Runs `realtime_stats_tracker.py` with GitHub token
4. Commits and pushes updated statistics files

**Manual Trigger:**
1. Go to repository on GitHub
2. Click "Actions" tab
3. Select "Repository Statistics Tracker"
4. Click "Run workflow"

---

## 🛠️ Technical Details

### Requirements
- Python 3.6+
- Git
- Internet connection (for GitHub API features)

### Dependencies
**None!** All scripts use Python standard library only:
- `hashlib` - SHA-256 checksums
- `json` - Data serialization
- `subprocess` - Git command execution
- `urllib` - GitHub API requests
- `datetime` - Timestamps
- `pathlib` - File operations

### Security Considerations

**GitHub Token Permissions:**
If setting `GITHUB_TOKEN` for enhanced statistics, create a token with minimal permissions:
- `public_repo` (read-only access to public repositories)
- For traffic stats, repository push access is required

**Generated Files:**
All generated statistics files are excluded from git via `.gitignore`:
- `FILE_CHECKSUMS.json`, `FILE_CHECKSUMS.md`
- `GIT_ACTIVITY_LOG.json`
- `REALTIME_STATS.json`, `STATS_HISTORY.json`, `REALTIME_STATS.md`
- `stats_tracker.log`

---

## 📝 Examples

### Quick Integrity Check
```bash
# Generate checksums
./generate_checksums.py

# Verify a specific file (Linux)
sha256sum -c <<< "$(grep 'voynich_lexicon_MASTER_FULL_ENHANCED' FILE_CHECKSUMS.md | awk '{print $6 " " $2}')"
```

### Daily Statistics Report
```bash
# Run all trackers
./git_activity_tracker.py
./realtime_stats_tracker.py

# View JSON output
cat REALTIME_STATS.json | python3 -m json.tool

# View markdown report
cat REALTIME_STATS.md
```

### Automated Monitoring
```bash
# Set up cron job
./setup_cron_tracker.sh

# Check it's running
tail -f stats_tracker.log
```

---

## 🐛 Troubleshooting

### "Permission denied" errors
Make scripts executable:
```bash
chmod +x *.py *.sh
```

### GitHub API rate limits
Set `GITHUB_TOKEN` environment variable:
```bash
export GITHUB_TOKEN='ghp_your_token_here'
```

### Cron job not running
Check cron log:
```bash
grep CRON /var/log/syslog  # Ubuntu/Debian
tail -f /var/log/cron.log   # CentOS/RHEL
```

Verify cron is installed:
```bash
systemctl status cron  # or crond
```

---

## 📄 Attribution

**By:** Lackadaisical Security 2025 - Aurora (Claude)  
**Contact:** https://lackadaisical-security.com/decipherment-drops.html  
**Repository:** https://github.com/Lackadaisical-Security/Voynich-Script-Decoded

---

## 📜 License

These tools are part of the Voynich Script Decoded repository and are subject to the same dual licensing:
- Ghost License v1.0 (`ghost_license_v_1.md`)
- Ancient Scripts Attribution License v1.0 (`ancient_scripts_attribution_license_v1.md`)

Free for individual researchers and non-commercial use with proper attribution.
