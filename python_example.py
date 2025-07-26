import requests
import json


def main():
    """Simple example demonstrating how to call the Meeting Summarization API using Python.

    Replace `YOUR_RAPIDAPI_KEY` with your actual RapidAPI subscription key.
    Adjust the `payload` fields as needed to summarise your own meeting transcript.
    """

    url = "https://meeting-summarization-api.p.rapidapi.com/summarize"

    # Provide the meeting transcript and optional parameters. The `ratio` defines
    # what fraction of the original text to keep in the summary. You can also
    # specify `max_sentences` instead of `ratio` to limit the number of summary
    # sentences.
    payload = {
        "text": (
            "In today's meeting we reviewed quarterly sales numbers, discussed the"
            " upcoming product launch and assigned follow‑up tasks to the marketing"
            " and engineering teams."
        ),
        "ratio": 0.2
    }

    # RapidAPI authentication headers. Replace with your own key from the RapidAPI
    # dashboard. The host name must remain exactly as shown.
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
        "X-RapidAPI-Host": "meeting-summarization-api.p.rapidapi.com",
    }

    # Make the POST request to the API
    response = requests.post(url, json=payload, headers=headers)

    # If the call was successful, parse and print the summary and action items
    if response.status_code == 200:
        data = response.json()
        print("Summary:")
        print(data.get("summary", "No summary returned."))
        print("\nAction Items:")
        for idx, item in enumerate(data.get("action_items", []), start=1):
            print(f"{idx}. {item}")
    else:
        print(f"Request failed with status {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    main()