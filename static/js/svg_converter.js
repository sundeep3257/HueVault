// SVG Converter JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('svg-convert-form');
    const resultSection = document.getElementById('result-section');
    const errorSection = document.getElementById('error-section');
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const fileInput = document.getElementById('svg-file');
        
        if (!fileInput.files[0]) {
            showError('Please select a file');
            return;
        }
        
        // Hide previous results
        resultSection.style.display = 'none';
        errorSection.style.display = 'none';
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Converting...';
        
        fetch('/svg/convert', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Conversion failed');
                });
            }
            return response.blob();
        })
        .then(blob => {
            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = blob.name || 'converted-image';
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

