#  DEPLOYMENT GUIDE - Render + Vercel

##  Files Created Successfully

All deployment configuration files are ready:

### Backend (Render)
-  `backend/Dockerfile` - Docker container config
-  `render.yaml` - Render service blueprint  
-  `.dockerignore` - Build optimization

### Frontend (Vercel)
-  `vercel.json` - Vercel deployment config
-  `frontend/.env.production` - Production environment
-  `frontend/.env.example` - Environment template

---

##  STEP-BY-STEP DEPLOYMENT

### STEP 1: Push to GitHub

```powershell
cd D:\HackWave
git add .
git commit -m "Add deployment configuration"
git push origin main
```

### STEP 2: Deploy Backend on Render

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com/
   - Sign in with GitHub

2. **Create New Blueprint**
   - Click: **New**  **Blueprint**
   - Connect your GitHub repository: **HackWave**
   - Render will auto-detect `render.yaml`

3. **Set Environment Variables**
   Click on your service and add these:
   ```
   GEMINI_API_KEY = <your-gemini-api-key>
   SUPABASE_URL = https://<your-project>.supabase.co
   SUPABASE_ANON_KEY = <your-supabase-anon-key>
   ```

4. **Deploy**
   - Click **Apply**
   - Wait for deployment (3-5 minutes)
   - Copy your URL: `https://cultural-context-analyzer-api.onrender.com`

5. **Test Health Endpoint**
   ```powershell
   curl https://your-app.onrender.com/health
   ```
   Should return: `{"status":"healthy",...}`

### STEP 3: Deploy Frontend on Vercel

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Sign in with GitHub

2. **Import Project**
   - Click: **Add New**  **Project**
   - Import your GitHub repository: **HackWave**
   - Vercel will auto-detect `vercel.json`

3. **Configure Project**
   - **Root Directory**: Leave as default (config handles subdirectory)
   - Vercel reads paths from `vercel.json` automatically

4. **Set Environment Variable**
   - Add environment variable:
   ```
   VITE_API_URL = https://your-render-app.onrender.com
   ```
   (Use the URL from Step 2)

5. **Deploy**
   - Click **Deploy**
   - Wait for build (2-3 minutes)
   - Copy your URL: `https://your-app.vercel.app`

### STEP 4: Update CORS (CRITICAL!)

After both deployments, update backend CORS:

1. **Edit `backend/main.py`** (line ~47):
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "https://your-app.vercel.app",  # Your Vercel URL
           "http://localhost:5173"  # Keep for local dev
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Commit and Push**:
   ```powershell
   cd D:\HackWave
   git add cultural-context-analyzer/backend/main.py
   git commit -m "Update CORS for production"
   git push origin main
   ```

   Render will automatically redeploy!

---

##  TESTING YOUR DEPLOYMENT

### Test Backend
```powershell
# Health check
curl https://your-app.onrender.com/health

# Root endpoint
curl https://your-app.onrender.com/
```

### Test Frontend
1. Visit: `https://your-app.vercel.app`
2. Open browser console (F12)
3. Register a new user
4. Try analyzing text
5. Check for CORS errors

---

##  CONFIGURATION DETAILS

### render.yaml
- **Docker Context**: `./cultural-context-analyzer/backend`
- **Dockerfile Path**: `./cultural-context-analyzer/backend/Dockerfile`
- **Health Check**: `/health` endpoint
- **Plan**: Free tier

### vercel.json
- **Build Command**: `cd cultural-context-analyzer/frontend && npm install && npm run build`
- **Output Directory**: `cultural-context-analyzer/frontend/dist`
- **Framework**: Vite (auto-detected)
- **Rewrites**: SPA routing enabled

### Dockerfile
- **Base Image**: `python:3.11-slim`
- **Port**: Uses `$PORT` env variable (Render requirement)
- **Command**: `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`

---

##  TROUBLESHOOTING

### Backend won't start on Render
**Error**: Missing environment variables
**Solution**: Set `GEMINI_API_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY` in Render dashboard

### Frontend can't reach backend
**Error**: CORS policy blocked
**Solution**: Update CORS in `backend/main.py` with your Vercel URL and redeploy

### Build fails on Render
**Error**: Cannot find Dockerfile
**Solution**: Check `render.yaml` paths match your repo structure

### Build fails on Vercel
**Error**: Build command failed
**Solution**: Verify paths in `vercel.json` are correct

### 502 Bad Gateway on Render
**Error**: Service crashed
**Solution**: Check Render logs for Python errors, verify all dependencies in requirements.txt

---

##  MONITORING

### Render Logs
- Dashboard  Your Service  **Logs** tab
- Real-time logs of your backend

### Vercel Logs  
- Dashboard  Your Project  Latest Deployment  **Logs**
- Build logs and runtime logs

---

##  REDEPLOYMENT

### Backend (Render)
Automatic on git push to main branch. Or manual:
- Render Dashboard  Your Service  **Manual Deploy**

### Frontend (Vercel)
Automatic on git push to main branch. Or manual:
```powershell
cd D:\HackWave
vercel --prod
```

---

##  DEPLOYMENT CHECKLIST

- [ ] All deployment files created
- [ ] Code pushed to GitHub
- [ ] Backend deployed on Render
- [ ] Backend environment variables set
- [ ] Backend health check passes
- [ ] Backend URL noted
- [ ] Frontend deployed on Vercel
- [ ] Frontend `VITE_API_URL` set
- [ ] CORS updated with Vercel URL
- [ ] CORS changes pushed and redeployed
- [ ] Full app tested in production
- [ ] No console errors in browser

---

##  SUCCESS!

Your app is now live:
- **Frontend**: https://your-app.vercel.app
- **Backend API**: https://your-app.onrender.com
- **Health Check**: https://your-app.onrender.com/health

Share your app with the world! 

---

##  NEED HELP?

### Check These Files
- `render.yaml` - Backend deployment config
- `vercel.json` - Frontend deployment config
- `backend/Dockerfile` - Docker container setup
- `.dockerignore` - Build optimization

### Common Commands
```powershell
# View deployment files
cd D:\HackWave\cultural-context-analyzer
dir render.yaml,vercel.json
dir backend\Dockerfile
dir frontend\.env.production

# Push updates
git add .
git commit -m "Update deployment config"
git push origin main
```

### Resources
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Your Repo: https://github.com/AbhiramOgirala/HackWave

Good luck! 
