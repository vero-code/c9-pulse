import pytest
import os
import json
from history_manager import save_match_to_history, get_match_history, get_player_avg_kd, get_first_blood_victim

@pytest.fixture
def temp_history_file(monkeypatch, tmp_path):
    history_file = tmp_path / "test_history.json"
    monkeypatch.setattr("history_manager.HISTORY_FILE", str(history_file))
    return history_file

def test_save_match_to_history(temp_history_file):
    match_id = "test_match_1"
    analysis_data = {"analysis": [{"team": "C9", "players": [{"name": "TenZ", "kills": 20, "deaths": 10}]}]}
    
    # Save first time
    assert save_match_to_history(match_id, analysis_data) is True
    
    with open(temp_history_file, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    assert len(history) == 1
    assert history[0]['match_id'] == match_id
    assert history[0]['data'] == analysis_data

    # Update existing match
    updated_data = {"analysis": [{"team": "C9", "players": [{"name": "TenZ", "kills": 25, "deaths": 5}]}]}
    assert save_match_to_history(match_id, updated_data) is True
    
    with open(temp_history_file, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    assert len(history) == 1
    assert history[0]['data'] == updated_data

def test_get_match_history_empty(temp_history_file):
    assert get_match_history() == []

def test_get_player_avg_kd(temp_history_file):
    match1 = {
        "match_id": "m1",
        "data": {"analysis": [{"players": [{"name": "P1", "kills": 10, "deaths": 5}]}]}
    }
    match2 = {
        "match_id": "m2",
        "data": {"analysis": [{"players": [{"name": "P1", "kills": 20, "deaths": 5}]}]}
    }
    
    save_match_to_history(match1["match_id"], match1["data"])
    save_match_to_history(match2["match_id"], match2["data"])
    
    # m1 KD = 10/5 = 2.0
    # m2 KD = 20/5 = 4.0
    # Avg = 3.0
    assert get_player_avg_kd("P1") == 3.0
    assert get_player_avg_kd("NonExistent") is None

def test_get_first_blood_victim(temp_history_file):
    match1 = {
        "match_id": "m1",
        "data": {"analysis": [
            {"players": [{"name": "P1", "deaths": 10}, {"name": "P2", "deaths": 5}]}
        ]}
    }
    match2 = {
        "match_id": "m2",
        "data": {"analysis": [
            {"players": [{"name": "P1", "deaths": 5}, {"name": "P2", "deaths": 10}]}
        ]}
    }
    match3 = {
        "match_id": "m3",
        "data": {"analysis": [
            {"players": [{"name": "P1", "deaths": 15}, {"name": "P2", "deaths": 5}]}
        ]}
    }
    
    save_match_to_history(match1["match_id"], match1["data"])
    save_match_to_history(match2["match_id"], match2["data"])
    save_match_to_history(match3["match_id"], match3["data"])
    
    # P1 max deaths in m1 and m3
    # P2 max deaths in m2
    victim = get_first_blood_victim()
    assert victim["name"] == "P1"
    assert victim["count"] == 2
