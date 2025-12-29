import requests
import json

class GridClient:
    # Open Platform Endpoint
    API_URL = "https://api-op.grid.gg/central-data/graphql"

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API Key is missing!")

        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

    def _execute_query(self, query, variables=None):
        """Internal method to execute GraphQL queries."""
        try:
            response = requests.post(
                self.API_URL,
                json={'query': query, 'variables': variables},
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                if 'errors' in data:
                    print("❌ Grid API Error:")
                    print(json.dumps(data['errors'], indent=2))
                    return None
                return data['data']
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return None

    def get_tournaments(self, limit=3):
        """Retrieves a list of tournaments."""
        query = f"""
        query GetTournaments {{
          tournaments(first: {limit}) {{
            totalCount
            edges {{
              node {{
                id
                name
              }}
            }}
          }}
        }}
        """
        return self._execute_query(query)