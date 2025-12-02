// DPI and Device Debugging Tool
// Provides detailed device information for debugging iOS rendering issues

class DPIDebugger {
    constructor() {
        this.deviceInfo = this.getDeviceInfo();
        this.displayDebugInfo();
        this.startMonitoring();
    }

    getDeviceInfo() {
        return {
            screenWidth: screen.width,
            screenHeight: screen.height,
            windowInnerWidth: window.innerWidth,
            windowInnerHeight: window.innerHeight,
            devicePixelRatio: window.devicePixelRatio,
            viewportScale: this.getViewportScale(),
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            isIOS: this.isIOS(),
            isMobile: this.isMobile(),
            isSafari: this.isSafari(),
            safeAreaInsets: this.getSafeAreaInsets(),
            orientation: this.getOrientation()
        };
    }

    getViewportScale() {
        return Math.round((window.outerWidth / window.innerWidth) * 100) / 100;
    }

    isIOS() {
        return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    }

    isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }

    isSafari() {
        return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
    }

    getSafeAreaInsets() {
        // Get safe area values from CSS custom properties (if set via CSS)
        const style = getComputedStyle(document.documentElement);
        return {
            top: style.getPropertyValue('--safe-area-top') || '0px',
            right: style.getPropertyValue('--safe-area-right') || '0px',
            bottom: style.getPropertyValue('--safe-area-bottom') || '0px',
            left: style.getPropertyValue('--safe-area-left') || '0px',
        };
    }

    getOrientation() {
        return window.innerWidth > window.innerHeight ? 'landscape' : 'portrait';
    }

    displayDebugInfo() {
        // Create a floating debug panel
        this.debugPanel = document.createElement('div');
        this.debugPanel.id = 'dpi-debug-panel';
        this.debugPanel.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 9999;
            background: rgba(0, 0, 0, 0.8);
            color: #fff;
            padding: 10px;
            font-size: 10px;
            font-family: monospace;
            border-radius: 5px;
            max-width: 300px;
            max-height: 80vh;
            overflow-y: auto;
            text-align: left;
        `;
        
        // Update the debug info
        this.updateDebugInfo();
        
        // Toggle panel with double-tap or key combination
        let tapCount = 0;
        document.addEventListener('click', () => {
            tapCount++;
            if (tapCount === 2) {
                this.toggleDebugPanel();
                tapCount = 0;
            }
            setTimeout(() => tapCount = 0, 300);
        }, true);
        
        // Also allow keyboard toggle (Ctrl+Shift+D)
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'D') {
                e.preventDefault();
                this.toggleDebugPanel();
            }
        });
    }

    updateDebugInfo() {
        this.deviceInfo = this.getDeviceInfo();
        
        const infoHTML = `
            <div><strong>DPI Debug Info</strong></div>
            <div>Screen: ${this.deviceInfo.screenWidth}×${this.deviceInfo.screenHeight}</div>
            <div>Viewport: ${this.deviceInfo.windowInnerWidth}×${this.deviceInfo.windowInnerHeight}</div>
            <div>DPR: ${this.deviceInfo.devicePixelRatio}</div>
            <div>View Scale: ${this.deviceInfo.viewportScale}</div>
            <div>Orientation: ${this.deviceInfo.orientation}</div>
            <div>Safe Area: ${this.deviceInfo.safeAreaInsets.top} ${this.deviceInfo.safeAreaInsets.right} ${this.deviceInfo.safeAreaInsets.bottom} ${this.deviceInfo.safeAreaInsets.left}</div>
            <div>Mobile: ${this.deviceInfo.isMobile}</div>
            <div>iOS: ${this.deviceInfo.isIOS}</div>
            <div>Safari: ${this.deviceInfo.isSafari}</div>
            <div>DIM: ${window.screen.width * window.devicePixelRatio}×${window.screen.height * window.devicePixelRatio}</div>
        `;
        
        this.debugPanel.innerHTML = infoHTML;
    }

    toggleDebugPanel() {
        if (this.debugPanel.style.display === 'none' || !document.body.contains(this.debugPanel)) {
            if (!document.body.contains(this.debugPanel)) {
                document.body.appendChild(this.debugPanel);
            }
            this.debugPanel.style.display = 'block';
        } else {
            this.debugPanel.style.display = 'none';
        }
    }

    startMonitoring() {
        // Update info periodically and on resize/orientation changes
        window.addEventListener('resize', () => {
            setTimeout(() => this.updateDebugInfo(), 100);
        });

        window.addEventListener('orientationchange', () => {
            setTimeout(() => this.updateDebugInfo(), 100);
        });

        // Update every 5 seconds in case of dynamic changes
        setInterval(() => {
            this.updateDebugInfo();
        }, 5000);
    }

    // Method to log device info to console
    logDeviceInfo() {
        console.group('📱 Device Information');
        console.log('Screen dimensions:', `${this.deviceInfo.screenWidth}×${this.deviceInfo.screenHeight}`);
        console.log('Viewport dimensions:', `${this.deviceInfo.windowInnerWidth}×${this.deviceInfo.windowInnerHeight}`);
        console.log('Device Pixel Ratio:', this.deviceInfo.devicePixelRatio);
        console.log('Viewport Scale:', this.deviceInfo.viewportScale);
        console.log('Orientation:', this.deviceInfo.orientation);
        console.log('Is Mobile:', this.deviceInfo.isMobile);
        console.log('Is iOS:', this.deviceInfo.isIOS);
        console.log('Is Safari:', this.deviceInfo.isSafari);
        console.log('Safe Area Insets:', this.deviceInfo.safeAreaInsets);
        console.log('User Agent:', this.deviceInfo.userAgent);
        console.groupEnd();
    }
}

// Initialize the DPI debugger when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.dpiDebugger = new DPIDebugger();
    
    // Make it available globally for console access
    window.DPIDebugger = DPIDebugger;
    
    // Log initial device info
    window.dpiDebugger.logDeviceInfo();
});

// Also export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DPIDebugger;
}