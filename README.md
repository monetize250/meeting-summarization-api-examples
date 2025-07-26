# Meeting Summarization API Example Clients

This repository contains example clients and instructions for using the Meeting Summarization & Action Items API available on RapidAPI. The API accepts raw meeting transcripts and returns a concise summary plus a list of action items extracted from the text.

## How to Use

1. Visit the Meeting Summarization API listing on RapidAPI and subscribe to the plan that meets your needs. RapidAPI will provide you with a `X-RapidAPI-Key` and `X-RapidAPI-Host` for authentication.
2. Send a POST request to the `/summarize` endpoint with your transcript text. You can optionally specify:
    - `ratio` *(float)* — the proportion of sentences to include in the summary (e.g., `0.2` will return the top 20% of sentences). Default is `0.2`.
    - `max_sentences` *(int)* — maximum number of sentences in the summary. If both `ratio` and `max_sentences` are provided, the API will honor the lower limit.

The request body should be a JSON object with at least the `text` field.

### Example Request Body
```json
{
  "text": "Yesterday we discussed the Q3 marketing strategy. The team agreed to focus on improving retention, launching the new referral program by September 1st, and scheduling bi-weekly check-in meetings. John will draft the referral program details and Sarah will create the timeline. The next meeting is set for August 10th.",
  "ratio": 0.3,
  "max_sentences": 3
}
```

### Example Response
```json
{
  "summary": "The team discussed the Q3 marketing strategy and agreed to focus on improving retention, launching a referral program by September 1st and scheduling bi-weekly check-in meetings.",
  "action_items": [
    "John will draft the referral program details.",
    "Sarah will create the timeline.",
    "The next meeting is set for August 10th."
  ]
}
```

## Python Example using `requests`

```python
import requests

# RapidAPI credentials
url = "https://<YOUR_RAPIDAPI_HOST>/summarize"
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "<YOUR_RAPIDAPI_KEY>",
    "X-RapidAPI-Host": "<YOUR_RAPIDAPI_HOST>"
}
payload = {
    "text": "Your meeting transcript goes here...",
    "ratio": 0.2,
    "max_sentences": 5
}

response = requests.post(url, json=payload, headers=headers)
if response.ok:
    data = response.json()
    print("Summary:", data["summary"])
    print("Action Items:", data["action_items"])
else:
    print("Request failed:", response.status_code, response.text)
```

Replace `<YOUR_RAPIDAPI_KEY>` and `<YOUR_RAPIDAPI_HOST>` with the values provided by RapidAPI when you subscribe.

## Node.js Example using `axios`

```javascript
const axios = require('axios');

// RapidAPI credentials
const url = 'https://<YOUR_RAPIDAPI_HOST>/summarize';
const options = {
  headers: {
    'Content-Type': 'application/json',
    'X-RapidAPI-Key': '<YOUR_RAPIDAPI_KEY>',
    'X-RapidAPI-Host': '<YOUR_RAPIDAPI_HOST>'
  }
};

const payload = {
  text: 'Your meeting transcript goes here...',
  ratio: 0.2,
  max_sentences: 5
};

axios.post(url, payload, options)
  .then(res => {
    const data = res.data;
    console.log('Summary:', data.summary);
    console.log('Action Items:', data.action_items);
  })
  .catch(err => {
    console.error('Error:', err.response ? err.response.data : err.message);
  });
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
