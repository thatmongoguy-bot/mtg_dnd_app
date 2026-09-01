// --- State ---
let game = {
    format: 'Standard',
    players: [],
    currentTurn: 0
};

// --- DOM references ---
const setupScreen = document.getElementById('setup-screen');
const gameScreen = document.getElementById('game-screen');
const playerNamesDiv = document.getElementById('player-names');
const playersContainer = document.getElementById('players-container');
const playerCountInput = document.getElementById('player-count');

// --- Player name fields update ---
playerCountInput.addEventListener('input', updateNameFields);

function updateNameFields() {
    const count = parseInt(playerCountInput.value) || 2;
    playerNamesDiv.innerHTML = '';
    for (let i = 0; i < count; i++) {
        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = `Player ${i + 1} name`;
        input.dataset.index = i;
        playerNamesDiv.appendChild(input);
    }
}
updateNameFields();

// --- Start Game ---
document.getElementById('start-btn').addEventListener('click', startGame);

function startGame() {
    const format = document.querySelector('input[name="format"]:checked').value;
    const nameInputs = playerNamesDiv.querySelectorAll('input');
    const names = [];
    nameInputs.forEach(inp => {
        if (inp.value.trim()) names.push(inp.value.trim());
    });

    if (names.length < 2) {
        alert('Please enter at least 2 player names.');
        return;
    }

    const startingLife = format === 'Commander' ? 40 : 20;
    game = {
        format: format,
        players: names.map(name => ({
            name: name,
            life: startingLife,
            poison: 0
        })),
        currentTurn: 0
    };

    setupScreen.style.display = 'none';
    gameScreen.style.display = 'block';
    renderGame();
}

// --- Render Game ---
function renderGame() {
    playersContainer.innerHTML = '';
    game.players.forEach((player, index) => {
        const card = document.createElement('section');
        card.className = 'player-card';
        if (index === game.currentTurn) {
            card.classList.add('current-turn');
        }

        card.innerHTML = `
            <h3>${player.name} ${index === game.currentTurn ? '👑' : ''}</h3>
            <div class="life-row">
                <button data-action="life" data-index="${index}" data-amount="-1">−</button>
                <span>${player.life}</span>
                <button data-action="life" data-index="${index}" data-amount="1">+</button>
            </div>
            <div class="poison-row">
                <span>☠️ Poison: ${player.poison}</span>
                <button data-action="poison" data-index="${index}">+ Poison</button>
            </div>
        `;
        playersContainer.appendChild(card);
    });

    // Attach event listeners
    document.querySelectorAll('[data-action="life"]').forEach(btn => {
        btn.addEventListener('click', function() {
            const idx = parseInt(this.dataset.index);
            const amount = parseInt(this.dataset.amount);
            game.players[idx].life += amount;
            renderGame();
        });
    });

    document.querySelectorAll('[data-action="poison"]').forEach(btn => {
        btn.addEventListener('click', function() {
            const idx = parseInt(this.dataset.index);
            game.players[idx].poison += 1;
            renderGame();
        });
    });
}

// --- Dice Rolls ---
document.getElementById('roll-d20').addEventListener('click', () => {
    const result = Math.floor(Math.random() * 20) + 1;
    alert(`🎲 d20: ${result}`);
});

document.getElementById('roll-d6').addEventListener('click', () => {
    const result = Math.floor(Math.random() * 6) + 1;
    alert(`🎲 d6: ${result}`);
});

// --- Next Turn ---
document.getElementById('next-turn').addEventListener('click', () => {
    game.currentTurn = (game.currentTurn + 1) % game.players.length;
    renderGame();
});