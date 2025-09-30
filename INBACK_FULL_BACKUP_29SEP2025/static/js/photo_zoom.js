// Photo zoom functionality for CSP compliance
// Moved from inline scripts to external file

function openPhotoZoom(imgSrc) {
    const modal = document.getElementById('photoZoomModal');
    const image = document.getElementById('zoomedPhoto');
    if (modal && image) {
        image.src = imgSrc;
        modal.classList.remove('hidden');
    }
}

function closePhotoZoom() {
    const modal = document.getElementById('photoZoomModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

function initializePhotoZoom() {
    // Add click handlers to all images in comparison table
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'IMG' && 
            e.target.src && 
            e.target.src !== '/static/images/no-photo.jpg' &&
            !e.target.src.includes('data:')) {
            openPhotoZoom(e.target.src);
        }
    });
    
    // Close modal when clicking on overlay
    const modal = document.getElementById('photoZoomModal');
    if (modal) {
        modal.addEventListener('click', closePhotoZoom);
    }
    
    // Prevent event bubbling when clicking on image
    const image = document.getElementById('zoomedPhoto');
    if (image) {
        image.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializePhotoZoom();
});