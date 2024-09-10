import requests
import argparse
import sys

# GitHub API endpoint to fetch user events
GITHUB_API_URL = "https://api.github.com/users/{}/events"

def fetch_github_activity(username):
    """Fetch recent GitHub activity of the specified user."""
    url = GITHUB_API_URL.format(username)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")
        sys.exit(1)

def display_activity(events):
    """Display the user's recent activity in a readable format."""
    for event in events[:5]:  # Display the 5 most recent events
        event_type = event.get("type")
        repo_name = event.get("repo", {}).get("name")
        
        if event_type == "PushEvent":
            commit_count = len(event.get("payload", {}).get("commits", []))
            print(f"Pushed {commit_count} commits to {repo_name}")
        elif event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action")
            print(f"{action.capitalize()} an issue in {repo_name}")
        elif event_type == "WatchEvent":
            print(f"Starred {repo_name}")
        elif event_type == "ForkEvent":
            print(f"Forked {repo_name}")
        else:
            print(f"{event_type} in {repo_name}")

def main():
    """Main function to handle argument parsing and activity fetching."""
    parser = argparse.ArgumentParser(description="Fetch recent GitHub activity of a user")
    parser.add_argument("username", help="GitHub username to fetch activity for")
    
    args = parser.parse_args()
    username = args.username
    
    # Fetch and display the user's activity
    events = fetch_github_activity(username)
    if events:
        display_activity(events)
    else:
        print(f"No recent activity found for user {username}.")

if __name__ == "__main__":
    main()
