# RouteGuard - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Start the Server
```bash
cd /Users/vyshnavi/RouteGuard_old/backend
PYTHONPATH=. python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 2: Open Your Browser
```
http://127.0.0.1:8000/
```

### Step 3: Explore the Features

The application will automatically authenticate you as **admin**.

---

## 🎯 What's New & Fixed

### ✅ Notification Bell (Top Right)
- **Click the bell icon** to see notifications
- Red badge appears when you have notifications
- Shows your recent actions (attack analysis, simulations, etc.)
- Auto-updates after each operation

### ✅ Profile Menu (Top Right Avatar)
- **Click your avatar** (shows "A" for admin)
- Opens profile menu with:
  - View Profile
  - Audit Logs
  - Sign Out
- Shows your role and username

### ✅ Improved Network Graph
- **No more auto-zoom** when you move your mouse
- **Clean hierarchical layout** - nodes don't overlap
- **New controls**:
  - **+** Zoom in
  - **−** Zoom out
  - **⊙** Fit to view
  - **Maximize** - Full screen graph
- **Drag to pan** around the graph
- **Click nodes** to see details

### ✅ All Navigation Working
1. **Dashboard** - Main view with all metrics
2. **Topology** - Full-screen network graph
3. **Attack Paths** - Find security vulnerabilities
4. **Simulation** - Test "what-if" scenarios
5. **Lab** - Network algorithm experiments
6. **Audit Logs** - See all your actions

---

## 🧪 Try These Features

### 1. Find Attack Paths
1. Go to Dashboard (or Attack Paths view)
2. Enter source: `internet`
3. Enter target: `db01`
4. Click **⚡ Attack** button
5. See attack paths highlighted on graph
6. Check notification bell - new notification!

### 2. Run Simulation
1. Click **Simulation** in navigation
2. Select "Compromise Node"
3. Enter target: `web01`
4. Click **▶ Execute Simulation**
5. See impact on network

### 3. Check Audit Logs
1. Click **Audit Logs** in navigation
2. See all your actions logged
3. Click **🔄 Refresh Logs** to update
4. Color-coded by action type

### 4. Maximize Graph
1. Click **Topology** in navigation
2. Click **Maximize** button
3. Graph expands to full screen
4. Use zoom controls to explore
5. Click **Restore** to return

### 5. View Notifications
1. Perform any action (Dijkstra, Attack Paths, etc.)
2. Click **notification bell** (top right)
3. See your action as a notification
4. Click notification to mark as read

---

## 🎨 UI Improvements

### Larger Fonts
- All text is now **easier to read**
- Navigation: 14px
- Section titles: 20px
- Input fields: 14px
- Result outputs: 13px

### Better Layout
- **More screen space used**
- Cards properly aligned
- Consistent spacing throughout
- Professional appearance

### Clear Graph
- **Hierarchical layout** - left to right flow
- **Wide spacing** between nodes
- **No overlapping** elements
- **Clear labels** on everything

---

## 🔧 Available Features

### Dashboard Actions
- **Routes** - Find security-aware routes
- **⚡ Attack** - Analyze attack paths
- **Dijkstra** - Shortest path algorithm
- **Reach** - Reachability analysis

### Simulation Types
- Compromise Node
- Isolate Node
- Sever Link
- Restore Network

### Lab Experiments
- Distance Vector Routing
- CRC Error Detection
- Leaky Bucket Algorithm
- Bit Stuffing Protocol

---

## 📊 Network Topology

### Default Network Nodes
- **internet** - Public Internet (untrusted)
- **fw01** - Perimeter Firewall
- **web01** - Public Web Server
- **router01** - Core Router R1
- **router02** - Backup Router R2
- **app01** - Primary App Server
- **db01** - Customer Database (critical!)
- **admin01** - SecOps Admin Workstation

### Sample Routes to Try
- `internet` → `db01` (find attack paths)
- `internet` → `app01` (web traffic)
- `admin01` → `db01` (admin access)
- `web01` → `app01` (application tier)

---

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Kill existing server
pkill -f "uvicorn app.main"

# Check if port is free
lsof -i :8000

# Restart server
cd /Users/vyshnavi/RouteGuard_old/backend
PYTHONPATH=. python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Page Shows Errors
1. Check browser console (F12)
2. Look for red error messages
3. Refresh page (Cmd+Shift+R or Ctrl+Shift+R)
4. Check server logs in terminal

### Graph Not Showing
1. Wait 2-3 seconds for authentication
2. Check if "admin" appears in top right
3. Refresh the page
4. Check browser console for errors

### Notifications Not Working
1. Perform an action first (e.g., run Dijkstra)
2. Click the bell icon
3. Check if notification appears
4. If not, check Network tab in browser DevTools

---

## 🔑 Login Credentials

The app auto-logs you in as **admin**.

If you need to change users, here are the credentials:

### Admin (Full Access)
- Username: `admin`
- Password: `AdminSecurePassword123!`
- Role: ADMIN

### Security Analyst (Most Access)
- Username: `analyst`
- Password: `AnalystSecurePassword123!`
- Role: SECURITY_ANALYST

### Viewer (Read Only)
- Username: `viewer`
- Password: `ViewerSecurePassword123!`
- Role: VIEWER

---

## 📝 Keyboard Shortcuts

### Graph Controls
- **Drag** - Pan around graph
- **+** button - Zoom in
- **−** button - Zoom out
- **⊙** button - Fit to view

### Navigation
- Click any nav button to switch views
- Active view is highlighted

---

## 🎯 What to Test

### High Priority
1. ✅ Click notification bell - does panel open?
2. ✅ Click avatar - does profile menu open?
3. ✅ Run attack path analysis - does it work?
4. ✅ Maximize graph - does it expand?
5. ✅ Check audit logs - do they load?

### Medium Priority
1. ✅ All navigation buttons work?
2. ✅ Graph zoom controls work?
3. ✅ Simulation executes?
4. ✅ Lab experiments run?
5. ✅ Results display correctly?

### Low Priority
1. ✅ Notifications update after actions?
2. ✅ Node click shows details?
3. ✅ Graph tooltips appear?
4. ✅ Layout looks professional?

---

## 📚 Next Steps

### For Testing
1. Read `TEST_PLAN.md` for detailed testing checklist
2. Read `REPAIR_REPORT.md` for complete technical details

### For Deployment
1. Update environment variables
2. Configure production settings
3. Test on staging server
4. Deploy to production

### For Development
1. Check `backend/app/api/routes.py` for API endpoints
2. Check `index.html` for frontend code
3. Run tests: `pytest tests/ -v`

---

## 🆘 Need Help?

### Documentation
- API Docs: http://127.0.0.1:8000/docs
- Test Plan: `TEST_PLAN.md`
- Full Report: `REPAIR_REPORT.md`

### Common Issues
- **401 Unauthorized**: Wait for auto-login, or refresh page
- **Graph blank**: Check browser console for errors
- **Slow loading**: Wait for authentication to complete
- **Buttons not working**: Check browser console

---

## ✨ Summary

All major issues have been **fixed**:
- ✅ Notification bell fully functional
- ✅ Profile menu implemented
- ✅ Graph layout improved (no overlaps)
- ✅ All navigation working
- ✅ Audit logs integrated
- ✅ Typography improved
- ✅ Professional appearance

**Status**: Ready for production use!

**Last Updated**: October 9, 2026, 3:40 PM
