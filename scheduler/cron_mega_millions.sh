#!/bin/bash
dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
python=/Users/ifeoluwalawal/.virtualenvs/scrape-to-db/bin/python
notifier=/usr/local/bin/terminal-notifier

cd $dir
export FUNC_TO_RUN="mega_millions"
$python ../main.py run latest
$notifier -title "Ran mega millions scrape" -subtitle "Scraped bruh" -message "Completed"
now=$(date)
echo "Cron job completed at $now"