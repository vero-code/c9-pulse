import pytest
from analyzer import MatchAnalyzer

@pytest.fixture
def sample_match_data():
    return {
        "games": [
            {
                "teams": [
                    {
                        "name": "Cloud9",
                        "score": 13,
                        "players": [
                            {"name": "TenZ", "kills": 20, "deaths": 10, "killAssistsGiven": 5},
                            {"name": "Mitch", "kills": 10, "deaths": 15, "killAssistsGiven": 2}
                        ]
                    },
                    {
                        "name": "Sentinels",
                        "score": 11,
                        "players": [
                            {"name": "ShahZaM", "kills": 15, "deaths": 15, "killAssistsGiven": 3},
                            {"name": "Sick", "kills": 12, "deaths": 12, "killAssistsGiven": 4}
                        ]
                    }
                ]
            }
        ]
    }

def test_analyze_player_performance(sample_match_data, mocker):
    # Mock get_random_insight to return predictable strings
    mocker.patch("analyzer.get_random_insight", side_effect=lambda key, **kwargs: f"{key}_{kwargs.get('player', '')}")
    
    analyzer = MatchAnalyzer(sample_match_data)
    
    # TenZ: 20/10 = 2.0 KD
    assert analyzer.analyze_player_performance("TenZ") == "good_kd_TenZ"
    
    # Mitch: 10/15 = 0.66 KD, deaths > 10
    assert analyzer.analyze_player_performance("Mitch") == "high_deaths_Mitch"
    
    assert analyzer.analyze_player_performance("Unknown") == "Player data not found in this match."

def test_analyze_team_economy(sample_match_data, mocker):
    mocker.patch("analyzer.get_random_insight", side_effect=lambda key, **kwargs: key)
    
    analyzer = MatchAnalyzer(sample_match_data)
    
    # Cloud9: 30/25 = 1.2 KD
    assert analyzer.analyze_team_economy("Cloud9") == "team_winning"
    
    # Create a losing team data
    losing_data = {
        "games": [{"teams": [{"name": "LosingTeam", "players": [{"kills": 5, "deaths": 10}]}]}]
    }
    analyzer_losing = MatchAnalyzer(losing_data)
    assert analyzer_losing.analyze_team_economy("LosingTeam") == "team_losing"

def test_calculate_trade_efficiency(sample_match_data):
    analyzer = MatchAnalyzer(sample_match_data)
    # TenZ: (20 + 5) / 10 = 2.5
    assert analyzer.calculate_trade_efficiency("TenZ") == 2.5
    # Mitch: (10 + 2) / 15 = 0.8
    assert analyzer.calculate_trade_efficiency("Mitch") == 0.8

def test_find_potential_victim(sample_match_data):
    analyzer = MatchAnalyzer(sample_match_data)
    victim = analyzer.find_potential_victim()
    # Mitch has 15 deaths, same as ShahZaM, max picks first or based on list order
    assert victim["name"] in ["Mitch", "ShahZaM"]
    assert victim["deaths"] == 15

def test_calculate_economy_risk(sample_match_data):
    analyzer = MatchAnalyzer(sample_match_data)
    # C9 KD is 1.2, Sentinels KD is 1.0
    # C9 has higher KD, so risk should be lower than 50
    risk = analyzer.calculate_economy_risk("Cloud9")
    assert 0 <= risk <= 100
    
    risk_opp = analyzer.calculate_economy_risk("Sentinels")
    assert risk < risk_opp

def test_find_mvp(sample_match_data):
    analyzer = MatchAnalyzer(sample_match_data)
    mvp = analyzer.find_mvp()
    assert mvp == "TenZ"

def test_multiple_games(mocker):
    mocker.patch("analyzer.get_random_insight", side_effect=lambda key, **kwargs: f"{key}")
    data = {
        "games": [
            {
                "teams": [
                    {
                        "name": "Team1",
                        "players": [{"name": "OldPlayer", "kills": 10, "deaths": 2}]
                    }
                ]
            },
            {
                "teams": [
                    {
                        "name": "Team1",
                        "players": [{"name": "NewPlayer", "kills": 5, "deaths": 1}]
                    }
                ]
            }
        ]
    }
    analyzer = MatchAnalyzer(data)
    # NewPlayer is in the latest game
    assert analyzer.analyze_player_performance("NewPlayer") == "good_kd"
    # OldPlayer is NOT in the latest game, but should be found by fallback
    assert analyzer.analyze_player_performance("OldPlayer") == "good_kd"
    # Team1 should be found in latest game primarily
    assert analyzer.analyze_team_economy("Team1") == "team_winning"
