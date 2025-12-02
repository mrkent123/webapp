/*
 * iOS Fixes JavaScript for iPhone Device Frame Tool
 * This script provides fixes for common iOS issues and includes auto-reload functionality
 */

// Fix for iOS 100vh bug
function setVhProperty() {
  const vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`);
}

// Initialize the vh property on load and resize
document.addEventListener('DOMContentLoaded', setVhProperty);
window.addEventListener('resize', setVhProperty);
window.addEventListener('orientationchange', function() {
  // Delay setting vh property on orientation change to ensure correct dimensions
  setTimeout(setVhProperty, 100);
});

// Auto-reload functionality via WebSocket
function setupAutoReload() {
  try {
    const ws = new WebSocket("ws://localhost:3210");
    
    ws.onopen = function(event) {
      console.log("Connected to reload server");
    };
    
    ws.onmessage = function(e) {
      if (e.data === "reload") {
        console.log("Reload triggered by file change");
        location.reload();
      }
    };
    
    ws.onerror = function(error) {
      console.error("WebSocket error:", error);
    };
    
    ws.onclose = function() {
      console.log("Disconnected from reload server");
      // Attempt to reconnect after 3 seconds
      setTimeout(setupAutoReload, 3000);
    };
  } catch (error) {
    console.error("Failed to setup WebSocket auto-reload:", error);
  }
}

// Input zoom fix - ensure all inputs have font-size >= 16px
function fixInputZoom() {
  const inputs = document.querySelectorAll('input, textarea, select');
  inputs.forEach(input => {
    const computedStyle = window.getComputedStyle(input);
    const fontSize = parseFloat(computedStyle.fontSize);
    
    if (fontSize < 16) {
      input.style.fontSize = '16px';
    }
  });
}

// Execute fixes on DOM load
document.addEventListener('DOMContentLoaded', function() {
  setVhProperty();
  fixInputZoom();
  setupAutoReload();
});

// Prevent overscroll bounce in iOS
function preventOverscroll() {
  const elements = document.querySelectorAll('body, .scroll-container');
  elements.forEach(el => {
    el.addEventListener('touchstart', function() {
      const scrollTop = this.scrollTop;
      const scrollHeight = this.scrollHeight;
      const height = this.offsetHeight;
      const maxScrollTop = scrollHeight - height;
      
      if (!maxScrollTop && scrollTop === 0) {
        this.scrollTop = 1;
      } else if (maxScrollTop === scrollTop) {
        this.scrollTop = scrollTop - 1;
      }
    });

    el.addEventListener('touchmove', function(event) {
      const scrollTop = this.scrollTop;
      const scrollHeight = this.scrollHeight;
      const height = this.offsetHeight;
      const maxScrollTop = scrollHeight - height;
      const deltaY = event.touches[0].pageY - this.touchStartY;
      
      if ((scrollTop === 0 && deltaY > 0) || (scrollTop === maxScrollTop && deltaY < 0)) {
        event.preventDefault();
      }
    });
  });
}

// Initialize overscroll prevention
document.addEventListener('DOMContentLoaded', preventOverscroll);

// Detect and handle high-DPR displays
function handleHighDprDisplays() {
  const dpr = window.devicePixelRatio || 1;
  
  if (dpr >= 3) {
    // Apply any DPR-specific fixes here
    document.body.classList.add('high-dpr');
  }
}

// Initialize DPR handling
document.addEventListener('DOMContentLoaded', handleHighDprDisplays);