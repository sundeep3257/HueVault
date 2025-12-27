// Color Accessibility & Color-Blindness Simulator JavaScript

let currentPalette = [];

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('load-palette-btn').addEventListener('click', loadPalette);
    
    // Allow Enter key to load palette
    document.getElementById('palette-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            loadPalette();
        }
    });
});

function loadPalette() {
    const input = document.getElementById('palette-input').value.trim();
    
    if (!input) {
        alert('Please enter at least one color');
        return;
    }
    
    // Parse colors (comma-separated or space-separated)
    const colors = input.split(/[,\s]+/)
        .map(c => c.trim())
        .filter(c => c.startsWith('#') && /^#[0-9A-Fa-f]{6}$/i.test(c))
        .map(c => c.toUpperCase());
    
    if (colors.length === 0) {
        alert('No valid hex colors found. Please enter colors in format #RRGGBB');
        return;
    }
    
    currentPalette = colors;
    displayOriginalPalette(colors);
    simulateAllDeficiencies(colors);
}

function displayOriginalPalette(palette) {
    const container = document.getElementById('original-palette');
    container.innerHTML = '';
    
    if (palette.length === 0) {
        container.innerHTML = '<p class="empty-palette">No colors loaded</p>';
        return;
    }
    
    palette.forEach(color => {
        const colorItem = document.createElement('div');
        colorItem.className = 'color-item-accessibility';
        colorItem.style.backgroundColor = color;
        colorItem.innerHTML = `
            <span class="color-hex-label">${color}</span>
        `;
        container.appendChild(colorItem);
    });
}

function simulateAllDeficiencies(palette) {
    const deficiencies = ['protanopia', 'deuteranopia', 'tritanopia'];
    
    deficiencies.forEach(deficiency => {
        simulateDeficiency(palette, deficiency);
    });
}

function simulateDeficiency(palette, deficiencyType) {
    fetch('/accessibility/simulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            palette: palette,
            deficiency_type: deficiencyType
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displaySimulatedPalette(data.palette, deficiencyType);
        } else {
            console.error('Error simulating:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displaySimulatedPalette(palette, deficiencyType) {
    const containerId = `${deficiencyType}-palette`;
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    if (palette.length === 0) {
        container.innerHTML = '<p class="empty-palette">No colors</p>';
        return;
    }
    
    palette.forEach((color, index) => {
        const colorItem = document.createElement('div');
        colorItem.className = 'color-item-accessibility';
        colorItem.style.backgroundColor = color;
        colorItem.innerHTML = `
            <span class="color-hex-label">${color}</span>
        `;
        container.appendChild(colorItem);
    });
}

