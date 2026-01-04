#!/bin/bash
# Setup cron job for local stats tracking
# By: Lackadaisical Security 2025

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_SCHEDULE="0 */6 * * *"  # Every 6 hours

echo "Setting up cron job for repository stats tracking..."

# Detect Python path
PYTHON_PATH=$(which python3 2>/dev/null || echo "/usr/bin/python3")

# Create cron job
(crontab -l 2>/dev/null; echo "${CRON_SCHEDULE} cd ${REPO_DIR} && ${PYTHON_PATH} realtime_stats_tracker.py &> ${REPO_DIR}/stats_tracker.log 2>&1") | crontab -

echo "✅ Cron job created!"
echo "   Schedule: Every 6 hours"
echo "   Location: ${REPO_DIR}"
echo "   Log file: ${REPO_DIR}/stats_tracker.log"
echo ""
echo "To view cron jobs: crontab -l"
echo "To remove: crontab -e (then delete the line)"
