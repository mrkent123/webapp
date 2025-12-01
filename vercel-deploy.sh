#!/bin/bash

# Vercel Deployment Script
# Generated on 2025-12-01 23:56:28

echo "🚀 Deploying eTax Mobile PWA to Vercel..."
echo "Repository: https://github.com/mrkent123/webapp"
echo "Token: 5INe5lvsNQ9NZToI7dFhMiVHr9wJtRwxmQWGf95kElpL9CAFFJ0DW8Zo"

# Set environment variables
export VERCEL_TOKEN="5INe5lvsNQ9NZToI7dFhMiVHr9wJtRwxmQWGf95kElpL9CAFFJ0DW8Zo"
export VERCEL_ORG_ID="team_XXXXXXXXXXXXX"  # Get this from your Vercel account
export VERCEL_PROJECT_ID="prj_XXXXXXXXXXXXX"  # Get this from your Vercel project

# Option 1: Manual deployment via Vercel CLI (if available)
if command -v vercel &> /dev/null; then
    echo "✅ Using Vercel CLI..."
    vercel login --token $VERCEL_TOKEN
    vercel deploy --prod --token $VERCEL_TOKEN --yes
else
    echo "❌ Vercel CLI not found. Please install it:"
    echo "npm install -g vercel@latest"
fi

# Option 2: Manual deployment steps
echo ""
echo "📋 MANUAL DEPLOYMENT STEPS:"
echo "1. Go to https://vercel.com/new"
echo "2. Import project from GitHub: https://github.com/mrkent123/webapp"
echo "3. Configure settings:"
echo "   - Framework Preset: Static"
echo "   - Build Command: (leave empty for static site)"
echo "   - Output Directory: ."
echo "   - Install Command: (leave empty)"
echo "4. Deploy!"
echo ""
echo "🔗 After deployment, your PWA will be available at:"
echo "   https://webapp-mrkent123.vercel.app"

# Option 3: Direct GitHub Pages (if Vercel fails)
echo ""
echo "🔄 FALLBACK: GitHub Pages"
echo "1. Go to https://github.com/mrkent123/webapp/settings/pages"
echo "2. Source: Deploy from a branch"
echo "3. Branch: master"
echo "4. Folder: / (root)"
echo "5. Your site will be available at:"
echo "   https://mrkent123.github.io/webapp"