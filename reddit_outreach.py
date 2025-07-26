"""
Automated Reddit outreach script for the Meeting Summarization API.

This script uses the `praw` library to authenticate with Reddit and
search for recent posts related to meeting transcription, Zoom, and
text summarization. It will leave a comment on each qualifying post
with a helpful introduction to the Meeting Summarization & Action
Items API and links to both the RapidAPI listing and the public demo.

**Important**: Commenting on posts is a public action. Please use
this script responsibly and respect each subreddit’s rules. Do not
spam—ensure your comment is relevant to the post and adds value.

**Dependencies**

You will need to install the `praw` library before running this
script:

```bash
pip install praw
```

**Environment Variables**

Set the following environment variables for authentication and
configuration:

- `REDDIT_CLIENT_ID`: Your Reddit app’s client ID.
- `REDDIT_CLIENT_SECRET`: Your Reddit app’s client secret.
- `REDDIT_USERNAME`: Your Reddit account username.
- `REDDIT_PASSWORD`: Your Reddit account password.
- `USER_AGENT`: A descriptive user agent string (e.g., "MeetingSummarizerBot/0.1 by u/YourUsername").
- `SUBREDDITS`: A comma‑separated list of subreddit names to monitor
  (e.g., "webdev,saas,productivity").
- `SEARCH_KEYWORDS`: A comma‑separated list of keywords to search for
  within each subreddit (e.g., "meeting transcription,meeting summary,zoom transcript").
- `COMMENT_BODY`: The Markdown‑formatted comment to post. Include
  links to your RapidAPI listing and demo. See the sample below.

You can set these variables in your shell or in a `.env` file and
load them using `python-dotenv` if desired.

**Sample Comment Body**

```
Hi there! I saw you’re working with meeting transcripts. I recently
created a free Meeting Summarization & Action Items API that turns
meeting text into a concise summary and a checklist of next steps.
It’s lightweight, doesn’t rely on large AI models, and offers a
generous free tier.

- Try it on RapidAPI: https://rapidapi.com/your_username/api/meeting-summarization-api
- Or see the demo: https://monetize250.github.io/instant-meeting-summarizer/

Here’s a quick Python example using the API:

```python
import requests
url = "https://meeting-summarization-api.p.rapidapi.com/summarize"
payload = {"text": "...transcript...", "ratio": 0.3}
headers = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": "<YOUR_RAPIDAPI_KEY>",
    "X-RapidAPI-Host": "meeting-summarization-api.p.rapidapi.com"
}
print(requests.post(url, json=payload, headers=headers).json())
```

Hope this helps your project! Let me know if you have any
questions.
```

**Usage**

After setting the environment variables, run the script:

```bash
python reddit_outreach.py
```

The script will:
1. Authenticate with Reddit using your credentials.
2. Iterate over each subreddit in `SUBREDDITS`.
3. Search for recent posts containing any of the keywords in
   `SEARCH_KEYWORDS`.
4. Post your comment in response to each match.

**Disclaimer**

Be mindful of Reddit’s API usage limits and subreddit rules.
Excessive automated comments can lead to your account being banned.
Always tailor your comments to the specific context and avoid
generic spammy messages.
"""

import os
import praw


def main() -> None:
    # Read required environment variables
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    username = os.environ.get("REDDIT_USERNAME")
    password = os.environ.get("REDDIT_PASSWORD")
    user_agent = os.environ.get("USER_AGENT")
    subreddits = os.environ.get("SUBREDDITS")
    keywords = os.environ.get("SEARCH_KEYWORDS")
    comment_body = os.environ.get("COMMENT_BODY")

    # Validate environment variables
    if not all([client_id, client_secret, username, password, user_agent, subreddits, keywords, comment_body]):
        raise SystemExit(
            "Missing one or more required environment variables. "
            "Please set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, "
            "REDDIT_PASSWORD, USER_AGENT, SUBREDDITS, SEARCH_KEYWORDS, and COMMENT_BODY."
        )

    # Initialise Reddit API client
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent,
    )

    subreddit_list = [s.strip() for s in subreddits.split(",") if s.strip()]
    keyword_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]

    print(f"Monitoring subreddits: {', '.join(subreddit_list)}")
    for sub_name in subreddit_list:
        subreddit = reddit.subreddit(sub_name)
        print(f"\nSearching for posts in r/{sub_name}...")
        for post in subreddit.new(limit=50):  # Check the 50 newest posts
            title = post.title.lower()
            # Check if any keyword appears in the title
            if any(keyword in title for keyword in keyword_list):
                print(f"Found matching post: '{post.title}' (id={post.id})")
                # Post the comment
                try:
                    post.reply(comment_body)
                    print(f"Commented on post: {post.permalink}")
                except Exception as e:
                    print(f"Failed to comment on post '{post.id}': {e}")


if __name__ == "__main__":
    main()