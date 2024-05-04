import json
import os
from discord_webhook import DiscordWebhook
import requests

# Fetch the latest commit from a specific repository and branch
def get_latest_commit(repo, branch='main'):
    url = f"https://api.github.com/repos/{repo}/commits?sha={branch}"
    response = requests.get(url)
    commits = response.json()
    if not commits:
        return None
    return commits[0]['sha']  # Return the SHA of the latest commit

# Save the last known commits to a file
def save_last_commit(data):
    with open('last_commit.json', 'w') as f:
        json.dump(data, f)

# Load the last known commits from a file
def load_last_commits():
    if not os.path.exists('last_commit.json'):
        return {}
    with open('last_commit.json', 'r') as f:
        return json.load(f)

# Send a notification to Discord
def notify_discord(webhook_url, repo, commit):
    message = f"New update in {repo}: {commit}"
    webhook = DiscordWebhook(url=webhook_url, content=message)
    webhook.execute()

def main():
    webhook_url = ''  # Replace with Discord webhook URL
    repos = {
        'rust-lang/rust': 'master',  # Rust main branch
        'umod/oxide': 'master'  # Oxide/uMod master branch (change branch as needed)
    }

    last_commits = load_last_commits()
    updates = {}

    for repo, branch in repos.items():
        latest_commit = get_latest_commit(repo, branch)
        if latest_commit and latest_commit != last_commits.get(repo):
            notify_discord(webhook_url, repo, latest_commit)
            updates[repo] = latest_commit

    if updates:
        save_last_commit(updates)  # Save the new commits to file

if __name__ == '__main__':
    main()