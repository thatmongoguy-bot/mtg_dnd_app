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
// --- Card Search & Deck Builder ---
let currentCard = null;
let deck = {};

// DOM refs
const cardSearch = document.getElementById('card-search');
const searchBtn = document.getElementById('search-btn');
const cardResult = document.getElementById('card-result');
const cardName = document.getElementById('card-name');
const cardType = document.getElementById('card-type');
const cardText = document.getElementById('card-text');
const cardPrice = document.getElementById('card-price');
const cardImage = document.getElementById('card-image');
const addToDeckBtn = document.getElementById('add-to-deck');
const cardCloseBtn = document.getElementById('card-close');
const deckList = document.getElementById('deck-list');
const exportBtn = document.getElementById('export-deck');
const clearBtn = document.getElementById('clear-deck');

// --- Search Card ---
searchBtn.addEventListener('click', searchCard);
cardSearch.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') searchCard();
});

async function searchCard() {
    const query = cardSearch.value.trim();
    if (!query) return;

    try {
        const response = await fetch(
            `https://api.scryfall.com/cards/search?q=${encodeURIComponent(query)}`
        );
        if (!response.ok) {
            alert('Card not found.');
            return;
        }
        const data = await response.json();
        const card = data.data[0];

        currentCard = {
            name: card.name,
            type: card.type_line || 'Unknown type',
            text: card.oracle_text || 'No text available.',
            image: card.image_uris?.normal || '',
            price: card.prices?.usd || 'N/A'
        };

        cardName.textContent = currentCard.name;
        cardType.textContent = `Type: ${currentCard.type}`;
        cardText.textContent = currentCard.text;
        cardPrice.textContent = `Price: $${currentCard.price}`;
        cardImage.src = currentCard.image;
        cardImage.alt = currentCard.name;
        cardResult.style.display = 'flex';

    } catch (error) {
        console.error('Error fetching card:', error);
        alert('Error fetching card. Please try again.');
    }
}

// --- Add to Deck ---
addToDeckBtn.addEventListener('click', () => {
    if (!currentCard) return;
    if (deck[currentCard.name]) {
        deck[currentCard.name].quantity += 1;
    } else {
        deck[currentCard.name] = { ...currentCard, quantity: 1 };
    }
    renderDeck();
    cardResult.style.display = 'none';
    cardSearch.value = '';
});

// --- Render Deck ---
function renderDeck() {
    deckList.innerHTML = '';
    const names = Object.keys(deck);
    if (names.length === 0) {
        deckList.innerHTML = '<li style="color: #888;">Deck is empty.</li>';
        return;
    }
    names.forEach(name => {
        const entry = deck[name];
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${entry.quantity}x ${name}</span>
            <button class="remove-card" data-name="${name}">✕</button>
        `;
        deckList.appendChild(li);
    });

    document.querySelectorAll('.remove-card').forEach(btn => {
        btn.addEventListener('click', function() {
            const name = this.dataset.name;
            delete deck[name];
            renderDeck();
        });
    });
}

// --- Close Card Result ---
cardCloseBtn.addEventListener('click', () => {
    cardResult.style.display = 'none';
    cardSearch.value = '';
});

// --- Export Deck ---
exportBtn.addEventListener('click', () => {
    const json = JSON.stringify(deck, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'my_deck.json';
    a.click();
    URL.revokeObjectURL(url);
});

// --- Clear Deck ---
clearBtn.addEventListener('click', () => {
    if (confirm('Clear your entire deck?')) {
        deck = {};
        renderDeck();
    }
});