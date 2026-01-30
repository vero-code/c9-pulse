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
        "Good work, {player}. K/D of {ratio} is what I like to see. Keep that pressure on.",
        "Finally, someone showing some backbone. {player} is carrying with a {ratio} K/D. Keep it up.",
        "Solid performance, {player}. {ratio} K/D. Don't get cocky, stay focused."
    ],
    "stable": [
        "Doing your job, {player}. Keep it steady.",
        "Stable performance. No complaints for now.",
        "Consistency is key. Keep holding your line."
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
    ]
}

def get_random_insight(category, **kwargs):
    import random
    templates = INSIGHT_TEMPLATES.get(category, ["Insight: Stable."])
    template = random.choice(templates)
    return template.format(**kwargs)
