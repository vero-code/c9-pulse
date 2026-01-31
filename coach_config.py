from typing import Dict, List, Any, Optional
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# coach_config.py

COACH_NAME: str = "Marcus 'Titan' Vance"
COACH_PERSONALITY: str = "Strict but Fair Veteran"

# Initialize Gemini Client
client: Optional[genai.Client] = None
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)

# Templates for insights based on personality
INSIGHT_TEMPLATES: Dict[str, Any] = {
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
        "Losing too many exchanges. This isn't how we practiced.",
        "Unlucky, reset mental. We can still pull this back.",
        "Take a breath. It was a tough round, but it's over. Focus on the next one.",
        "Don't let that loss get in your head. Reset and go again.",
        "Shake it off. We've been in worse spots than this. Stay composed.",
        "Flush it. New round, new start. Eyes on the prize."
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
    ],
    "timeout_talk": [
        "Half-time report, team. {team_a} {score_a}, {team_b} {score_b}. {mvp} is carrying, while {underperformer} needs to wake up. {economy_insight}. Let's focus!",
        "Midway mark reached. {team_a} vs {team_b}. Score is {score_a} to {score_b}. {mvp} is the MVP so far. {underperformer}, we need more from you. {economy_insight}. Keep the pressure on!",
        "Alright, listen up. We're halfway through. {score_a} for {team_a}, {score_b} for {team_b}. {mvp} is doing great. {underperformer}, pick up the pace. {economy_insight}. Win this next half!"
    ],
    "chat_responses": {
        "greeting": [
            "What do you want? I'm busy watching the game.",
            "Make it quick. We've got a match to win.",
            "You again? Hope you have something useful to say."
        ],
        "default": [
            "I don't have time for this. Focus on the game.",
            "What kind of question is that? Stay sharp!",
            "Ask me something that actually helps us win."
        ],
        "performance_query": [
            "Look at the stats. They don't lie. We need more impact.",
            "If you're asking, you already know the answer. We need to do better.",
            "Consistency is key. Right now, we're lacking it."
        ],
        "economy_query": [
            "Money management is everything. Don't waste your credits.",
            "If we don't fix our economy, we're finished. Buy smart.",
            "Control the economy, control the game. It's that simple."
        ]
    }
}

def get_random_insight(category: str, **kwargs: Any) -> str:
    """
    Retrieve a random formatted insight string for a given category.

    Args:
        category: The insight category (e.g., 'good_kd', 'ace').
        **kwargs: Values to format into the template.

    Returns:
        A formatted insight string.
    """
    import random
    templates = INSIGHT_TEMPLATES.get(category, ["Insight: Stable."])
    template = random.choice(templates)
    return template.format(**kwargs)

def get_chat_response(message: str) -> str:
    """
    Select an appropriate coach response based on the user's message using Gemini API.

    Args:
        message: The user's input message.

    Returns:
        A coach response string generated by Gemini.
    """
    if not client:
        return "I'm off the clock. (API Key missing)"

    prompt = f"""
    You are {COACH_NAME}, a professional Valorant coach with a {COACH_PERSONALITY} personality.
    A player or fan is asking you a question: "{message}"
    
    Respond as the coach. Keep it concise, authentic, and stay in character.
    Do not use emojis unless they fit the 'Strict but Fair' vibe (rarely).
    Maximum 2-3 sentences.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=512,
                temperature=0.7,
            )
        )
        # Use result.text to get the full response
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I've got nothing for you right now. (Connection issue)"
