import json
import os

HISTORY_FILE = 'match_history.json'

def save_match_to_history(match_id, analysis_data):
    """
    Saves match analysis results to a JSON file.
    If the match already exists, it updates the record.
    """
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            history = []

    # Check if match already exists
    match_exists = False
    for i, entry in enumerate(history):
        if entry.get('match_id') == match_id:
            history[i] = {
                'match_id': match_id,
                'data': analysis_data
            }
            match_exists = True
            break
    
    if not match_exists:
        history.append({
            'match_id': match_id,
            'data': analysis_data
        })

    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving history: {e}")
        return False

def get_match_history():
    """
    Retrieves the full match history from the JSON file.
    """
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def get_player_avg_kd(player_name):
    """
    Calculates the average K/D ratio for a player based on history.
    """
    history = get_match_history()
    total_kd = 0
    match_count = 0

    for entry in history:
        analysis = entry.get('data', {}).get('analysis', [])
        for team in analysis:
            for player in team.get('players', []):
                if player.get('name') == player_name:
                    kills = player.get('kills', 0)
                    deaths = player.get('deaths', 0)
                    kd = kills / max(1, deaths)
                    total_kd += kd
                    match_count += 1
                    break # Found player in this match, move to next match
    
    if match_count == 0:
        return None
    
    return round(total_kd / match_count, 2)
