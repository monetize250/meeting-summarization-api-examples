"""
Automated outreach script for the Meeting Summarization API.

This script uses the GitHub REST API to search for open‑source projects
related to meeting transcription or summarisation and opens an issue on
each selected repository. The goal is to inform maintainers about the
Meeting Summarization & Action Items API and invite them to try the
service (either via RapidAPI or the public demo).

**Usage instructions**

1. Install dependencies (requests). It is recommended to use a virtual
   environment:
   ```bash
   pip install requests
   ```
2. Set the following environment variables before running the script:
   - `GITHUB_TOKEN`: A personal access token with `repo` scope. You must
     generate this token from your GitHub account settings. The script
     uses it for authentication when creating issues.
   - `OUTREACH_TITLE`: The title of the issue to create on each target
     repository (e.g., "Suggestion: integrate meeting summarization API").
   - `OUTREACH_BODY`: The Markdown‑formatted body of the issue. Use this
     to introduce your API, include links to the RapidAPI listing and
     demo, and provide usage examples. A sample body is provided below.
3. Run the script:
   ```bash
   python github_outreach.py
   ```

By default the script searches for repositories using the query
"meeting transcription summarization" and will open issues on up to
`MAX_REPOS` matching projects. You can adjust the query and limits by
editing the constants in the script.

**Sample outreach body**

```
Hello and thank you for open‑sourcing your meeting transcription tool!  
I built a lightweight Meeting Summarization & Action Items API that
accepts plain‑text transcripts and returns a concise summary plus a
checklist of next steps. It runs fast without external AI models, and
it's available as a freemium service on RapidAPI.

- API listing: https://rapidapi.com/your_username/api/meeting-summarization-api
- Demo: https://monetize250.github.io/instant-meeting-summarizer/

You can integrate it into your project with a simple POST request:

```python
import requests
url = "https://meeting-summarization-api.p.rapidapi.com/summarize"
payload = {"text": "...transcript...", "ratio": 0.2}
headers = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": "<YOUR_KEY>",
    "X-RapidAPI-Host": "meeting-summarization-api.p.rapidapi.com"
}
print(requests.post(url, json=payload, headers=headers).json())
```

I hope this can help your users quickly distill long meetings into
actionable next steps. Feel free to reach out if you have any
questions!
```

**Disclaimer**

Please use this script responsibly. Opening unsolicited issues can be
perceived as spam. It is recommended to personally review the list of
target repositories and adjust the outreach message to ensure it is
appropriate and adds value.
"""

import os
import requests
from typing import List, Dict


# Configuration constants
SEARCH_QUERY = "meeting transcription summarization"
MAX_REPOS = 5  # Maximum number of repositories to process


def github_search_repositories(token: str, query: str, per_page: int = 10) -> List[Dict]:
    """Search GitHub for repositories matching the given query.

    Args:
        token: GitHub personal access token.
        query: Search query string.
        per_page: Number of results per page (max 100).

    Returns:
        A list of repository metadata dictionaries.
    """
    url = "https://api.github.com/search/repositories"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": per_page}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("items", [])


def github_create_issue(token: str, repo_full_name: str, title: str, body: str) -> None:
    """Create an issue in the specified repository.

    Args:
        token: GitHub personal access token.
        repo_full_name: Full name of the repository (e.g., "owner/repo").
        title: Title of the issue.
        body: Body text of the issue (Markdown allowed).
    """
    url = f"https://api.github.com/repos/{repo_full_name}/issues"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    payload = {"title": title, "body": body}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"Issue created in {repo_full_name}")
    else:
        print(f"Failed to create issue in {repo_full_name}: {response.status_code} - {response.text}")


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    title = os.environ.get("OUTREACH_TITLE")
    body = os.environ.get("OUTREACH_BODY")
    if not token or not title or not body:
        raise SystemExit(
            "Environment variables GITHUB_TOKEN, OUTREACH_TITLE and OUTREACH_BODY must be set."
        )

    print(f"Searching for repositories related to: '{SEARCH_QUERY}'...\n")
    repos = github_search_repositories(token, SEARCH_QUERY, per_page=MAX_REPOS)
    for repo in repos:
        full_name = repo["full_name"]
        stars = repo["stargazers_count"]
        description = repo.get("description", "")
        print(f"Preparing to open issue on {full_name} (⭐ {stars}) - {description}")
        github_create_issue(token, full_name, title, body)


if __name__ == "__main__":
    main()