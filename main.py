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

    print("\n--- 1. Checking Tournaments ---")
    tournaments_data = client.get_tournaments(limit=1)
    if tournaments_data:
        print("✅ Tournaments endpoint is working.")

    print("\n--- 2. Fetching Recent Series (Matches) ---")
    series_data = client.get_recent_series(limit=5)

    if series_data:
        all_series = series_data.get('allSeries', {})
        print(f"✅ SUCCESS! Found {all_series.get('totalCount')} series available.")
        print("Here are the first 5 loaded matches:\n")

        for edge in all_series.get('edges', []):
            match = edge['node']
            match_id = match['id']
            start_time = match['startTimeScheduled']

            tourn_name = match.get('tournament', {}).get('nameShortened', 'Unknown Tournament')

            teams = match.get('teams', [])
            if teams and len(teams) >= 2:
                team_a = teams[0].get('baseInfo', {}).get('name', 'Unknown')
                team_b = teams[1].get('baseInfo', {}).get('name', 'Unknown')
                versus = f"{team_a} vs {team_b}"
            else:
                versus = "TBD vs TBD"

            print(f"[{start_time}] {versus}")
            print(f"   Tournament: {tourn_name} | ID: {match_id}")
            print("-" * 40)


if __name__ == "__main__":
    main()