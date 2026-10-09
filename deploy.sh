#!/bin/bash
# RouteGuard Vercel Deployment Script
# Run this script to deploy your application to Vercel

set -e  # Exit on any error

echo "🚀 RouteGuard Deployment to Vercel"
echo "===================================="
echo ""

# Navigate to project directory
cd /Users/vyshnavi/RouteGuard_old

echo "✅ Current directory: $(pwd)"
echo ""

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Initializing..."
    git init
    git branch -M main
fi

echo "📦 Staging deployment files..."
git add vercel.json
git add requirements.txt
git add .env.example
git add .gitignore
git add index.html
git add vis-network.min.js
git add backend/app/api/routes.py
git add DEPLOYMENT.md
git add QUICK_START.md
git add TEST_PLAN.md
git add REPAIR_REPORT.md
git add VERIFICATION.md
git add data/
git add backend/

echo ""
echo "📝 Committing changes..."
git commit -m "Production deployment: Fixed UI, added notifications, improved graph" || echo "Nothing to commit"

echo ""
echo "🔍 Checking Vercel CLI..."
if command -v vercel &> /dev/null; then
    VERCEL_CMD="vercel"
elif command -v npx &> /dev/null; then
    VERCEL_CMD="npx vercel"
else
    echo "❌ Vercel CLI not found. Please install:"
    echo "   npm install -g vercel"
    echo "   OR use npx (requires Node.js)"
    exit 1
fi

echo "✅ Using: $VERCEL_CMD"
echo ""

echo "🎯 Starting deployment..."
echo ""
echo "You will be prompted for:"
echo "  1. Login (if not already logged in)"
echo "  2. Set up and deploy? → Yes"
echo "  3. Which scope? → Select your account"
echo "  4. Link to existing project? → No"
echo "  5. Project name? → routeguard (or your choice)"
echo "  6. Directory? → ./ (current directory)"
echo "  7. Override settings? → No"
echo ""

read -p "Press ENTER to continue with deployment..."

# Deploy to Vercel
$VERCEL_CMD

echo ""
echo "✅ Initial deployment complete!"
echo ""
echo "⚙️  Now setting environment variables..."
echo ""

# Set environment variables
echo "Setting SECRET_KEY..."
SECRET_KEY=$(openssl rand -hex 32)
echo $SECRET_KEY | $VERCEL_CMD env add SECRET_KEY production --force

echo "Setting ENVIRONMENT..."
echo "production" | $VERCEL_CMD env add ENVIRONMENT production --force

echo "Setting DEBUG..."
echo "False" | $VERCEL_CMD env add DEBUG production --force

echo ""
echo "✅ Environment variables set!"
echo ""

echo "🚀 Deploying to production..."
$VERCEL_CMD --prod

echo ""
echo "===================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "===================================="
echo ""
echo "Your application is now live!"
echo ""
echo "Next steps:"
echo "1. Open your Vercel URL (shown above)"
echo "2. Test the application"
echo "3. Check browser console for errors"
echo "4. Verify all features work"
echo ""
echo "To view logs:"
echo "  $VERCEL_CMD logs"
echo ""
echo "To view in dashboard:"
echo "  $VERCEL_CMD dashboard"
echo ""
echo "Documentation:"
echo "  - QUICK_START.md - How to use the application"
echo "  - DEPLOYMENT.md - Deployment details"
echo "  - TEST_PLAN.md - Testing checklist"
echo ""
