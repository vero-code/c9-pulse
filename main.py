import os
from dotenv import load_dotenv
from grid_client import GridClient

# Load variables from .env file
load_dotenv()

def main():
    api_key = os.getenv("GRID_API_KEY")

    try:
        client = GridClient(api_key)
        print(f"✅ Client initialized for: {client.API_URL}")
    except ValueError as e:
        print(e)
        return

    print("Fetching tournaments...")
    data = client.get_tournaments(limit=3)

    if data:
        tournaments = data.get('tournaments', {})
        print(f"✅ SUCCESS! Total tournaments: {tournaments.get('totalCount')}")

        for edge in tournaments.get('edges', []):
            t = edge['node']
            print(f"- {t['name']} (ID: {t['id']})")

if __name__ == "__main__":
    main()