# NRG Slack Crawler
## Background
At NRG, we rely on slack for all of our official team communications. Despite the size of our workspace, we are on a free slack plan. For a long time, a limitation of this plan was that any message/file history older than 90 days would be hidden behind a paywall. However, we always had the option to upgrade and regain access to our old files, which were safely stored on slack servers.
Unfortunately, on August 26, 2024, Slack began deleting all data over a year old instead of just hiding it. For us, this would mean permanently losing access to seven years of messages, pictures, and files. 
Luckily, we were able to get a free trial of Slack Pro and perform a data export. With this export, we obtained a full backup of message logs and links to any attached files. However, we still had a problem: these files would still be deleted after our trial expired, and we would be left with a bunch of dead links.
To address this, I built a script that takes a Slack data export and downloads a copy of every file that's linked in the server's message logs. This script isn't specific to NRG, and can be used with any slack server's data export.`
## Instructions
1) Perform a slack [data export](https://slack.com/help/articles/201658943-Export-your-workspace-data) (note: you need to be a workspace administrator to do this.)
2) Download [python](https://python.org/downloads)
3) Unzip your data export, then copy the *main.py* file from this repo into the root directory
4) Run *main.py*