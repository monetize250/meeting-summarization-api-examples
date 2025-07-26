// Example usage of the Meeting Summarization API from Node.js using axios.
//
// Before running this script, install axios:
//   npm install axios
//
// Replace 'YOUR_RAPIDAPI_KEY' with your actual RapidAPI key.

const axios = require('axios');

async function main() {
  const options = {
    method: 'POST',
    url: 'https://meeting-summarization-api.p.rapidapi.com/summarize',
    headers: {
      'content-type': 'application/json',
      'X-RapidAPI-Key': 'YOUR_RAPIDAPI_KEY',
      'X-RapidAPI-Host': 'meeting-summarization-api.p.rapidapi.com',
    },
    data: {
      text:
        "In today's meeting we reviewed quarterly sales numbers, discussed the upcoming product launch and assigned follow‑up tasks to the marketing and engineering teams.",
      ratio: 0.2,
    },
  };

  try {
    const response = await axios.request(options);
    console.log('Summary:', response.data.summary);
    console.log('Action Items:');
    response.data.action_items.forEach((item, idx) => {
      console.log(`${idx + 1}. ${item}`);
    });
  } catch (error) {
    if (error.response) {
      console.error('API responded with status', error.response.status);
      console.error(error.response.data);
    } else {
      console.error('Request error', error.message);
    }
  }
}

main();