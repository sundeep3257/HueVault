// Archive Edit JavaScript with Preview Functionality
// archiveUsername, updateUrl, and addProjectUrl are defined in the template

// Display name editing
document.getElementById('edit-name-btn').addEventListener('click', () => {
    const displayName = document.getElementById('archive-display-name');
    displayName.contentEditable = 'true';
    displayName.focus();
    document.getElementById('edit-name-btn').style.display = 'none';
    document.getElementById('save-name-btn').style.display = 'inline-block';
});

document.getElementById('save-name-btn').addEventListener('click', () => {
    const displayName = document.getElementById('archive-display-name').textContent.trim();
    
    fetch(updateUrl, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({display_name: displayName})
    })
    .then(response => response.json())
    .then(data => {
        const nameEl = document.getElementById('archive-display-name');
        nameEl.contentEditable = 'false';
        document.getElementById('edit-name-btn').style.display = 'inline-block';
        document.getElementById('save-name-btn').style.display = 'none';
    });
});

// Preview functionality
function parsePalette(paletteInput) {
    return paletteInput.split(/[,\s\n]+/)
        .map(c => c.trim())
        .filter(c => /^#[0-9A-Fa-f]{6}$/i.test(c))
        .map(c => c.toUpperCase());
}

function updatePreview(previewContainer, title, palette, images, layoutSettings) {
    previewContainer.innerHTML = '';
    
    if (!title && palette.length === 0 && images.length === 0) {
        previewContainer.innerHTML = '<div class="preview-placeholder">Enter project details to see preview</div>';
        return;
    }
    
    const previewCard = document.createElement('div');
    previewCard.className = 'project-card-full';
    
    if (title) {
        const titleEl = document.createElement('h3');
        titleEl.textContent = title;
        previewCard.appendChild(titleEl);
    }
    
    if (palette.length > 0) {
        const paletteDiv = document.createElement('div');
        paletteDiv.className = 'palette-display-short';
        palette.forEach(color => {
            const swatch = document.createElement('div');
            swatch.className = 'color-swatch-short';
            swatch.style.backgroundColor = color;
            swatch.title = color;
            const hexOverlay = document.createElement('span');
            hexOverlay.className = 'color-hex-overlay';
            hexOverlay.textContent = color;
            swatch.appendChild(hexOverlay);
            paletteDiv.appendChild(swatch);
        });
        previewCard.appendChild(paletteDiv);
    }
    
    if (images.length > 0) {
        const gallery = document.createElement('div');
        gallery.className = 'graphics-gallery';
        gallery.style.cssText = `
            grid-template-columns: repeat(auto-fill, minmax(${layoutSettings.width}px, 1fr));
            gap: ${layoutSettings.gap}px;
        `;
        
        images.forEach((imageUrl, index) => {
            const item = document.createElement('div');
            item.className = 'graphic-item';
            item.style.cssText = `
                width: ${layoutSettings.width}px;
                height: ${layoutSettings.height}px;
                border-radius: ${layoutSettings.radius}px;
            `;
            
            const img = document.createElement('img');
            img.src = imageUrl;
            img.style.cssText = `
                object-fit: ${layoutSettings.fit};
                width: 100%;
                height: 100%;
                border-radius: ${layoutSettings.radius}px;
            `;
            item.appendChild(img);
            gallery.appendChild(item);
        });
        previewCard.appendChild(gallery);
    }
    
    previewContainer.appendChild(previewCard);
}

// Add project form with live preview
const addProjectForm = document.getElementById('add-project-form');
const previewContainer = document.getElementById('project-preview');

function updateAddProjectPreview() {
    const title = document.getElementById('project-title').value.trim();
    const paletteInput = document.getElementById('project-palette').value;
    const palette = parsePalette(paletteInput);
    const imageFiles = document.getElementById('project-images').files;
    
    const images = [];
    for (let i = 0; i < imageFiles.length; i++) {
        images.push(URL.createObjectURL(imageFiles[i]));
    }
    
    const layoutSettings = {
        width: parseInt(document.getElementById('img-width').value) || 260,
        height: parseInt(document.getElementById('img-height').value) || 200,
        fit: document.getElementById('img-fit').value || 'cover',
        radius: parseInt(document.getElementById('img-radius').value) || 8,
        gap: parseInt(document.getElementById('img-gap').value) || 16
    };
    
    updatePreview(previewContainer, title, palette, images, layoutSettings);
}

// Add event listeners for live preview
['project-title', 'project-palette', 'project-images', 'img-width', 'img-height', 'img-fit', 'img-radius', 'img-gap'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
        el.addEventListener('input', updateAddProjectPreview);
        el.addEventListener('change', updateAddProjectPreview);
    }
});

addProjectForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('title', document.getElementById('project-title').value);
    
    const paletteInput = document.getElementById('project-palette').value;
    const paletteArray = parsePalette(paletteInput);
    formData.append('palette', JSON.stringify(paletteArray));
    
    formData.append('img_width', document.getElementById('img-width').value);
    formData.append('img_height', document.getElementById('img-height').value);
    formData.append('img_fit', document.getElementById('img-fit').value);
    formData.append('img_radius', document.getElementById('img-radius').value);
    formData.append('img_gap', document.getElementById('img-gap').value);
    
    const images = document.getElementById('project-images').files;
    for (let i = 0; i < images.length; i++) {
        formData.append('images', images[i]);
    }
    
    fetch(addProjectUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error: ' + (data.error || 'Failed to add project'));
        }
    });
});

// Edit project functionality
let currentEditProjectId = null;

document.querySelectorAll('.btn-edit-project').forEach(btn => {
    btn.addEventListener('click', () => {
        const projectId = btn.dataset.projectId;
        const projectCard = document.querySelector(`[data-project-id="${projectId}"]`);
        const projectTitle = projectCard.querySelector('h3').textContent;
        
        // Fetch project data (we'll need to get it from the page or make an API call)
        // For now, we'll extract from the DOM
        const paletteSwatches = projectCard.querySelectorAll('.color-swatch-short');
        const palette = Array.from(paletteSwatches).map(s => s.style.backgroundColor);
        
        // Get layout from inline styles if available
        const gallery = projectCard.querySelector('.graphics-gallery');
        const firstItem = gallery ? gallery.querySelector('.graphic-item') : null;
        
        document.getElementById('edit-project-id').value = projectId;
        document.getElementById('edit-project-title').value = projectTitle;
        document.getElementById('edit-project-palette').value = palette.map(c => rgbToHex(c)).join(', ');
        
        if (firstItem) {
            const style = firstItem.style;
            document.getElementById('edit-img-width').value = parseInt(style.width) || 260;
            document.getElementById('edit-img-height').value = parseInt(style.height) || 200;
            document.getElementById('edit-img-radius').value = parseInt(style.borderRadius) || 8;
        }
        
        document.getElementById('edit-project-modal').style.display = 'block';
        currentEditProjectId = projectId;
        updateEditProjectPreview();
    });
});

function rgbToHex(rgb) {
    if (rgb.startsWith('#')) return rgb;
    const match = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
    if (!match) return rgb;
    return '#' + [1, 2, 3].map(i => ('0' + parseInt(match[i]).toString(16)).slice(-2)).join('').toUpperCase();
}

function updateEditProjectPreview() {
    const title = document.getElementById('edit-project-title').value.trim();
    const paletteInput = document.getElementById('edit-project-palette').value;
    const palette = parsePalette(paletteInput);
    const imageFiles = document.getElementById('edit-project-images').files;
    
    const images = [];
    for (let i = 0; i < imageFiles.length; i++) {
        images.push(URL.createObjectURL(imageFiles[i]));
    }
    
    // Also include existing images
    const projectCard = document.querySelector(`[data-project-id="${currentEditProjectId}"]`);
    if (projectCard) {
        const existingImgs = projectCard.querySelectorAll('.graphic-item img');
        existingImgs.forEach(img => images.push(img.src));
    }
    
    const layoutSettings = {
        width: parseInt(document.getElementById('edit-img-width').value) || 260,
        height: parseInt(document.getElementById('edit-img-height').value) || 200,
        fit: document.getElementById('edit-img-fit').value || 'cover',
        radius: parseInt(document.getElementById('edit-img-radius').value) || 8,
        gap: parseInt(document.getElementById('edit-img-gap').value) || 16
    };
    
    updatePreview(document.getElementById('edit-project-preview'), title, palette, images, layoutSettings);
}

['edit-project-title', 'edit-project-palette', 'edit-project-images', 'edit-img-width', 'edit-img-height', 'edit-img-fit', 'edit-img-radius', 'edit-img-gap'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
        el.addEventListener('input', updateEditProjectPreview);
        el.addEventListener('change', updateEditProjectPreview);
    }
});

document.getElementById('edit-project-form').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const projectId = document.getElementById('edit-project-id').value;
    const formData = new FormData();
    formData.append('title', document.getElementById('edit-project-title').value);
    
    const paletteInput = document.getElementById('edit-project-palette').value;
    const paletteArray = parsePalette(paletteInput);
    formData.append('palette', JSON.stringify(paletteArray));
    
    formData.append('img_width', document.getElementById('edit-img-width').value);
    formData.append('img_height', document.getElementById('edit-img-height').value);
    formData.append('img_fit', document.getElementById('edit-img-fit').value);
    formData.append('img_radius', document.getElementById('edit-img-radius').value);
    formData.append('img_gap', document.getElementById('edit-img-gap').value);
    
    const images = document.getElementById('edit-project-images').files;
    for (let i = 0; i < images.length; i++) {
        formData.append('images', images[i]);
    }
    
    fetch(`/archives/${archiveUsername}/projects/${projectId}/update`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error: ' + (data.error || 'Failed to update project'));
        }
    });
});

document.getElementById('cancel-edit').addEventListener('click', () => {
    document.getElementById('edit-project-modal').style.display = 'none';
});

// Delete project
document.querySelectorAll('.btn-delete-project').forEach(btn => {
    btn.addEventListener('click', () => {
        if (!confirm('Are you sure you want to delete this project?')) return;
        
        const projectId = btn.dataset.projectId;
        fetch(`/archives/${archiveUsername}/projects/${projectId}/delete`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'Failed to delete project'));
            }
        });
    });
});

// Delete image
document.querySelectorAll('.btn-delete-image').forEach(btn => {
    btn.addEventListener('click', () => {
        if (!confirm('Delete this image?')) return;
        
        const imageId = btn.dataset.imageId;
        const projectId = btn.closest('[data-project-id]').dataset.projectId;
        
        fetch(`/archives/${archiveUsername}/projects/${projectId}/images/${imageId}/delete`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'Failed to delete image'));
            }
        });
    });
});

// Delete archive
document.getElementById('delete-archive-btn').addEventListener('click', () => {
    const confirmedUsername = prompt(`Type the username "${archiveUsername}" to confirm archive deletion:`);
    
    if (confirmedUsername === null) {
        return; // User cancelled
    }
    
    if (confirmedUsername.trim().toLowerCase() !== archiveUsername.toLowerCase()) {
        alert('Username does not match. Deletion cancelled.');
        return;
    }
    
    if (!confirm('Are you sure you want to delete this archive? This action cannot be undone.')) {
        return;
    }
    
    fetch(`/archives/${archiveUsername}/delete`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: confirmedUsername.trim().toLowerCase()})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/archives?deleted=1';
        } else {
            alert('Error: ' + (data.error || 'Failed to delete archive'));
        }
    });
});

