/**
 * Match Detail Page Scripts
 */

// Confetti logic for victory
function startVictoryConfetti() {
    const duration = 5 * 1000;
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

    function randomInRange(min, max) {
        return Math.random() * (max - min) + min;
    }

    const interval = setInterval(function() {
        const timeLeft = animationEnd - Date.now();

        if (timeLeft <= 0) {
            return clearInterval(interval);
        }

        const particleCount = 50 * (timeLeft / duration);
        // since particles fall down, start a bit higher than random
        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
        confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
    }, 250);
}

// Analysis and Sound logic
function initAnalysisLogic() {
    const startBtn = document.getElementById('startAnalysisBtn');
    if (startBtn) {
        startBtn.addEventListener('click', function() {
            const btn = this;
            const text = document.getElementById('btnText');
            const spinner = document.getElementById('btnSpinner');
            const content = document.getElementById('analysisContent');

            btn.disabled = true;
            text.innerText = 'Analyzing...';
            spinner.classList.remove('d-none');

            setTimeout(() => {
                spinner.classList.add('d-none');
                text.innerText = 'Analysis Complete';
                btn.classList.remove('btn-info');
                btn.classList.add('btn-success');
                content.classList.remove('d-none');

                // Initialize chart if data is available
                if (window.matchData && window.matchData.economyHistory) {
                    initEconomyChart(window.matchData.economyHistory, window.matchData.analysis);
                }

                const audio = document.getElementById('analysisAudio');
                const ping = document.getElementById('pingSound');
                if (ping) {
                    ping.play().catch(e => console.log("Ping play failed:", e));
                }
                if (audio) {
                    setTimeout(() => {
                        audio.play().catch(e => console.log("Audio play failed:", e));
                    }, 500);
                }
            }, 1500);
        });
    }

    const muteBtn = document.getElementById('muteCoachBtn');
    if (muteBtn) {
        muteBtn.addEventListener('click', function() {
            const audio = document.getElementById('analysisAudio');
            const ping = document.getElementById('pingSound');
            const muteText = document.getElementById('muteText');
            const muteIcon = document.getElementById('muteIcon');
            
            const isMuted = audio ? !audio.muted : (ping ? !ping.muted : false);

            if (audio) audio.muted = isMuted;
            if (ping) ping.muted = isMuted;

            if (isMuted) {
                muteText.innerText = 'Unmute Coach';
                muteIcon.innerText = '🔇';
                this.classList.remove('btn-outline-secondary');
                this.classList.add('btn-danger');
            } else {
                muteText.innerText = 'Mute Coach';
                muteIcon.innerText = '🔊';
                this.classList.remove('btn-danger');
                this.classList.add('btn-outline-secondary');
            }
        });
    }

    // Update progress bars
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const width = bar.getAttribute('data-width');
        if (width) {
            bar.style.width = width + '%';
        }
        const tilt = bar.getAttribute('data-tilt');
        if (tilt) {
            bar.style.width = tilt + '%';
        }
    });
}

// Economy Chart logic
function initEconomyChart(economyHistory, analysis) {
    const ctx = document.getElementById('economyChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: economyHistory.rounds,
            datasets: [
                {
                    label: analysis[0].team_name,
                    data: economyHistory.team_a,
                    borderColor: '#00aeef',
                    backgroundColor: 'rgba(0, 174, 239, 0.1)',
                    fill: true,
                    tension: 0.3
                },
                {
                    label: analysis[1].team_name,
                    data: economyHistory.team_b,
                    borderColor: '#ffffff',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    fill: true,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: '#ffffff' }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#2d3238' },
                    ticks: { color: '#ffffff' },
                    title: {
                        display: true,
                        text: 'Value ($)',
                        color: '#ffffff'
                    }
                },
                x: {
                    grid: { color: '#2d3238' },
                    ticks: { color: '#ffffff' }
                }
            }
        }
    });
}

// Chat Logic
function initChatLogic() {
    const coachChat = document.getElementById('coachChat');
    const chatHeader = document.getElementById('chatHeader');
    const chatToggle = document.getElementById('chatToggle');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatBody = document.getElementById('chatBody');

    if (chatHeader && coachChat && chatToggle) {
        chatHeader.addEventListener('click', () => {
            coachChat.classList.toggle('chat-minimized');
            chatToggle.innerText = coachChat.classList.contains('chat-minimized') ? '+' : '−';
        });
    }

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            // Add user message
            addMessage(message, 'user');
            chatInput.value = '';

            // Show thinking indicator
            const thinkingDiv = showThinking();

            try {
                const response = await fetch('/ask_coach', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                
                // Simulate typing delay
                setTimeout(() => {
                    thinkingDiv.remove();
                    addMessage(data.response, 'coach');
                }, 500);
            } catch (err) {
                console.error('Chat error:', err);
                thinkingDiv.remove();
                addMessage('Connection lost. I am busy anyway.', 'coach');
            }
        });
    }

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.className = `chat-message ${sender}`;
        div.innerText = text;
        chatBody.appendChild(div);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function showThinking() {
        const div = document.createElement('div');
        div.className = 'chat-message coach typing-indicator';
        div.innerHTML = '<span></span><span></span><span></span>';
        chatBody.appendChild(div);
        chatBody.scrollTop = chatBody.scrollHeight;
        return div;
    }
}

// Initialize everything on DOM Content Loaded
window.addEventListener('DOMContentLoaded', () => {
    if (window.matchData && window.matchData.matchFinished) {
        startVictoryConfetti();
    }
    initAnalysisLogic();
    initChatLogic();
});
