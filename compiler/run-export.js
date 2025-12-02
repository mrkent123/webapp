#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const { buildSchemaToHtml } = require('./build-schema-to-html');
const { buildPWA } = require('./build-pwa');

async function runExport() {
  // Parse command line arguments
  const args = process.argv.slice(2);
  let schemaPath = './export/input.json';
  let outputPath = './export/dist';
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--schema' && args[i + 1]) {
      schemaPath = args[i + 1];
      i++;
    } else if (args[i] === '--out' && args[i + 1]) {
      outputPath = args[i + 1];
      i++;
    }
  }
  
  try {
    console.log('Starting export process...');
    console.log(`Schema path: ${schemaPath}`);
    console.log(`Output path: ${outputPath}`);
    
    // Read the schema
    const schemaContent = await fs.readFile(schemaPath, 'utf8');
    const schema = JSON.parse(schemaContent);
    
    // Create output directory
    await fs.mkdir(outputPath, { recursive: true });
    
    // Build HTML
    await buildSchemaToHtml(schema, outputPath);
    
    // Build PWA
    await buildPWA(outputPath);
    
    console.log(`\nExport completed successfully!`);
    console.log(`Generated files are available in: ${path.resolve(outputPath)}`);
    
  } catch (error) {
    console.error('Export failed:', error);
    process.exit(1);
  }
}

// Run the export if this file is executed directly
if (require.main === module) {
  runExport();
}

module.exports = { runExport };