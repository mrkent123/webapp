// WebSocket reload client for iPhone Device Frame Tool
// Connects to WebSocket server and reloads page when requested

class ReloadClient {
    constructor(wsUrl = 'ws://localhost:3210') {
        this.wsUrl = wsUrl;
        this.reconnectInterval = 5000; // 5 seconds
        this.maxReconnectAttempts = 10;
        this.reconnectAttempts = 0;
        this.connect();
    }

    connect() {
        try {
            this.ws = new WebSocket(this.wsUrl);
            
            this.ws.onopen = (event) => {
                console.log('Reload client connected to', this.wsUrl);
                this.reconnectAttempts = 0; // Reset on successful connection
            };
            
            this.ws.onmessage = (event) => {
                if (event.data === 'reload') {
                    console.log('Reload triggered by server');
                    this.reloadPage();
                }
            };
            
            this.ws.onerror = (error) => {
                console.error('Reload client error:', error);
            };
            
            this.ws.onclose = (event) => {
                console.log('Reload client disconnected:', event.code, event.reason);
                
                // Attempt to reconnect if we haven't exceeded max attempts
                if (this.reconnectAttempts < this.maxReconnectAttempts) {
                    this.reconnectAttempts++;
                    console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
                    setTimeout(() => this.connect(), this.reconnectInterval);
                } else {
                    console.error('Max reconnection attempts reached. Please refresh the page.');
                }
            };
        } catch (error) {
            console.error('Failed to create WebSocket connection:', error);
        }
    }

    reloadPage() {
        // Reload the current page
        window.location.reload();
    }

    // Method to manually trigger reload (for testing)
    triggerReload() {
        this.ws.send('reload');
    }
}

// Initialize the reload client when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're in an iframe (for device frame) or main window
    if (window.self === window.top) {
        // Main window - create reload client
        window.reloadClient = new ReloadClient();
    } else {
        // In iframe - check if parent has reload client
        try {
            if (window.parent && window.parent.reloadClient) {
                // We're in device frame, use parent's reload client
                console.log('Device frame detected - using parent reload client');
            } else {
                // Iframe but not in device frame - create own client
                window.reloadClient = new ReloadClient();
            }
        } catch (e) {
            // Cross-origin error - create own client
            window.reloadClient = new ReloadClient();
        }
    }
});

// Export for use in other modules if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReloadClient;
}