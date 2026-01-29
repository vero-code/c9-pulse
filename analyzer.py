# analyzer.py
class MatchAnalyzer:
    def __init__(self, data):
        """
        Initialize with raw JSON data from seriesState query.
        """
        self.data = data

    def analyze_player_performance(self, player_name):
        """
        Analyze player performance based on kills and deaths.
        """
        games = self.data.get('games', [])
        
        for game in games:
            teams = game.get('teams', [])
            for team in teams:
                players = team.get('players', [])
                for p in players:
                    if p.get('name') == player_name:
                        kills = p.get('kills', 0)
                        deaths = p.get('deaths', 0)
                        ratio = round(kills / max(1, deaths), 2)
                        
                        if deaths > 10 and ratio < 0.8:
                            return f"⚠️ Insight: High death count ({deaths}). Recommendation: Play safer."
                        if ratio > 1.5:
                            return f"🔥 Insight: Excellent performance (K/D {ratio}). Keep playing aggressive."
                        
                        return "✅ Insight: Stable performance."
        
        return "Player data not found in this match."

    def analyze_team_economy(self, team_name):
        """
        Analyze team economy based on total Team K/D.
        """
        games = self.data.get('games', [])
        
        for game in games:
            teams = game.get('teams', [])
            for team in teams:
                if team.get('name') == team_name:
                    players = team.get('players', [])
                    total_kills = sum(p.get('kills', 0) for p in players)
                    total_deaths = sum(p.get('deaths', 0) for p in players)
                    ratio = round(total_kills / max(1, total_deaths), 2)
                    
                    if ratio < 0.9:
                        return f"📉 Macro Review: Team is losing duels (K/D {ratio}). Likely economy disadvantage."
                    else:
                        return "📈 Macro Review: Team winning exchanges. Economy looks strong."

        return f"Team {team_name} not found."

    def calculate_trade_efficiency(self, player_name):
        """
        Calculates Trade Efficiency: (Kills + Assists) / Deaths
        """
        games = self.data.get('games', [])
        for game in games:
            for team in game.get('teams', []):
                for p in team.get('players', []):
                    if p.get('name') == player_name:
                        kills = p.get('kills', 0)
                        deaths = p.get('deaths', 0)
                        assists = p.get('killAssistsGiven', 0)
                        efficiency = round((kills + assists) / max(1, deaths), 2)
                        return efficiency
        return 0.0
