# C9 Pulse: The AI Assistant Coach 🌩️

[![Hackathon](https://img.shields.io/badge/Hackathon-Cloud9_x_JetBrains-blue?style=flat&logo=jetbrains)](https://devpost.com/software/c9-pulse-the-ai-morale-coach)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=flat&logo=python)](https://www.python.org/)
[![API](https://img.shields.io/badge/Data-GRID_Open_Platform-green?style=flat)](https://grid.gg/)
[![AI](https://img.shields.io/badge/Powered_by-Junie_AI-purple?style=flat&logo=openai)](https://www.jetbrains.com/ai/)

> **"Moneyball with a Heart"** — An intelligent analytical engine that combines real-time strategic insights with psychological support for Valorant players.

---

## 📺 Demo Video

[![C9 Pulse Demo](https://img.youtube.com/vi/Y7r9F2NEKbQ/0.jpg)](https://www.youtube.com/watch?v=Y7r9F2NEKbQ)

*(Click the image to watch the live demo)*

---

## 📖 About The Project

**C9 Pulse** is a dual-layer Assistant Coach built for the **Sky’s the Limit - Cloud9 x JetBrains Hackathon**. 

In competitive esports, mechanical skill is only half the battle. The other half is mental resilience and strategic adaptability. C9 Pulse solves the problem of "information overload" by acting as a real-time analyst that filters raw match data into actionable advice.

### Key Features

#### 🧠 1. The Analyst (Micro & Macro Insights)
Powered by a custom `MatchAnalyzer` engine, the app processes the **GRID Live Data Feed**:
* **Micro-Insights:** Detects individual performance outliers.
    * *Example:* "Oscarinin is winning 80% of opening duels. Suggestion: Keep playing aggressive angles."
* **Macro-Review:** Analyzes team economy and trading efficiency.
    * *Example:* "Team is losing rounds due to forced buys (K/D ratio < 0.7). Recommendation: Save next round."

#### ❤️ 2. The Hype Man (Emotional Support)
Unlike dry stat tools, C9 Pulse manages the player's mental state:
* **Momentum Validation:** Celebrates clutches and multi-kills to boost morale.
* **Tilt Prevention:** Offers constructive, calm advice after repeated deaths to prevent tilt.

---

## 🛠️ Tech Stack

* **Core:** Python 3.x
* **Data Source:** [GRID Open Platform API](https://grid.gg/platform) (GraphQL)
* **Development:** JetBrains IDE (PyCharm/IntelliJ)
* **AI Co-Pilot:** Junie (JetBrains AI Agent)

---

## 🧩 Technical Deep Dive

### The "Live Data" Breakthrough
One of the biggest technical challenges was accessing granular player statistics (Kills/Deaths) via the standard Open Platform API. The default `central-data` endpoint provided only schedule information.

**How I solved it:**
Using **Junie (JetBrains AI)**, I reverse-engineered the query structure and identified the access point for the **Live Data Feed** (`series-state`). 
I wrote a custom GraphQL client in Python that bypasses the static data limitations, fetching real-time game states directly.

```python
# Example of the Live Data Query utilized
query GetSeriesState($id: ID!) {
  seriesState(id: $id) {
    games {
      teams {
        players {
          name
          kills  # Accessed via flat structure
          deaths
        }
      }
    }
  }
}
```

## 🚀 Installation & Usage

### Prerequisites

-   Python 3.9 or higher
    
-   A GRID Open Platform API Key
    

### Setup

1.  **Clone the repository**

    ```
    git clone https://github.com/vero-code/c9-pulse.git
    cd c9-pulse
    ```
    
2.  **Install uv** (if not installed)
    Follow the instructions at [astral.sh/uv](https://astral.sh/uv).

3.  **Install dependencies**

    ```
    uv sync
    ```
    
4.  **Configure Environment** Create a `.env` file in the root directory and add your key:

    ```
    GRID_API_KEY=your_actual_api_key_here
    ```
    
5.  **Run the Assistant**

    ```
    uv run main.py
    ```

----------

## 📊 Example Output

When running, the console provides real-time analysis of active or recent matches:

Plaintext

```
📢 Match: Fnatic vs Karmine Corp (ID: 2618420)
   👤 Analyzing Player: Oscarinin
   > 🔥 Insight: Excellent performance (K/D 7.0). Keep playing aggressive.
   
   🛡️ Analyzing Team Economy: Fnatic
   > 📈 Macro Review: Team winning exchanges. Economy looks strong.

```

----------

## 🔮 Future Roadmap

-   [ ] **React Frontend:** Visual dashboard for economy graphs.
    
-   [ ] **Voice Synthesis (TTS):** Allowing the AI Coach to speak during timeouts.
    
-   [ ] **Predictive Models:** Using historical data to predict enemy eco-rounds.
    

----------

## 🤝 Acknowledgments

-   **JetBrains & Cloud9:** For hosting the "Sky's the Limit" Hackathon.
    
-   **Junie:** For being an incredible pair programmer and helping decode the GraphQL schema.
    
-   **GRID:** For providing the esports data infrastructure.
    
----------

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

----------

*Built with 💙 by vero-code*