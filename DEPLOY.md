# Deployment Guide

## Architecture
- **Frontend**: GitHub Pages (free, auto-deploys on every push)
- **Backend**: Render.com (free tier, Python/FastAPI)
- **Database**: SQLite (free, file-based, included in repo)

---

## Step 1: Deploy Backend to Render (5 minutes)

1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo: `Prince11-dev/careerforge-ai`
4. Configure:
   - **Name**: `careerforge-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`
5. Add Environment Variables:
   - `DATABASE_URL`: `sqlite:///./careerforge.db`
   - `SECRET_KEY`: (generate at https://randomkeygen.com/)
   - `MOCK_AI_MODE`: `true`
   - `FRONTEND_URL`: `https://prince11-dev.github.io/careerforge-ai`
6. Click **"Create Web Service"**
7. Wait for deploy (2-3 minutes). You'll get a URL like:
   `https://careerforge-api.onrender.com`

---

## Step 2: Enable GitHub Pages (2 minutes)

1. Go to your repo on GitHub: `github.com/Prince11-dev/careerforge-ai`
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Build and deployment**:
   - **Source**: `GitHub Actions`
4. That's it! The workflow file is already in `.github/workflows/deploy.yml`

---

## Step 3: Update API URL (if Render URL is different)

If your Render URL is different from `careerforge-api.onrender.com`:

1. Edit `.github/workflows/deploy.yml`
2. Change this line:
   ```yaml
   VITE_API_URL: https://careerforge-api.onrender.com/api
   ```
   to your actual Render URL.
3. Push the change:
   ```bash
   git add .
   git commit -m "Update API URL"
   git push
   ```

---

## Step 4: Seed Demo Data on Render

After the backend deploys, seed the demo data:

1. Go to Render dashboard → your service → **Shell**
2. Run:
   ```bash
   python seed.py
   ```

---

## Your Live URLs

| Service | URL |
|---------|-----|
| Frontend | `https://prince11-dev.github.io/careerforge-ai` |
| Backend API | `https://careerforge-api.onrender.com` |
| API Docs | `https://careerforge-api.onrender.com/docs` |

---

## Important Notes

- **Render free tier**: Spins down after 15 min of inactivity. First request after idle takes ~1 min to wake up.
- **GitHub Pages**: Frontend updates automatically on every push to `main`.
- **Database**: SQLite is file-based and persists on Render's disk (free tier has 512MB).
- **CORS**: Already configured in `app/main.py` to allow your GitHub Pages URL.

---

## Troubleshooting

**Frontend shows "Login failed"?**
→ Backend is likely sleeping. Wait 1 minute and retry.

**CORS errors in browser console?**
→ Check `FRONTEND_URL` env var on Render matches your GitHub Pages URL exactly.

**404 on refresh?**
→ GitHub Pages SPA routing is handled. If not, add a `404.html` that redirects to `index.html`.
