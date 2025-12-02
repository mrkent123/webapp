// iOS Safe Area Debugging Tool
// Visualizes and debugs iOS safe area issues

class IOSSafeAreaDebugger {
    constructor() {
        this.safeAreaVisualizer = null;
        this.isActive = false;
        this.safeAreaValues = {
            top: '0px',
            right: '0px',
            bottom: '0px',
            left: '0px'
        };
        
        this.init();
    }

    init() {
        // Get safe area values from CSS environment variables
        this.updateSafeAreaValues();
        
        // Create visualizer if iOS device is detected
        if (this.isIOS()) {
            this.createSafeAreaVisualizer();
        }
        
        // Monitor for changes
        this.startMonitoring();
    }

    isIOS() {
        return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    }

    updateSafeAreaValues() {
        const rootStyles = getComputedStyle(document.documentElement);
        
        this.safeAreaValues = {
            top: rootStyles.getPropertyValue('--safe-area-top') || 
                 getComputedStyle(document.body).getPropertyValue('--safe-area-top') ||
                 `env(safe-area-inset-top, 0px)`,
            right: rootStyles.getPropertyValue('--safe-area-right') ||
                  getComputedStyle(document.body).getPropertyValue('--safe-area-right') ||
                  `env(safe-area-inset-right, 0px)`,
            bottom: rootStyles.getPropertyValue('--safe-area-bottom') ||
                   getComputedStyle(document.body).getPropertyValue('--safe-area-bottom') ||
                   `env(safe-area-inset-bottom, 0px)`,
            left: rootStyles.getPropertyValue('--safe-area-left') ||
                 getComputedStyle(document.body).getPropertyValue('--safe-area-left') ||
                 `env(safe-area-inset-left, 0px)`
        };
    }

    createSafeAreaVisualizer() {
        // Create visual overlay elements for safe areas
        const overlay = document.createElement('div');
        overlay.id = 'safe-area-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 9998;
            box-sizing: border-box;
        `;
        
        // Top safe area (notch area)
        const topSafe = document.createElement('div');
        topSafe.className = 'safe-area-visualizer top';
        topSafe.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: ${this.safeAreaValues.top};
            background: rgba(255, 0, 0, 0.3);
            border-bottom: 2px dashed rgba(255, 255, 255, 0.7);
        `;
        
        // Right safe area
        const rightSafe = document.createElement('div');
        rightSafe.className = 'safe-area-visualizer right';
        rightSafe.style.cssText = `
            position: absolute;
            top: ${this.safeAreaValues.top};
            right: 0;
            bottom: ${this.safeAreaValues.bottom};
            width: ${this.safeAreaValues.right};
            background: rgba(0, 255, 0, 0.3);
            border-left: 2px dashed rgba(255, 255, 255, 0.7);
        `;
        
        // Bottom safe area (home indicator)
        const bottomSafe = document.createElement('div');
        bottomSafe.className = 'safe-area-visualizer bottom';
        bottomSafe.style.cssText = `
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: ${this.safeAreaValues.bottom};
            background: rgba(0, 0, 255, 0.3);
            border-top: 2px dashed rgba(255, 255, 255, 0.7);
        `;
        
        // Left safe area
        const leftSafe = document.createElement('div');
        leftSafe.className = 'safe-area-visualizer left';
        leftSafe.style.cssText = `
            position: absolute;
            top: ${this.safeAreaValues.top};
            left: 0;
            bottom: ${this.safeAreaValues.bottom};
            width: ${this.safeAreaValues.left};
            background: rgba(255, 255, 0, 0.3);
            border-right: 2px dashed rgba(255, 255, 255, 0.7);
        `;
        
        // Add labels to each safe area
        const topLabel = this.createLabel('Safe Area Top', 'red');
        topLabel.style.top = '5px';
        topLabel.style.left = '5px';
        
        const rightLabel = this.createLabel('Safe Area Right', 'lime');
        rightLabel.style.top = '50%';
        rightLabel.style.right = '5px';
        rightLabel.style.transform = 'translateY(-50%)';
        
        const bottomLabel = this.createLabel('Safe Area Bottom', 'blue');
        bottomLabel.style.bottom = '5px';
        bottomLabel.style.left = '5px';
        
        const leftLabel = this.createLabel('Safe Area Left', 'yellow');
        leftLabel.style.top = '50%';
        leftLabel.style.left = '5px';
        leftLabel.style.transform = 'translateY(-50%)';
        
        // Add all elements to overlay
        topSafe.appendChild(topLabel);
        rightSafe.appendChild(rightLabel);
        bottomSafe.appendChild(bottomLabel);
        leftSafe.appendChild(leftLabel);
        
        overlay.appendChild(topSafe);
        overlay.appendChild(rightSafe);
        overlay.appendChild(bottomSafe);
        overlay.appendChild(leftSafe);
        
        // Add to document
        document.body.appendChild(overlay);
        
        this.safeAreaVisualizer = overlay;
        this.hideVisualizer(); // Start hidden
    }

    createLabel(text, color) {
        const label = document.createElement('div');
        label.textContent = text;
        label.style.cssText = `
            position: absolute;
            color: black;
            font-size: 10px;
            font-weight: bold;
            padding: 2px 4px;
            background: ${color};
            border-radius: 2px;
            pointer-events: none;
            white-space: nowrap;
            z-index: 9999;
        `;
        return label;
    }

    showVisualizer() {
        if (this.safeAreaVisualizer) {
            this.safeAreaVisualizer.style.display = 'block';
            this.isActive = true;
        }
    }

    hideVisualizer() {
        if (this.safeAreaVisualizer) {
            this.safeAreaVisualizer.style.display = 'none';
            this.isActive = false;
        }
    }

    toggleVisualizer() {
        if (this.isActive) {
            this.hideVisualizer();
        } else {
            this.showVisualizer();
        }
    }

    // Method to log safe area values
    logSafeAreas() {
        console.group(' safezone Values');
        console.log('Top:', this.safeAreaValues.top);
        console.log('Right:', this.safeAreaValues.right);
        console.log('Bottom:', this.safeAreaValues.bottom);
        console.log('Left:', this.safeAreaValues.left);
        console.groupEnd();
    }

    startMonitoring() {
        // Update safe area values periodically
        setInterval(() => {
            this.updateSafeAreaValues();
        }, 1000);

        // Also update on resize and orientation change
        window.addEventListener('resize', () => {
            setTimeout(() => this.updateSafeAreaValues(), 100);
        });

        window.addEventListener('orientationchange', () => {
            setTimeout(() => this.updateSafeAreaValues(), 100);
        });

        // Toggle visualizer with key combo (Ctrl+Shift+S)
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'S') {
                e.preventDefault();
                this.toggleVisualizer();
            }
        });
    }
}

// Add CSS for safe area variables and fixes
function addIOSFixesCSS() {
    const css = `
        :root {
            --safe-area-top: env(safe-area-inset-top, 0px);
            --safe-area-right: env(safe-area-inset-right, 0px);
            --safe-area-bottom: env(safe-area-inset-bottom, 0px);
            --safe-area-left: env(safe-area-inset-left, 0px);
            --vh: 1vh;
        }
        
        body {
            padding-top: var(--safe-area-top);
            padding-right: var(--safe-area-right);
            padding-bottom: var(--safe-area-bottom);
            padding-left: var(--safe-area-left);
            height: calc(var(--vh, 1vh) * 100);
        }
        
        /* iOS-specific viewport fix */
        @supports (-webkit-touch-callout: none) {
            body {
                height: calc(var(--vh, 1vh) * 100);
            }
        }
    `;
    
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
}

// Initialize the safe area debugger when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add iOS fixes CSS first
    addIOSFixesCSS();
    
    // Initialize safe area debugger
    window.iosSafeAreaDebugger = new IOSSafeAreaDebugger();
    
    // Make it available globally
    window.IOSSafeAreaDebugger = IOSSafeAreaDebugger;
    
    // Log initial safe area values
    window.iosSafeAreaDebugger.logSafeAreas();
});

// Also export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IOSSafeAreaDebugger;
}