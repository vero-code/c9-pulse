import json
import os
from typing import List, Dict, Any, Optional, Union, Tuple

HISTORY_FILE: str = 'match_history.json'

def save_match_to_history(match_id: Union[int, str], analysis_data: Dict[str, Any]) -> bool:
    """
    Save or update match analysis results in the local history.
    
    Args:
        match_id: Unique identifier for the match.
        analysis_data: The processed analysis results.
        
    Returns:
        True if saved successfully, False otherwise.
    """
    history: List[Dict[str, Any]] = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            history = []

    # Check if match already exists
    match_exists: bool = False
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

def get_match_history() -> List[Dict[str, Any]]:
    """
    Retrieve the complete match history.
    
    Returns:
        A list of match history entries.
    """
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data: List[Dict[str, Any]] = json.load(f)
                return data
        except (json.JSONDecodeError, IOError):
            return []
    return []

def get_player_avg_kd(player_name: str) -> Optional[float]:
    """
    Calculate a player's average K/D ratio from history.
    
    Args:
        player_name: The name of the player.
        
    Returns:
        Average K/D as a float, or None if no history exists.
    """
    history: List[Dict[str, Any]] = get_match_history()
    total_kd: float = 0.0
    match_count: int = 0

    for entry in history:
        analysis: List[Dict[str, Any]] = entry.get('data', {}).get('analysis', [])
        for team in analysis:
            for player in team.get('players', []):
                if player.get('name') == player_name:
                    kills: int = player.get('kills', 0)
                    deaths: int = player.get('deaths', 0)
                    kd: float = kills / max(1, deaths)
                    total_kd += kd
                    match_count += 1
                    break # Found player in this match, move to next match
    
    if match_count == 0:
        return None
    
    return float(round(total_kd / match_count, 2))

def get_first_blood_victim() -> Optional[Dict[str, Union[str, int]]]:
    """
    Identify the player who died most frequently across all matches.
    
    Returns:
        A dictionary with 'name' and 'count', or None.
    """
    history: List[Dict[str, Any]] = get_match_history()
    victim_counts: Dict[str, int] = {}

    for entry in history:
        analysis: List[Dict[str, Any]] = entry.get('data', {}).get('analysis', [])
        all_players: List[Dict[str, Any]] = []
        for team in analysis:
            for player in team.get('players', []):
                all_players.append(player)

        if not all_players:
            continue

        # Find player(s) with maximum deaths in this match
        max_deaths: int = max(p.get('deaths', 0) for p in all_players)
        if max_deaths > 0:
            for p in all_players:
                if p.get('deaths', 0) == max_deaths:
                    name: str = p.get('name')
                    victim_counts[name] = victim_counts.get(name, 0) + 1

    if not victim_counts:
        return None

    # Sort by count descending
    sorted_victims: List[Tuple[str, int]] = sorted(victim_counts.items(), key=lambda x: x[1], reverse=True)
    top_victim, count = sorted_victims[0]
    return {"name": top_victim, "count": count}
