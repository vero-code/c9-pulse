import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from grid_client import GridClient
from analyzer import MatchAnalyzer

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize GridClient
api_key = os.getenv("GRID_API_KEY")
client = None
if api_key:
    client = GridClient(api_key)

@app.route('/')
def index():
    if not client:
        return "Error: GRID_API_KEY not found in environment.", 500
    
    series_data = client.get_recent_series(limit=10)
    matches = []
    if series_data:
        all_series = series_data.get('allSeries', {})
        for edge in all_series.get('edges', []):
            node = edge['node']
            match_id = node['id']
            teams = node.get('teams', [])
            if teams and len(teams) >= 2:
                team_a = teams[0].get('baseInfo', {}).get('name', 'Unknown')
                team_b = teams[1].get('baseInfo', {}).get('name', 'Unknown')
                versus = f"{team_a} vs {team_b}"
            else:
                versus = "TBD vs TBD"
            
            matches.append({
                'id': match_id,
                'versus': versus,
                'tournament': node.get('tournament', {}).get('nameShortened', 'N/A'),
                'time': node.get('startTimeScheduled', 'N/A')
            })
    
    return render_template('index.html', matches=matches)

@app.route('/match/<match_id>')
def match_detail(match_id):
    if not client:
        return "Error: GRID_API_KEY not found in environment.", 500
    
    state_data = client.get_series_state(match_id)
    if not state_data or not state_data.get('games'):
        return render_template('match_detail.html', match_id=match_id, error="No live data available for this match.")
    
    analyzer = MatchAnalyzer(state_data)
    analysis_results = []
    
    # Simple analysis for the first game
    try:
        first_game = state_data['games'][0]
        for team in first_game.get('teams', []):
            team_analysis = {
                'team_name': team['name'],
                'economy': analyzer.analyze_team_economy(team['name']),
                'players': []
            }
            for player in team.get('players', []):
                player_name = player['name']
                team_analysis['players'].append({
                    'name': player_name,
                    'stats': f"K: {player.get('kills', 0)} | D: {player.get('deaths', 0)}",
                    'insight': analyzer.analyze_player_performance(player_name)
                })
            analysis_results.append(team_analysis)
    except (IndexError, KeyError) as e:
        return render_template('match_detail.html', match_id=match_id, error=f"Analysis error: {e}")

    return render_template('match_detail.html', match_id=match_id, analysis=analysis_results)

if __name__ == '__main__':
    app.run(debug=True)
