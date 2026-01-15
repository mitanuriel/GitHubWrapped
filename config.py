"""
Configuration file for GitHub Team Wrapped
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get GitHub token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found. Please create a .env file with your token.")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}

# List your team members logins here
TEAM_MEMBERS = ["mitanuriel", "TheoKoppenhoefer","lucalewin","V4ldeSalnikov", "GodDaddyC", "ErikRydengard", "Lipjup7", "Narwish" ]  

ORG_NAME = "Kravi-Analytics-AB"  

# Collecting data from January 1, 2025 to present (January 15, 2026) - over 1 year of history
SINCE_DATE = "2025-01-01T00:00:00Z"
