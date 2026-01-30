# C9 Pulse: The AI Assistant Coach 🌩️

[![Hackathon](https://img.shields.io/badge/Hackathon-Cloud9_x_JetBrains-blue?style=flat&logo=jetbrains)](https://devpost.com/software/c9-pulse-the-ai-morale-coach)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=flat&logo=python)](https://www.python.org/)
[![API](https://img.shields.io/badge/Data-GRID_Open_Platform-green?style=flat)](https://grid.gg/)
[![AI](https://img.shields.io/badge/Powered_by-Junie_AI-purple?style=flat&logo=openai)](https://www.jetbrains.com/ai/)

> **"Moneyball with a Heart"** — An intelligent analytical engine that combines real-time strategic insights with psychological support for Valorant players.

---

## 🎨 New Visual Experience (Web Dashboard)

We have moved away from the console-only interface to a full-featured **Web Dashboard** built with **Flask**.

### ⚡ Key UI Features:
* **Dark Mode (Cloud9 Style):** A sleek, professional interface using C9's signature black, blue, and white colors.
* **C9 Pulse Logo:** Branded header with neon-effect titles.
* **Interactive Dashboard:** 
    * **Left Side:** Real-time statistics and match history.
    * **Right Side (Match Detail):** AI-driven insights and advice.
* **Visual Progress Bars:** K/D performance visualized through dynamic progress bars.
* **Team Economy Graph:** A live line chart showing team economy trends across rounds.
* **Actionable UX:** "Start Analysis" button with a loading spinner for a smooth experience.
* **Enhanced Player Cards:** Large, readable names with detailed metrics.

---

## 🧠 Advanced Analytics (Moneyball "Brain")

The core engine has been upgraded with deep analytical metrics:

* **Match History Persistence:** All analyzed matches are saved to `match_history.json` for long-term tracking.
* **Historical K/D Comparison:** Compare current performance (`Current K/D`) against the player's historical average (`Avg K/D`).
* **Trade Efficiency Metric:** Measures how effectively players are traded during exchanges: `(Kills + Assists) / Deaths`.
* **First Blood Victim Detector:** Identifies players who are dying first most frequently, allowing teams to adjust their positioning.

---

## 📺 Demo Video

[![C9 Pulse Demo](https://img.youtube.com/vi/Y7r9F2NEKbQ/0.jpg)](https://www.youtube.com/watch?v=Y7r9F2NEKbQ)

*(Click the image to watch the live demo)*

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3 (Custom C9 Theme), Bootstrap 5, Chart.js
* **Backend:** Flask (Python)
* **Data Source:** [GRID Open Platform API](https://grid.gg/platform) (GraphQL)
* **Storage:** JSON-based persistence
* **AI Co-Pilot:** Junie (JetBrains AI Agent)

---

## 🚀 Installation & Usage

### Prerequisites

-   Python 3.9 or higher
-   A GRID Open Platform API Key

### Setup

1.  **Clone the repository**

    ```bash
    git clone https://github.com/vero-code/c9-pulse.git
    cd c9-pulse
    ```
    
2.  **Install dependencies**

    ```bash
    uv sync
    ```
    
3.  **Configure Environment** Create a `.env` file in the root directory and add your key:

    ```env
    GRID_API_KEY=your_actual_api_key_here
    ```
    
4.  **Run the Web Dashboard**

    ```bash
    uv run app.py
    ```
    Open `http://127.0.0.1:5000` in your browser.

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

---

## 🔮 Future Roadmap

-   [x] **Flask Web Dashboard:** Visual dashboard for economy graphs and stats.
-   [ ] **Voice Synthesis (TTS):** Allowing the AI Coach to speak during timeouts.
-   [ ] **Predictive Models:** Using historical data to predict enemy eco-rounds.

---

## 🤝 Acknowledgments

-   **JetBrains & Cloud9:** For hosting the "Sky's the Limit" Hackathon.
-   **Junie:** For being an incredible pair programmer and helping decode the GraphQL schema.
-   **GRID:** For providing the esports data infrastructure.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built with 💙 by vero-code*