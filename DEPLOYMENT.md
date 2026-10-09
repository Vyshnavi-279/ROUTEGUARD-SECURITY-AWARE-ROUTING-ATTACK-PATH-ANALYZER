# RouteGuard Vercel Deployment Guide

## 🚀 Deploying to Vercel

### Prerequisites
1. Vercel account (free tier available at https://vercel.com)
2. Vercel CLI installed
3. Git repository initialized

---

## Step 1: Install Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login
```

---

## Step 2: Initialize Git Repository (if not done)

```bash
cd /Users/vyshnavi/RouteGuard_old

# Initialize git if needed
git init

# Add all files
git add .

# Commit
git commit -m "Production-ready RouteGuard deployment"
```

---

## Step 3: Deploy to Vercel

```bash
cd /Users/vyshnavi/RouteGuard_old

# Deploy (this will prompt you for project settings)
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account/team
# - Link to existing project? No
# - Project name? routeguard (or your preferred name)
# - Directory? ./ (leave as current directory)
# - Override settings? No
```

---

## Step 4: Set Environment Variables

After the first deployment, set production environment variables:

```bash
# Set SECRET_KEY (generate a strong random key)
vercel env add SECRET_KEY production

# When prompted, enter a strong secret key, e.g.:
# your-super-secret-production-key-$(openssl rand -hex 32)

# Set ENVIRONMENT
vercel env add ENVIRONMENT production
# Enter: production

# Set DEBUG
vercel env add DEBUG production
# Enter: False

# Optional: Update default passwords
vercel env add ADMIN_PASSWORD production
# Enter your strong admin password

vercel env add ANALYST_PASSWORD production
# Enter your strong analyst password

vercel env add VIEWER_PASSWORD production
# Enter your strong viewer password
```

---

## Step 5: Deploy to Production

```bash
# Deploy to production
vercel --prod

# Your application will be live at:
# https://your-project-name.vercel.app
```

---

## Step 6: Verify Deployment

1. Open the Vercel URL provided
2. Check that page loads without errors
3. Verify authentication works
4. Test notification bell
5. Test profile menu
6. Test graph visualization
7. Test all navigation

---

## Post-Deployment Configuration

### Set Custom Domain (Optional)

```bash
# Add custom domain
vercel domains add yourdomain.com

# Follow DNS instructions provided by Vercel
```

### Configure CORS for Production

After deployment, if you use a custom domain, update CORS:

1. Go to Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add `ALLOWED_ORIGINS` with your domain(s)

---

## Troubleshooting

### Issue: "Module not found" error

**Solution**: Ensure requirements.txt is in the root directory

```bash
cat requirements.txt
# Should show all Python dependencies
```

### Issue: "Path not found" for API routes

**Solution**: Check vercel.json routing configuration

```bash
cat vercel.json
# Verify /api/(.*) routes to backend/app/main.py
```

### Issue: Static files not loading

**Solution**: Verify static file routes in vercel.json

```bash
# Check that vis-network.min.js route is configured
# Check that index.html route is configured
```

### Issue: Environment variables not working

**Solution**: Redeploy after setting variables

```bash
vercel env pull
vercel --prod
```

---

## Monitoring Deployment

### View Logs

```bash
# View deployment logs
vercel logs

# View real-time logs
vercel logs --follow
```

### Check Deployment Status

```bash
# List deployments
vercel ls

# Inspect specific deployment
vercel inspect [deployment-url]
```

---

## Rollback (if needed)

```bash
# List all deployments
vercel ls

# Promote a previous deployment to production
vercel promote [deployment-url]
```

---

## Continuous Deployment (Optional)

### Connect to GitHub

1. Go to Vercel dashboard
2. Import your GitHub repository
3. Configure build settings (already set in vercel.json)
4. Enable auto-deployment on push

Now every push to main branch will auto-deploy!

---

## Security Checklist

Before going live:

- [ ] Changed SECRET_KEY from default
- [ ] Changed default passwords
- [ ] Set ENVIRONMENT=production
- [ ] Set DEBUG=False
- [ ] Configured CORS properly
- [ ] Tested all features
- [ ] Verified no console errors
- [ ] Checked API responses
- [ ] Tested authentication
- [ ] Verified graph loads

---

## Production URLs

After deployment, your application will be available at:

- **Vercel URL**: https://your-project-name.vercel.app
- **API Docs**: https://your-project-name.vercel.app/docs
- **ReDoc**: https://your-project-name.vercel.app/redoc

---

## Cost

Vercel Free Tier includes:
- ✅ Unlimited deployments
- ✅ Automatic HTTPS
- ✅ CDN
- ✅ 100GB bandwidth/month
- ✅ Serverless functions

Perfect for this application!

---

## Maintenance

### Update Deployment

```bash
# Make changes to your code
git add .
git commit -m "Update description"
git push

# Deploy
vercel --prod
```

### View Analytics

Go to Vercel dashboard to view:
- Deployment history
- Request analytics
- Error logs
- Performance metrics

---

## Support

If deployment fails:
1. Check Vercel logs: `vercel logs`
2. Verify requirements.txt exists
3. Verify vercel.json is correct
4. Check environment variables
5. Try deploying without --prod first

---

**Deployment Prepared**: October 9, 2026
**Status**: Ready for production deployment
**Platform**: Vercel
**Type**: Serverless FastAPI + Static Frontend
