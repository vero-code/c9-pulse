# main.py
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
            
            # --- Integration of MatchAnalyzer ---
            print("   Running Analysis...")
            details = client.get_match_details(match_id)
            if details:
                analyzer = MatchAnalyzer(details)
                
                # Analyze first player of first team as an example
                if teams:
                    first_team_name = teams[0].get('baseInfo', {}).get('name')
                    # We need to find a player name from the details
                    try:
                        first_game = details.get('series', {}).get('games', [])[0]
                        first_player = first_game['teams'][0]['players'][0]['player']['baseInfo']['name']
                        
                        print(f"   > {analyzer.analyze_opening_deaths(first_player)}")
                        print(f"   > {analyzer.analyze_economy_impact(first_team_name)}")
                    except (IndexError, KeyError):
                        print("   > No player/game data available for detailed analysis.")

            print("-" * 40)

    print("\n--- 3. Fetching Team Statistics & Moneyball Insight ---")
    team_id = "83" # Example team ID
    team_stats = client.get_team_stats(team_id)
    if team_stats:
        # Initialize MatchAnalyzer with the returned statistics data
        analyzer = MatchAnalyzer(team_stats)
        insight = analyzer.analyze_team_moneyball(team_stats)
        print(f"📊 Team Statistics Insight (ID: {team_id}):")
        print(f"   {insight}")
    else:
        print(f"❌ Could not fetch statistics for team ID: {team_id}")


if __name__ == "__main__":
    main()