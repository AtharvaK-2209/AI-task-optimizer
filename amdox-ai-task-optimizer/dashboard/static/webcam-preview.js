/**
 * Floating Webcam Preview Component
 * Shows live camera feed in a draggable floating window
 */

class WebcamPreview {
    constructor() {
        this.videoElement = null;
        this.containerElement = null;
        this.stream = null;
        this.isDragging = false;
        this.currentX = 0;
        this.currentY = 0;
        this.initialX = 0;
        this.initialY = 0;
        this.xOffset = 0;
        this.yOffset = 0;
    }

    /**
     * Initialize and show the webcam preview
     */
    async show() {
        if (this.containerElement) {
            this.containerElement.style.display = 'block';
            return;
        }

        // Create the floating container
        this.createContainer();
        
        // Request camera access
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                },
                audio: false
            });

            // Attach stream to video element
            this.videoElement.srcObject = this.stream;
            this.videoElement.play();

            console.log('✅ Webcam preview started');
        } catch (error) {
            console.error('❌ Camera access error:', error);
            this.showError('Camera access denied. Please allow camera permissions.');
        }
    }

    /**
     * Create the floating container HTML
     */
    createContainer() {
        // Create container
        this.containerElement = document.createElement('div');
        this.containerElement.id = 'webcam-preview-container';
        this.containerElement.className = 'webcam-preview-container';

        // Create header (draggable area)
        const header = document.createElement('div');
        header.className = 'webcam-preview-header';
        header.innerHTML = `
            <span class="webcam-preview-title">📷 Live Camera</span>
            <button class="webcam-preview-close" id="webcam-close-btn">×</button>
        `;

        // Create video element
        this.videoElement = document.createElement('video');
        this.videoElement.className = 'webcam-preview-video';
        this.videoElement.autoplay = true;
        this.videoElement.playsInline = true;
        this.videoElement.muted = true;

        // Create status indicator
        const statusIndicator = document.createElement('div');
        statusIndicator.className = 'webcam-status-indicator';
        statusIndicator.innerHTML = '<span class="status-dot"></span> Live';

        // Assemble container
        this.containerElement.appendChild(header);
        this.containerElement.appendChild(this.videoElement);
        this.containerElement.appendChild(statusIndicator);

        // Add to body
        document.body.appendChild(this.containerElement);

        // Setup event listeners
        this.setupEventListeners();
    }

    /**
     * Setup drag and close event listeners
     */
    setupEventListeners() {
        const header = this.containerElement.querySelector('.webcam-preview-header');
        const closeBtn = document.getElementById('webcam-close-btn');

        // Drag functionality
        header.addEventListener('mousedown', this.dragStart.bind(this));
        document.addEventListener('mousemove', this.drag.bind(this));
        document.addEventListener('mouseup', this.dragEnd.bind(this));

        // Touch support for mobile
        header.addEventListener('touchstart', this.dragStart.bind(this));
        document.addEventListener('touchmove', this.drag.bind(this));
        document.addEventListener('touchend', this.dragEnd.bind(this));

        // Close button
        closeBtn.addEventListener('click', this.hide.bind(this));
    }

    /**
     * Drag start handler
     */
    dragStart(e) {
        if (e.type === 'touchstart') {
            this.initialX = e.touches[0].clientX - this.xOffset;
            this.initialY = e.touches[0].clientY - this.yOffset;
        } else {
            this.initialX = e.clientX - this.xOffset;
            this.initialY = e.clientY - this.yOffset;
        }

        if (e.target.closest('.webcam-preview-header')) {
            this.isDragging = true;
            this.containerElement.style.cursor = 'grabbing';
        }
    }

    /**
     * Drag handler
     */
    drag(e) {
        if (this.isDragging) {
            e.preventDefault();

            if (e.type === 'touchmove') {
                this.currentX = e.touches[0].clientX - this.initialX;
                this.currentY = e.touches[0].clientY - this.initialY;
            } else {
                this.currentX = e.clientX - this.initialX;
                this.currentY = e.clientY - this.initialY;
            }

            this.xOffset = this.currentX;
            this.yOffset = this.currentY;

            this.setTranslate(this.currentX, this.currentY);
        }
    }

    /**
     * Drag end handler
     */
    dragEnd() {
        this.initialX = this.currentX;
        this.initialY = this.currentY;
        this.isDragging = false;
        if (this.containerElement) {
            this.containerElement.style.cursor = 'grab';
        }
    }

    /**
     * Set element position
     */
    setTranslate(xPos, yPos) {
        this.containerElement.style.transform = `translate(${xPos}px, ${yPos}px)`;
    }

    /**
     * Hide the webcam preview
     */
    hide() {
        if (this.containerElement) {
            this.containerElement.style.display = 'none';
        }
        console.log('📷 Webcam preview hidden');
    }

    /**
     * Stop camera stream and cleanup
     */
    destroy() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => {
                track.stop();
                console.log('🛑 Camera track stopped');
            });
            this.stream = null;
        }

        if (this.videoElement) {
            this.videoElement.srcObject = null;
        }

        if (this.containerElement) {
            this.containerElement.remove();
            this.containerElement = null;
        }

        console.log('🧹 Webcam preview cleaned up');
    }

    /**
     * Show error message
     */
    showError(message) {
        if (this.containerElement) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'webcam-error';
            errorDiv.textContent = message;
            this.containerElement.appendChild(errorDiv);
        }
    }

    /**
     * Check if preview is currently visible
     */
    isVisible() {
        return this.containerElement && this.containerElement.style.display !== 'none';
    }
}

// Export for use in other scripts
window.WebcamPreview = WebcamPreview;