const fs = require('fs').promises;
const path = require('path');

async function buildSchemaToHtml(schema, outputDir) {
  try {
    // Create output directory if it doesn't exist
    await fs.mkdir(outputDir, { recursive: true });
    
    // Generate HTML content
    const htmlContent = generateHTML(schema);
    
    // Write index.html
    const indexPath = path.join(outputDir, 'index.html');
    await fs.writeFile(indexPath, htmlContent);
    
    // Generate CSS content
    const cssContent = generateCSS();
    
    // Write styles.css
    const cssPath = path.join(outputDir, 'styles.css');
    await fs.writeFile(cssPath, cssContent);
    
    console.log(`HTML and CSS generated successfully in ${outputDir}`);
    return { htmlPath: indexPath, cssPath: cssPath };
  } catch (error) {
    console.error('Error building schema to HTML:', error);
    throw error;
  }
}

function generateHTML(schema) {
  let html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Generated Web App</title>
  <link rel="stylesheet" href="styles.css">
  <link rel="manifest" href="manifest.json">
</head>
<body>
  <div class="app-container">
`;

  // Process the schema to generate HTML components
  schema.forEach(element => {
    html += processElement(element, 0);
  });

  html += `
  </div>
  <script>
    // Service worker registration
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('service-worker.js')
          .then(function(registration) {
            console.log('ServiceWorker registration successful');
          })
          .catch(function(err) {
            console.log('ServiceWorker registration failed');
          });
      });
    }
  </script>
</body>
</html>`;

  return html;
}

function processElement(element, depth) {
  const indent = '  '.repeat(depth + 2);
  let elementHTML = '';
  
  switch (element.type) {
    case 'section':
      elementHTML += `${indent}<section class="section" style="`;
      if (element.props) {
        Object.entries(element.props).forEach(([key, value]) => {
          if (typeof value === 'string' || typeof value === 'number') {
            // Convert camelCase to kebab-case for CSS properties
            const cssProperty = key.replace(/([A-Z])/g, '-$1').toLowerCase();
            elementHTML += `${cssProperty}:${value};`;
          }
        });
      }
      elementHTML += `">`;
      
      if (element.children && element.children.length > 0) {
        elementHTML += '\n';
        element.children.forEach(child => {
          elementHTML += processElement(child, depth + 1);
        });
        elementHTML += `${indent}</section>`;
      } else {
        elementHTML += `${indent}</section>`;
      }
      break;
      
    case 'heading':
      elementHTML += `${indent}<h2 class="heading" style="`;
      if (element.props) {
        Object.entries(element.props).forEach(([key, value]) => {
          if (typeof value === 'string' || typeof value === 'number') {
            const cssProperty = key.replace(/([A-Z])/g, '-$1').toLowerCase();
            elementHTML += `${cssProperty}:${value};`;
          }
        });
      }
      elementHTML += `">${element.props?.text || 'Heading'}</h2>`;
      break;
      
    case 'text':
      elementHTML += `${indent}<p class="text" style="`;
      if (element.props) {
        Object.entries(element.props).forEach(([key, value]) => {
          if (typeof value === 'string' || typeof value === 'number') {
            const cssProperty = key.replace(/([A-Z])/g, '-$1').toLowerCase();
            elementHTML += `${cssProperty}:${value};`;
          }
        });
      }
      elementHTML += `">${element.props?.text || 'Sample text content'}</p>`;
      break;
      
    case 'image':
      elementHTML += `${indent}<div class="image-container"><img class="image" src="${element.props?.src || 'https://placehold.co/300x200'}" alt="${element.props?.alt || 'Placeholder image'}" style="`;
      if (element.props) {
        Object.entries(element.props).forEach(([key, value]) => {
          if (typeof value === 'string' || typeof value === 'number') {
            const cssProperty = key.replace(/([A-Z])/g, '-$1').toLowerCase();
            elementHTML += `${cssProperty}:${value};`;
          }
        });
      }
      elementHTML += `"></div>`;
      break;
      
    case 'button':
      elementHTML += `${indent}<button class="button" style="`;
      if (element.props) {
        Object.entries(element.props).forEach(([key, value]) => {
          if (typeof value === 'string' || typeof value === 'number') {
            const cssProperty = key.replace(/([A-Z])/g, '-$1').toLowerCase();
            elementHTML += `${cssProperty}:${value};`;
          }
        });
      }
      elementHTML += `">${element.props?.text || 'Button'}</button>`;
      break;
      
    default:
      elementHTML += `${indent}<div class="unknown" style="color: #999; font-style: italic;">Unknown element type: ${element.type}</div>`;
  }
  
  if (element.type !== 'section' || (element.children && element.children.length === 0)) {
    elementHTML += '\n';
  }
  
  return elementHTML;
}

function generateCSS() {
  return `/* Generated Styles - Tailwind-like Responsive Framework */
  
/* Base styles */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #333;
}

.app-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Section styles */
.section {
  width: 100%;
  margin: 1rem 0;
  padding: 1.5rem;
  border-radius: 0.5rem;
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}

/* Heading styles */
.heading {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0.5rem 0;
  color: #1f2937;
}

/* Text styles */
.text {
  font-size: 1rem;
  margin: 0.5rem 0;
  color: #4b5563;
}

/* Image styles */
.image-container {
  text-align: center;
  margin: 1rem 0;
}

.image {
  max-width: 100%;
  height: auto;
  border-radius: 0.25rem;
}

/* Button styles */
.button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
  text-decoration: none;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  margin: 0.25rem;
}

/* Responsive styles */
@media (max-width: 640px) {
  /* Mobile styles */
  .app-container {
    padding: 0 0.5rem;
  }
  
  .section {
    padding: 1rem;
    margin: 0.5rem 0;
  }
  
  .heading {
    font-size: 1.25rem;
  }
  
  /* Auto scale mobile width 393 → responsive 100% */
  body {
    font-size: calc(16px * (100vw / 393));
  }
}

@media (min-width: 640px) and (max-width: 768px) {
  /* Tablet styles */
  .section {
    padding: 1.25rem;
  }
}

@media (min-width: 1024px) {
  /* Desktop styles */
  .app-container {
    padding: 0 1.5rem;
  }
  
  .heading {
    font-size: 1.75rem;
  }
}

/* Utility classes */
.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

.m-1 { margin: 0.25rem; }
.m-2 { margin: 0.5rem; }
.m-3 { margin: 0.75rem; }
.m-4 { margin: 1rem; }
.m-5 { margin: 1.25rem; }
.m-6 { margin: 1.5rem; }

.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 0.75rem; }
.p-4 { padding: 1rem; }
.p-5 { padding: 1.25rem; }
.p-6 { padding: 1.5rem; }

.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.flex { display: flex; }
.inline-flex { display: inline-flex; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }

.w-full { width: 100%; }
.h-full { height: 100%; }

.hidden { display: none; }

/* Focus styles for accessibility */
.button:focus,
input:focus,
textarea:focus,
select:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Reduce motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
`;
}

module.exports = { buildSchemaToHtml };