# FULL PACK - Web Builder Enhancement Suite

## MODULE A - E2E Test System (Puppeteer + Screenshot diff)

### Files Created:
- `tests/e2e/run-tests.js`
- `tests/e2e/viewports.json`
- `tests/e2e/screenshot-baseline/` (folder)
- `tests/e2e/screenshot-latest/` (folder)
- `tests/e2e/screenshot-diff/` (folder)
- `tests/e2e/report.json`

### Features:
- Loads http://127.0.0.1:5173/
- Captures screenshots for 12 devices:
  * iPhone SE, iPhone 12, iPhone 14 Pro, iPhone 14 Pro Max
  * Android 360×800, 412×915
  * Tablet 768, Desktop 1024, 1280, 1440
- Compares baseline vs latest screenshots using pixelmatch
- Generates diff images highlighting pixel differences
- Creates JSON report with results

### How to Run E2E Tests:
1. Ensure the dev server is running: `npm run dev`
2. Run the tests: `node tests/e2e/run-tests.js`
3. Check results in `tests/e2e/report.json`
4. View screenshots in the respective folders:
   - Baseline: `tests/e2e/screenshot-baseline/`
   - Latest: `tests/e2e/screenshot-latest/`
   - Diffs: `tests/e2e/screenshot-diff/`

## MODULE B - HTML/CSS/PWA Export Compiler

### Files Created:
- `compiler/build-schema-to-html.js`
- `compiler/build-pwa.js`
- `compiler/run-export.js`
- `export/input.json`
- `export/dist/`

### Features:
- Converts builder schema to complete HTML/CSS application
- Generates PWA assets (manifest.json, service-worker.js)
- Creates responsive CSS with mobile-first approach
- Auto-scales mobile width (393px) to responsive 100%
- Generates all necessary assets for PWA installation

### How to Run Compiler:
1. Prepare your schema JSON in `export/input.json`
2. Run the export command:
   `node compiler/run-export.js --schema ./export/input.json --out ./export/dist`
3. Find your generated PWA-ready bundle in `export/dist/`
4. The bundle includes:
   - index.html
   - styles.css
   - manifest.json
   - service-worker.js
   - placeholder icons

## MODULE D - Auto Clone UI from HTML/CSS 

### Files Created:
- `importer/import-html.js`
- `importer/output-schema.json`

### Features:
- Parses raw HTML + CSS and converts to builder schema
- Detects sections, headings, text, images, buttons
- Converts CSS units to responsive rules
- Normalizes fonts, colors, and spacing
- Automatically wraps components into responsive sections

### How to Import HTML→Schema:
1. Run the import command:
   `node importer/import-html.js source.html --css source.css`
2. The generated schema will be saved to `importer/output-schema.json`
3. Import this schema directly into the Web Builder

### Requirements:
- Ensure dev server is running on http://127.0.0.1:5173 for E2E tests
- Node.js and npm must be available
- No additional global dependencies required