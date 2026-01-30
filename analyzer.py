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

    def find_potential_victim(self):
        """
        Identify the player with the most deaths in the current game state.
        """
        games = self.data.get('games', [])
        if not games:
            return None
        
        # Consider only the last game (usually the current one)
        game = games[-1]
        all_players = []
        for team in game.get('teams', []):
            for p in team.get('players', []):
                all_players.append(p)
        
        if not all_players:
            return None
            
        victim = max(all_players, key=lambda p: p.get('deaths', 0))
        if victim.get('deaths', 0) > 0:
            return victim
        return None

    def calculate_economy_risk(self, team_name):
        """
        Calculates "Economy Risk": The chance of losing a round due to poor buy.
        Calculated based on recent K/D trends.
        """
        games = self.data.get('games', [])
        if not games:
            return 50  # Default middle risk

        # Use the latest game state
        game = games[-1]
        target_team = None
        opponent_team = None

        for team in game.get('teams', []):
            if team.get('name') == team_name:
                target_team = team
            else:
                opponent_team = team

        if not target_team or not opponent_team:
            return 50

        def get_team_kd(team):
            players = team.get('players', [])
            kills = sum(p.get('kills', 0) for p in players)
            deaths = sum(p.get('deaths', 0) for p in players)
            return kills / max(1, deaths)

        target_kd = get_team_kd(target_team)
        opp_kd = get_team_kd(opponent_team)

        # Base risk is 50%. 
        # If target team has lower K/D than opponent, risk increases.
        # We use a simple sigmoid-like mapping or linear mapping with bounds.
        # Difference in K/D of 1.0 could mean significant risk difference.
        
        kd_diff = opp_kd - target_kd
        # If kd_diff is 1.0 (e.g. Opp KD 1.5, Target KD 0.5), risk should be high.
        risk = 50 + (kd_diff * 25)
        
        # Clamp between 5% and 95%
        return round(max(5, min(95, risk)), 1)
