# Direct Vercel Deployment Guide

## Step 1: Push to GitHub

1. **Create a new repository on GitHub**:
   - Go to github.com and click "New repository"
   - Name it `tds-virtual-ta`
   - Set it to Public
   - Don't initialize with README (we already have one)

2. **Download your Replit code**:
   - In Replit, click the three dots (⋯) menu
   - Select "Download as zip"
   - Extract to your computer

3. **Push to GitHub**:
   ```bash
   cd path/to/extracted/folder
   git init
   git add .
   git commit -m "Initial commit - TDS Virtual TA"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/tds-virtual-ta.git
   git push -u origin main
   ```

## Step 2: Deploy to Vercel

1. **Go to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Sign in with GitHub

2. **Import Project**:
   - Click "New Project"
   - Find your `tds-virtual-ta` repository
   - Click "Import"

3. **Configure Deployment**:
   - Vercel will auto-detect the Python project
   - No changes needed - the `vercel.json` file is already configured
   - Click "Deploy"

4. **Add Environment Variables** (Optional but recommended):
   - Go to Project Settings → Environment Variables
   - Add these variables:
     ```
     OPENAI_API_KEY = your_openai_api_key_here
     SESSION_SECRET = any_random_string_here
     ```

## Step 3: Verify Deployment

Your app will be live at: `https://tds-virtual-ta.vercel.app` (or your custom domain)

Test these endpoints:
- `/` - Web interface
- `/api/health` - Health check
- `/api/` - Submit questions (POST)

## Features Ready for Production

✅ **Web Interface**: Clean HTML interface for testing
✅ **API Endpoints**: RESTful API for integration
✅ **Database**: SQLite with automatic table creation
✅ **AI Integration**: OpenAI GPT-4 support
✅ **Error Handling**: Graceful fallbacks when AI unavailable
✅ **Security**: Proper environment variable handling
✅ **Scalability**: Serverless deployment ready

## Custom Domain (Optional)

1. In Vercel dashboard, go to your project
2. Click "Domains" tab
3. Add your domain
4. Follow DNS setup instructions

Your TDS Virtual Teaching Assistant is now live and ready for production use!