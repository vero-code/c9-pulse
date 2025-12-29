import os
from dotenv import load_dotenv
from grid_client import GridClient
from analyzer import MatchAnalyzer

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
    series_data = client.get_recent_series(limit=3)

    if series_data:
        all_series = series_data.get('allSeries', {})
        print(f"✅ SUCCESS! Found {all_series.get('totalCount')} series available.")
        print("Processing top 3 matches with Live Data Analysis:\n")

        for edge in all_series.get('edges', []):
            match = edge['node']
            match_id = match['id']
            teams = match.get('teams', [])
            if teams and len(teams) >= 2:
                team_a_name = teams[0].get('baseInfo', {}).get('name', 'Unknown')
                team_b_name = teams[1].get('baseInfo', {}).get('name', 'Unknown')
                versus = f"{team_a_name} vs {team_b_name}"
            else:
                versus = "TBD vs TBD"
            print(f"📢 Match: {versus} (ID: {match_id})")

            # --- Live Data Flow (Moneyball Logic) ---
            state_data = client.get_series_state(match_id)
            if not state_data or not state_data.get('games'):
                print("   ⚠️ No live game data available yet. Waiting for start...")
                print("-" * 40)
                continue

            analyzer = MatchAnalyzer(state_data)
            try:
                first_game = state_data['games'][0]

                if len(first_game['teams']) > 0:
                    team_live = first_game['teams'][0]
                    team_name = team_live['name']

                    if len(team_live['players']) > 0:
                        player_name = team_live['players'][0]['name']
                        print(f"   👤 Analyzing Player: {player_name}")
                        print(f"   > {analyzer.analyze_player_performance(player_name)}")
                    print(f"   🛡️ Analyzing Team Economy: {team_name}")
                    print(f"   > {analyzer.analyze_team_economy(team_name)}")
            except (IndexError, KeyError) as e:
                print(f"   > Analysis skipped: Data structure mismatch ({e})")
            print("-" * 40)

if __name__ == "__main__":
    main()