const API_BASE_URL = "http://127.0.0.1:5000/api";
let currentScenario = null;

// --- Main Game Functions ---

async function getNewScenario() {
    try {
        const response = await fetch(`${API_BASE_URL}/get_scenario`);
        const scenario = await response.json();
        currentScenario = scenario;
        loadScenarioUI(scenario);
    } catch (error) {
        console.error("Failed to fetch scenario:", error);
        document.getElementById('ta-text').innerText = "Could not connect to the game server. Make sure it's running!";
    }
}

async function submitAnswer(playerChoice) {
    if (!currentScenario) return;

    try {
        const response = await fetch(`${API_BASE_URL}/submit_answer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                scenario_id: currentScenario.scenario_id,
                choice: playerChoice
            })
        });
        const result = await response.json();
        showOutcome(result);

    } catch (error) {
        console.error("Failed to submit answer:", error);
    }
}

// --- UI Update Functions ---

function loadScenarioUI(scenario) {
    document.getElementById('pair-title').innerText = scenario.pair;
    document.getElementById('chart-image').src = scenario.image_filename;
    document.getElementById('ta-text').innerText = scenario.ta_text;
    document.getElementById('fa-text').innerText = scenario.fa_text;
}

function showOutcome(result) {
    let title;
    if (result.correct) {
        title = `✅ Congratulations! You earned +$${result.amount}!`;
    } else {
        title = `❌ Incorrect. You lost -$${Math.abs(result.amount)}.`;
    }

    // We use a simple "alert" for the pop-up.
    // It combines the title and the feedback text.
    alert(`${title}\n\nFeedback: ${result.feedback}`);

    // After the player closes the alert, load the next scenario.
    getNewScenario();
}

// --- Event Listeners ---

document.getElementById('buy-button').addEventListener('click', () => submitAnswer('BUY'));
document.getElementById('sell-button').addEventListener('click', () => submitAnswer('SELL'));

// When the page first loads, get the first scenario.
window.addEventListener('load', () => {
    getNewScenario();
});