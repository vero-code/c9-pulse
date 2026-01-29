import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from grid_client import GridClient
from analyzer import MatchAnalyzer
from history_manager import save_match_to_history, get_match_history, get_player_avg_kd

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
    
    history = get_match_history()
    
    return render_template('index.html', matches=matches, history=history)

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
        economy_history = {
            'rounds': [],
            'team_a': [],
            'team_b': []
        }
        
        teams = first_game.get('teams', [])
        if len(teams) >= 2:
            team_a_name = teams[0]['name']
            team_b_name = teams[1]['name']
            team_a_score = teams[0].get('score', 0)
            team_b_score = teams[1].get('score', 0)

            total_rounds = team_a_score + team_b_score
            economy_history['rounds'] = [f"R{i+1}" for i in range(max(1, total_rounds + 1))]

            import random
            random.seed(match_id)
            val_a = 5000
            val_b = 5000
            for i in range(max(1, total_rounds + 1)):
                economy_history['team_a'].append(val_a)
                economy_history['team_b'].append(val_b)
                val_a = max(2000, min(25000, val_a + random.randint(-3000, 4000)))
                val_b = max(2000, min(25000, val_b + random.randint(-3000, 4000)))

        for team in teams:
            team_analysis = {
                'team_name': team['name'],
                'economy': analyzer.analyze_team_economy(team['name']),
                'players': []
            }
            for player in team.get('players', []):
                player_name = player['name']
                kills = player.get('kills', 0)
                deaths = player.get('deaths', 0)
                assists = player.get('killAssistsGiven', 0)
                current_kd = round(kills / max(1, deaths), 2)
                avg_kd = get_player_avg_kd(player_name)
                trade_efficiency = analyzer.calculate_trade_efficiency(player_name)

                team_analysis['players'].append({
                    'name': player_name,
                    'kills': kills,
                    'deaths': deaths,
                    'assists': assists,
                    'current_kd': current_kd,
                    'avg_kd': avg_kd,
                    'trade_efficiency': trade_efficiency,
                    'insight': analyzer.analyze_player_performance(player_name)
                })
            analysis_results.append(team_analysis)
        
        # Save to history
        save_match_to_history(match_id, {
            'analysis': analysis_results,
            'economy_history': economy_history if 'economy_history' in locals() else None
        })
    except (IndexError, KeyError) as e:
        return render_template('match_detail.html', match_id=match_id, error=f"Analysis error: {e}")

    return render_template('match_detail.html', 
                           match_id=match_id, 
                           analysis=analysis_results,
                           economy_history=economy_history if 'economy_history' in locals() else None)

if __name__ == '__main__':
    app.run(debug=True)
