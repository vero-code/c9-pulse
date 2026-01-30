# coach_config.py

COACH_NAME = "Marcus 'Titan' Vance"
COACH_PERSONALITY = "Strict but Fair Veteran"

# Templates for insights based on personality
INSIGHT_TEMPLATES = {
    "high_deaths": [
        "Listen up. {player} has {deaths} deaths. This isn't a shooting gallery. Play smarter, or sit on the bench.",
        "Too many mistakes from {player}. {deaths} deaths is unacceptable. Pull it together.",
        "{player}, you're feeding. {deaths} deaths. Tighten up your defense or we lose this."
    ],
    "good_kd": [
        "Absolute clinical performance, {player}. That {ratio} K/D is pure class.",
        "{player} is absolutely cooking today! Look at that {ratio} K/D.",
        "Total dominance from {player}. Keep punishing them.",
        "That's some high-level impact, {player}. Exactly what the team needs.",
        "You're making them look like amateurs, {player}. Godlike."
    ],
    "stable": [
        "Solid as a rock, {player}. You're our anchor.",
        "Love the discipline. Keep playing your game.",
        "You're winning the mental battle. Stay sharp.",
        "That's the consistency of a pro. Keep it rolling.",
        "Perfect execution. You're in the zone."
    ],
    "team_losing": [
        "The team is falling apart. K/D {ratio}. If we don't start winning duels, we're done.",
        "Macro state is poor. {ratio} K/D means our economy is bleeding. Discipline, people!",
        "Losing too many exchanges. This isn't how we practiced."
    ],
    "team_winning": [
        "Strong presence on the map. Winning exchanges. Don't let up.",
        "Economy looks solid because you're actually hitting your shots. Good.",
        "The momentum is ours. Close this out."
    ],
    "clutch": [
        "Ice in your veins! What a massive clutch!",
        "They had the numbers, but you had the skill. Incredible!",
        "You just saved our skins. That was a championship-level clutch.",
        "Never a doubt! You read them like an open book.",
        "That's how legends are made. Huge play!"
    ],
    "ace": [
        "The whole team? By yourself? You're a monster, {player}!",
        "That was a masterpiece! An ace they'll never forget.",
        "Sit down! {player} just sent the entire enemy squad home.",
        "Unstoppable! You just put the whole server on notice.",
        "Clean. Surgical. That's how you deliver an Ace."
    ],
    "death_streak": [
        "You're on a death streak. Wake up and focus!",
        "Stop dying! That's {deaths} deaths in a row. Change your position.",
        "Death after death. You're throwing! Get it together."
    ]
}

def get_random_insight(category, **kwargs):
    import random
    templates = INSIGHT_TEMPLATES.get(category, ["Insight: Stable."])
    template = random.choice(templates)
    return template.format(**kwargs)
