import os
import requests
import json
from dotenv import load_dotenv

def test_series_state():
    # 1. Load the API Key from .env
    load_dotenv()
    api_key = os.getenv("GRID_API_KEY")

    if not api_key:
        print("❌ Error: GRID_API_KEY not found in .env file.")
        return

    # 2. Define the URL
    url = "https://api-op.grid.gg/live-data-feed/series-state/graphql"

    # 3. Define the GraphQL query
    query = """
    query GetState {
      seriesState(id: "2618418") {
        id
        valid
        games {
          id
          sequenceNumber
          teams {
            name
            players {
              name
              kills
              deaths
            }
          }
        }
      }
    }
    """

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    print(f"Connecting to: {url}...")
    
    try:
        # 4. Execute the request
        response = requests.post(
            url,
            json={'query': query},
            headers=headers
        )

        # 5. Handle response
        if response.status_code == 200:
            data = response.json()
            print("✅ Response received:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Error text: {response.text}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    test_series_state()
