# Manual Deployment Checklist - Run These Commands

## 🚀 Deploy RouteGuard to Vercel - Step by Step

### Option 1: Automated Deployment (Recommended)

```bash
# Navigate to project
cd /Users/vyshnavi/RouteGuard_old

# Make script executable
chmod +x deploy.sh

# Run deployment script
./deploy.sh
```

The script will:
- ✅ Stage all files
- ✅ Commit changes
- ✅ Deploy to Vercel
- ✅ Set environment variables
- ✅ Deploy to production

---

### Option 2: Manual Deployment (If script fails)

#### Step 1: Prepare Files
```bash
cd /Users/vyshnavi/RouteGuard_old

# Stage deployment files
git add vercel.json requirements.txt .env.example .gitignore
git add index.html vis-network.min.js
git add backend/ data/
git add *.md

# Commit
git commit -m "Production-ready deployment with UI fixes"
```

#### Step 2: Deploy with Vercel
```bash
# Deploy (first time)
npx vercel

# Follow prompts:
# - Login with your Vercel account
# - Set up and deploy? → Yes
# - Which scope? → Your account
# - Link to existing project? → No
# - Project name? → routeguard
# - Directory? → ./ (just press Enter)
# - Override settings? → No
```

#### Step 3: Set Environment Variables
```bash
# Generate and set SECRET_KEY
SECRET_KEY=$(openssl rand -hex 32)
echo $SECRET_KEY | npx vercel env add SECRET_KEY production

# Set ENVIRONMENT
echo "production" | npx vercel env add ENVIRONMENT production

# Set DEBUG
echo "False" | npx vercel env add DEBUG production
```

#### Step 4: Deploy to Production
```bash
npx vercel --prod
```

---

## ✅ After Deployment

### 1. Get Your URL
After running `npx vercel --prod`, you'll see:
```
✅ Production: https://routeguard-xxx.vercel.app [copied to clipboard]
```

### 2. Test the Application

Open the URL and verify:
- [ ] Page loads without errors (F12 console)
- [ ] "admin" appears in top right (after 2-3 seconds)
- [ ] Network graph displays
- [ ] Click notification bell → panel opens
- [ ] Click avatar → profile menu opens
- [ ] Navigation buttons work
- [ ] Graph zoom controls work
- [ ] Graph maximize works

### 3. Check API Endpoints

```bash
# Replace YOUR_URL with your Vercel URL
export URL="https://routeguard-xxx.vercel.app"

# Test authentication
curl -X POST $URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"AdminSecurePassword123!"}' | jq

# Should return: {"access_token": "...", "token_type": "bearer", "role": "ADMIN"}
```

### 4. Monitor Logs

```bash
# View deployment logs
npx vercel logs

# View real-time logs
npx vercel logs --follow
```

---

## 🔧 Troubleshooting

### Issue: "Not logged in"
```bash
npx vercel login
```

### Issue: "Build failed"
```bash
# Check logs
npx vercel logs

# Common fix: Ensure requirements.txt exists
ls -la requirements.txt

# Redeploy
npx vercel --prod
```

### Issue: "Environment variables not working"
```bash
# Pull environment variables
npx vercel env pull

# List environment variables
npx vercel env ls

# Re-add if needed
echo "production" | npx vercel env add ENVIRONMENT production --force
```

### Issue: "API routes return 404"
```bash
# Verify vercel.json is correct
cat vercel.json

# Should have routes for /api/(.*)
```

### Issue: "Static files not loading"
```bash
# Verify files exist
ls -la index.html vis-network.min.js

# Redeploy
npx vercel --prod
```

---

## 📊 Vercel Dashboard

Access your deployment dashboard:
```bash
npx vercel dashboard
```

Or visit: https://vercel.com/dashboard

From dashboard you can:
- View deployment status
- Check logs
- Manage environment variables
- View analytics
- Set up custom domain
- Configure CORS

---

## 🔐 Security Post-Deployment

### Change Default Passwords (Recommended)

```bash
# Set custom admin password
npx vercel env add ADMIN_PASSWORD production
# When prompted, enter: YourStrongPassword123!

# Set custom analyst password
npx vercel env add ANALYST_PASSWORD production
# When prompted, enter: YourAnalystPassword123!

# Set custom viewer password
npx vercel env add VIEWER_PASSWORD production
# When prompted, enter: YourViewerPassword123!

# Redeploy for changes to take effect
npx vercel --prod
```

### Configure CORS (If using custom domain)

```bash
# Add allowed origins
npx vercel env add ALLOWED_ORIGINS production
# When prompted, enter: https://yourdomain.com,https://www.yourdomain.com

# Redeploy
npx vercel --prod
```

---

## 🌐 Custom Domain (Optional)

### Add Domain
```bash
npx vercel domains add yourdomain.com
```

Follow DNS instructions provided by Vercel.

---

## 📱 Share Your Application

After successful deployment, share:

**Application URL**: https://routeguard-xxx.vercel.app
**API Documentation**: https://routeguard-xxx.vercel.app/docs
**ReDoc**: https://routeguard-xxx.vercel.app/redoc

**Default Login**:
- Username: `admin`
- Password: `AdminSecurePassword123!` (or your custom password)

---

## 🔄 Update Deployment

When you make changes:

```bash
cd /Users/vyshnavi/RouteGuard_old

# Make your changes to code
# ...

# Commit changes
git add .
git commit -m "Description of changes"

# Deploy updated version
npx vercel --prod
```

---

## 📞 Support

### View Deployment Info
```bash
npx vercel ls
npx vercel inspect
```

### Get Help
```bash
npx vercel help
```

### Rollback if needed
```bash
# List all deployments
npx vercel ls

# Promote previous deployment
npx vercel promote [previous-deployment-url]
```

---

## ✅ Deployment Success Checklist

After deployment, verify:
- [ ] Application loads at Vercel URL
- [ ] No browser console errors
- [ ] Authentication works
- [ ] Notification bell functional
- [ ] Profile menu functional
- [ ] Graph renders correctly
- [ ] All navigation works
- [ ] API endpoints respond (200 OK)
- [ ] Audit logs load
- [ ] No 404 or 500 errors

If all checked, **deployment is successful!** 🎉

---

## 📝 Important URLs

Save these for reference:

- **Application**: https://routeguard-xxx.vercel.app
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Documentation**: https://vercel.com/docs
- **Support**: https://vercel.com/support

---

**Ready to deploy?** Run the automated script:
```bash
cd /Users/vyshnavi/RouteGuard_old
chmod +x deploy.sh
./deploy.sh
```

Or follow the manual steps above.

**Good luck with your deployment!** 🚀
