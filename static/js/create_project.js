// Create Project JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('project-form');
    const resultSection = document.getElementById('result-section');
    const errorSection = document.getElementById('error-section');
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Hide previous results
        resultSection.style.display = 'none';
        errorSection.style.display = 'none';
        
        // Collect form data
        const title = document.getElementById('project-title').value.trim();
        if (!title) {
            showError('Project title is required');
            return;
        }
        
        const description = document.getElementById('project-description').value.trim();
        
        // Parse palettes
        let palettes = [];
        const palettesText = document.getElementById('project-palettes').value.trim();
        if (palettesText) {
            try {
                palettes = JSON.parse(palettesText);
            } catch (e) {
                showError('Invalid JSON format for palettes');
                return;
            }
        }
        
        // Parse URLs (one per line)
        const parseUrls = (text) => {
            return text.trim().split('\n')
                .map(line => line.trim())
                .filter(line => line.length > 0);
        };
        
        const logos = parseUrls(document.getElementById('project-logos').value);
        const favicons = parseUrls(document.getElementById('project-favicons').value);
        const graphics = parseUrls(document.getElementById('project-graphics').value);
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Creating...';
        
        fetch('/projects/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description,
                palettes: palettes,
                logos: logos,
                favicons: favicons,
                graphics: graphics
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const projectLink = document.getElementById('project-link');
                projectLink.href = data.url;
                resultSection.style.display = 'block';
            } else {
                showError(data.error || 'Failed to create project');
            }
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        })
        .catch(error => {
            showError('Failed to create project: ' + error.message);
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        });
    });
});

function showError(message) {
    const errorSection = document.getElementById('error-section');
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

