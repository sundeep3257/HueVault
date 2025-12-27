// Palette Generator JavaScript

let currentPalette = [];
let lockedIndices = [];
let currentSeed = Math.floor(Math.random() * 1000000);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    updateSliderValues();
});

function setupEventListeners() {
    // Sliders
    const formalPlayful = document.getElementById('formal-playful');
    const modernClassic = document.getElementById('modern-classic');
    
    formalPlayful.addEventListener('input', updateSliderValues);
    modernClassic.addEventListener('input', updateSliderValues);
    
    // Generate button
    document.getElementById('generate-btn').addEventListener('click', generatePalette);
    
    // Regenerate button
    document.getElementById('regenerate-btn').addEventListener('click', regenerateUnlocked);
    
    // Expand button
    document.getElementById('expand-btn').addEventListener('click', expandPalette);
    
    // Add color input button
    document.getElementById('add-color-input').addEventListener('click', addColorInput);
    
    // Copy all hex codes button
    const copyAllBtn = document.getElementById('copy-all-hex-btn');
    if (copyAllBtn) {
        copyAllBtn.addEventListener('click', () => {
            if (currentPalette.length === 0) {
                return;
            }
            
            // Copy all hex codes as comma-separated string
            const hexCodes = currentPalette.join(', ');
            copyToClipboard(hexCodes);
        });
    }
}

function updateSliderValues() {
    const formalPlayful = document.getElementById('formal-playful').value;
    const modernClassic = document.getElementById('modern-classic').value;
    
    document.getElementById('formal-playful-value').textContent = parseFloat(formalPlayful).toFixed(2);
    document.getElementById('modern-classic-value').textContent = parseFloat(modernClassic).toFixed(2);
}

function addColorInput() {
    const container = document.getElementById('manual-colors-input');
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'color-input';
    input.placeholder = '#FFFFFF';
    input.pattern = '^#[0-9A-Fa-f]{6}$';
    container.appendChild(input);
}

function getManualColors() {
    const inputs = document.querySelectorAll('.color-input');
    const colors = [];
    inputs.forEach(input => {
        const value = input.value.trim();
        if (value && /^#[0-9A-Fa-f]{6}$/i.test(value)) {
            colors.push(value.toUpperCase());
        }
    });
    return colors;
}

function getSelectedAdjectives() {
    const checkboxes = document.querySelectorAll('.adjective-checkboxes input[type="checkbox"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

function generatePalette() {
    const numColors = parseInt(document.getElementById('num-colors').value);
    const formalPlayful = parseFloat(document.getElementById('formal-playful').value);
    const modernClassic = parseFloat(document.getElementById('modern-classic').value);
    const adjectives = getSelectedAdjectives();
    const manualColors = getManualColors();
    
    currentSeed = Math.floor(Math.random() * 1000000);
    
    fetch('/palette/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            num_colors: numColors,
            formal_playful: formalPlayful,
            modern_classic: modernClassic,
            adjectives: adjectives,
            manual_colors: manualColors,
            seed: currentSeed
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentPalette = data.palette;
            lockedIndices = [];
            displayPalette(data.palette);
            document.getElementById('regenerate-btn').disabled = false;
            document.getElementById('expand-btn').disabled = false;
        } else {
            alert('Error generating palette: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to generate palette');
    });
}

function regenerateUnlocked() {
    if (currentPalette.length === 0) return;
    
    const formalPlayful = parseFloat(document.getElementById('formal-playful').value);
    const modernClassic = parseFloat(document.getElementById('modern-classic').value);
    const adjectives = getSelectedAdjectives();
    
    currentSeed = Math.floor(Math.random() * 1000000);
    
    fetch('/palette/regenerate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            palette: currentPalette,
            locked_indices: lockedIndices,
            formal_playful: formalPlayful,
            modern_classic: modernClassic,
            adjectives: adjectives,
            seed: currentSeed
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentPalette = data.palette;
            displayPalette(data.palette);
        } else {
            alert('Error regenerating palette: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to regenerate palette');
    });
}

function expandPalette() {
    if (currentPalette.length === 0) return;
    
    const newSize = currentPalette.length + 1;
    const formalPlayful = parseFloat(document.getElementById('formal-playful').value);
    const modernClassic = parseFloat(document.getElementById('modern-classic').value);
    const adjectives = getSelectedAdjectives();
    
    currentSeed = Math.floor(Math.random() * 1000000);
    
    fetch('/palette/expand', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            palette: currentPalette,
            new_size: newSize,
            formal_playful: formalPlayful,
            modern_classic: modernClassic,
            adjectives: adjectives,
            seed: currentSeed
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentPalette = data.palette;
            displayPalette(data.palette);
        } else {
            alert('Error expanding palette: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to expand palette');
    });
}

function displayPalette(palette) {
    const container = document.getElementById('palette-colors');
    const copyAllBtn = document.getElementById('copy-all-hex-btn');
    
    container.innerHTML = '';
    
    // Enable copy all button if palette exists
    if (palette.length > 0) {
        copyAllBtn.disabled = false;
    } else {
        copyAllBtn.disabled = true;
    }
    
    palette.forEach((color, index) => {
        const colorItem = document.createElement('div');
        colorItem.className = 'color-item';
        
        const isLocked = lockedIndices.includes(index);
        
        colorItem.innerHTML = `
            <div class="color-swatch" style="background-color: ${color};"></div>
            <div class="color-info">
                <span class="color-hex">${color}</span>
                <div class="color-actions">
                    <button class="lock-btn ${isLocked ? 'locked' : ''}" data-index="${index}" title="${isLocked ? 'Unlock' : 'Lock'}">
                        ${isLocked ? '🔒' : '🔓'}
                    </button>
                    <button class="copy-btn" data-color="${color}" title="Copy hex">
                        📋
                    </button>
                </div>
            </div>
        `;
        
        container.appendChild(colorItem);
    });
    
    // Add event listeners for lock and copy buttons
    container.querySelectorAll('.lock-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const index = parseInt(e.target.dataset.index);
            toggleLock(index);
        });
    });
    
    container.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const color = e.target.dataset.color;
            copyToClipboard(color);
        });
    });
}

function toggleLock(index) {
    if (lockedIndices.includes(index)) {
        lockedIndices = lockedIndices.filter(i => i !== index);
    } else {
        lockedIndices.push(index);
    }
    displayPalette(currentPalette);
}

