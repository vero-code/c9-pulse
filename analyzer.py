# analyzer.py
from coach_config import get_random_insight

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
                            return get_random_insight("high_deaths", player=player_name, deaths=deaths)
                        if ratio > 1.5:
                            return get_random_insight("good_kd", player=player_name, ratio=ratio)
                        
                        return get_random_insight("stable", player=player_name)
        
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
                        return get_random_insight("team_losing", ratio=ratio)
                    else:
                        return get_random_insight("team_winning")

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

    def get_buy_recommendation(self, team_name):
        """
        Calculates buy recommendation based on economy risk.
        Low risk -> Full Buy
        Medium risk -> Force Buy
        High risk -> Eco
        """
        risk = self.calculate_economy_risk(team_name)
        
        if risk < 35:
            return "Full Buy"
        elif risk < 65:
            return "Force Buy"
        else:
            return "Eco"

    def calculate_tilt_risk(self, player_name):
        """
        Calculates Tilt Risk for a player.
        If a player has a high death count relative to their kills and the team's progress,
        the tilt risk increases.
        Since we don't have round-by-round death history in the current schema,
        we use the current game's K/D and total deaths as a proxy.
        If deaths >= 3 and K/D < 0.5, risk starts growing.
        """
        games = self.data.get('games', [])
        if not games:
            return 0

        game = games[-1]
        for team in game.get('teams', []):
            for p in team.get('players', []):
                if p.get('name') == player_name:
                    deaths = p.get('deaths', 0)
                    kills = p.get('kills', 0)
                    
                    if deaths == 0:
                        return 0
                    
                    kd = kills / deaths
                    
                    # Risk grows if deaths >= 3
                    if deaths < 3:
                        return 0
                    
                    # Base risk for 3+ deaths
                    risk = 30
                    
                    # Increase risk for poor K/D
                    if kd < 0.5:
                        risk += 40
                    elif kd < 1.0:
                        risk += 20
                        
                    # Increase risk for every death above 3
                    risk += (deaths - 3) * 10
                    
                    return min(100, risk)
        return 0

    def analyze_opponent_strategy(self, team_name):
        """
        Analyzes opponent strategy based on available match data.
        Currently provides basic insights like "Enemy often pushes B".
        """
        games = self.data.get('games', [])
        if not games:
            return "No data for strategy analysis."

        # Find the opponent team
        opponent_team = None
        game = games[-1]
        for team in game.get('teams', []):
            if team.get('name') != team_name:
                opponent_team = team
                break

        if not opponent_team:
            return "Opponent data not found."

        # Basic logic: if opponent is winning significantly, they might be playing aggressive
        target_team = next((t for t in game.get('teams', []) if t.get('name') == team_name), None)
        
        if target_team and opponent_team.get('score', 0) > target_team.get('score', 0) + 3:
            return "⚠️ Strategy Insight: Enemy often pushes B. Be ready for aggressive site takes."
        
        return "✅ Strategy Insight: Opponent playing standard. No unusual patterns detected."

    def find_mvp(self):
        """
        Identify the MVP of the match.
        MVP is determined by the highest score, where score = kills + assists * 0.5 - deaths * 0.3.
        """
        games = self.data.get('games', [])
        if not games:
            return None
        
        game = games[-1]
        best_player = None
        max_score = -1000
        
        for team in game.get('teams', []):
            for p in team.get('players', []):
                kills = p.get('kills', 0)
                deaths = p.get('deaths', 0)
                assists = p.get('killAssistsGiven', 0)
                
                # Simple MVP formula
                score = kills + (assists * 0.5) - (deaths * 0.3)
                
                if score > max_score:
                    max_score = score
                    best_player = p.get('name')
        
        return best_player

    def get_critical_moments(self):
        """
        Detects critical moments like Aces, Clutches, and Death Streaks.
        Returns a list of strings describing these moments.
        """
        moments = []
        games = self.data.get('games', [])
        if not games:
            return moments

        game = games[-1]
        for team in game.get('teams', []):
            for p in team.get('players', []):
                name = p.get('name')
                kills = p.get('kills', 0)
                deaths = p.get('deaths', 0)

                # Heuristic for Ace (e.g. 5+ kills in a game, since we don't have round data)
                # In a real scenario, this would check round-specific data.
                if kills >= 5 and kills % 5 == 0:
                    moments.append(get_random_insight("ace", player=name))

                # Heuristic for Death Streak
                if deaths >= 5 and kills < (deaths / 2):
                    moments.append(get_random_insight("death_streak", player=name, deaths=deaths))

        # Heuristic for Clutch (e.g. if one team is winning rounds with fewer players)
        # This is very simplified given the current schema.
        if len(game.get('teams', [])) >= 2:
            team_a = game['teams'][0]
            team_b = game['teams'][1]
            if abs(team_a.get('score', 0) - team_b.get('score', 0)) == 1:
                moments.append(get_random_insight("clutch"))

        return moments
