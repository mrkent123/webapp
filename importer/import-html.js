#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const cheerio = require('cheerio');

async function importHtml(htmlPath, cssPath = null) {
  try {
    // Read HTML content
    const htmlContent = await fs.readFile(htmlPath, 'utf8');
    
    // Load HTML into Cheerio
    const $ = cheerio.load(htmlContent);
    
    // If CSS file is provided, read and parse it
    let cssRules = {};
    if (cssPath) {
      try {
        const cssContent = await fs.readFile(cssPath, 'utf8');
        cssRules = parseCSS(cssContent);
      } catch (err) {
        console.log(`CSS file not found or readable: ${cssPath}. Proceeding without CSS.`);
      }
    }
    
    // Parse the DOM and convert to schema
    const schema = parseDOM($, 'body', cssRules);
    
    // Write output schema
    const outputPath = path.join(__dirname, 'output-schema.json');
    await fs.writeFile(outputPath, JSON.stringify(schema, null, 2));
    
    console.log(`Schema successfully imported to: ${outputPath}`);
    return schema;
  } catch (error) {
    console.error('Error importing HTML:', error);
    throw error;
  }
}

function parseDOM($, selector, cssRules) {
  const elements = [];
  const $elements = $(selector).children();
  
  $elements.each(function() {
    const $element = $(this);
    const tagName = $element[0].name;
    
    // Skip script and style tags
    if (['script', 'style', 'link', 'meta', 'title'].includes(tagName)) {
      return;
    }
    
    // Convert HTML element to our schema format
    const element = convertToSchemaElement($element, cssRules);
    
    // Process children recursively
    const childElements = parseDOM($, this, cssRules);
    element.children = childElements;
    
    elements.push(element);
  });
  
  return elements;
}

function convertToSchemaElement($element, cssRules) {
  const tagName = $element[0].name.toLowerCase();
  const className = $element.attr('class') || '';
  const id = $element.attr('id') || '';
  
  // Determine element type based on tag
  let type = 'section'; // default
  switch (tagName) {
    case 'h1':
    case 'h2':
    case 'h3':
    case 'h4':
    case 'h5':
    case 'h6':
      type = 'heading';
      break;
    case 'p':
    case 'span':
    case 'div':
      // Check if it looks like a text element
      if (!isLikelyContainer($element)) {
        type = 'text';
      } else {
        type = 'section'; // container div
      }
      break;
    case 'img':
      type = 'image';
      break;
    case 'button':
    case 'a':
      type = 'button';
      break;
    default:
      // Check if element is likely a container
      if (isLikelyContainer($element)) {
        type = 'section';
      } else {
        type = 'text';
      }
  }
  
  // Get element properties
  const props = getElementProps($element, type, cssRules);
  
  // Generate unique ID
  const elementId = `${type}-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
  
  return {
    id: elementId,
    type: type,
    props: props,
    children: []
  };
}

function isLikelyContainer($element) {
  // Check if element has multiple children or specific container-like classes
  const children = $element.children();
  const classAttr = $element.attr('class') || '';
  
  // If it has more than a few children, likely a container
  if (children.length > 2) return true;
  
  // Check for common container classes
  const containerClasses = ['container', 'row', 'col', 'section', 'wrapper', 'box', 'card', 'panel'];
  return containerClasses.some(cls => classAttr.toLowerCase().includes(cls));
}

function getElementProps($element, type, cssRules) {
  const props = {};
  const tagName = $element[0].name.toLowerCase();
  const className = $element.attr('class') || '';
  const styleAttr = $element.attr('style') || '';
  
  // Extract inline styles
  Object.assign(props, extractInlineStyles(styleAttr));
  
  switch (type) {
    case 'heading':
      props.text = $element.text().trim() || 'Heading';
      props.fontSize = props.fontSize || '24px';
      props.fontWeight = props.fontWeight || 'bold';
      props.color = props.color || '#1f2937';
      props.margin = props.margin || '10px 0';
      break;
      
    case 'text':
      props.text = $element.text().trim() || 'Sample text content';
      props.fontSize = props.fontSize || '16px';
      props.color = props.color || '#374151';
      props.lineHeight = props.lineHeight || '1.5';
      props.margin = props.margin || '10px 0';
      break;
      
    case 'image':
      props.src = $element.attr('src') || 'https://placehold.co/300x200';
      props.alt = $element.attr('alt') || 'Imported image';
      props.width = props.width || '100%';
      props.borderRadius = props.borderRadius || '4px';
      break;
      
    case 'button':
      props.text = ($element.text().trim() || $element.attr('title') || 'Button').substring(0, 50);
      props.backgroundColor = props.backgroundColor || '#3b82f6';
      props.color = props.color || '#ffffff';
      props.padding = props.padding || '10px 20px';
      props.borderRadius = props.borderRadius || '6px';
      props.border = props.border || 'none';
      props.cursor = props.cursor || 'pointer';
      props.fontSize = props.fontSize || '16px';
      break;
      
    case 'section':
      props.padding = props.padding || '20px';
      props.margin = props.margin || '10px';
      props.backgroundColor = props.backgroundColor || '#ffffff';
      props.borderRadius = props.borderRadius || '8px';
      break;
  }
  
  // Apply CSS classes if available
  if (className) {
    Object.assign(props, extractClassStyles(className, cssRules));
  }
  
  return props;
}

function extractInlineStyles(styleString) {
  const props = {};
  if (!styleString) return props;
  
  const styles = styleString.split(';');
  styles.forEach(style => {
    const [property, value] = style.split(':');
    if (property && value) {
      const camelCaseProp = property.trim()
        .split('-')
        .map((word, index) => index === 0 ? word : word.charAt(0).toUpperCase() + word.slice(1))
        .join('');
      props[camelCaseProp] = value.trim();
    }
  });
  
  return props;
}

function extractClassStyles(className, cssRules) {
  const props = {};
  const classes = className.split(/\s+/);
  
  classes.forEach(cls => {
    const ruleName = `.${cls}`;
    if (cssRules[ruleName]) {
      Object.assign(props, cssRules[ruleName]);
    }
  });
  
  return props;
}

function parseCSS(cssString) {
  const rules = {};
  
  // Very basic CSS parser - extracts class rules
  const classRuleRegex = /\.([^{]+)\s*\{([^}]+)\}/g;
  let match;
  
  while ((match = classRuleRegex.exec(cssString)) !== null) {
    const className = match[1].trim();
    const properties = match[2].trim();
    
    // Split properties by semicolon
    const propPairs = properties.split(';').filter(p => p.trim());
    const ruleProps = {};
    
    propPairs.forEach(pair => {
      const [prop, value] = pair.split(':');
      if (prop && value) {
        const trimmedProp = prop.trim();
        const trimmedValue = value.trim();
        
        // Convert CSS property to camelCase
        const camelCaseProp = trimmedProp
          .split('-')
          .map((word, index) => index === 0 ? word : word.charAt(0).toUpperCase() + word.slice(1))
          .join('');
          
        ruleProps[camelCaseProp] = trimmedValue;
      }
    });
    
    rules[className] = ruleProps;
  }
  
  return rules;
}

// Parse command line arguments
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('Usage: node import-html.js <html-file> [--css <css-file>]');
    process.exit(1);
  }
  
  const htmlPath = args[0];
  let cssPath = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--css' && args[i + 1]) {
      cssPath = args[i + 1];
      i++;
    }
  }
  
  try {
    await importHtml(htmlPath, cssPath);
  } catch (error) {
    console.error('Import failed:', error);
    process.exit(1);
  }
}

// Run if this is the main module
if (require.main === module) {
  main();
}

module.exports = { importHtml };