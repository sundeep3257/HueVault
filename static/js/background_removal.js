// Background Removal Tool JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('bg-remove-form');
    const colorPicker = document.getElementById('bg-color-picker');
    const colorInput = document.getElementById('bg-color');
    const toleranceSlider = document.getElementById('tolerance');
    const toleranceValue = document.getElementById('tolerance-value');
    
    // Sync color picker and text input
    colorPicker.addEventListener('input', (e) => {
        colorInput.value = e.target.value.toUpperCase();
    });
    
    colorInput.addEventListener('input', (e) => {
        if (/^#[0-9A-Fa-f]{6}$/i.test(e.target.value)) {
            colorPicker.value = e.target.value;
        }
    });
    
    // Update tolerance value display
    toleranceSlider.addEventListener('input', (e) => {
        toleranceValue.textContent = e.target.value;
    });
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const fileInput = document.getElementById('image-file');
        
        if (!fileInput.files[0]) {
            showError('Please select a file');
            return;
        }
        
        // Validate color
        const bgColor = colorInput.value.trim();
        if (!/^#[0-9A-Fa-f]{6}$/i.test(bgColor)) {
            showError('Please enter a valid hex color (e.g., #FFFFFF)');
            return;
        }
        
        // Hide previous results
        const resultSection = document.getElementById('result-section');
        const errorSection = document.getElementById('error-section');
        resultSection.style.display = 'none';
        errorSection.style.display = 'none';
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
        
        fetch('/background/remove', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Processing failed');
                });
            }
            return response.blob();
        })
        .then(blob => {
            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = blob.name || 'image-no-bg';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            resultSection.style.display = 'block';
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        })
        .catch(error => {
            showError(error.message);
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

