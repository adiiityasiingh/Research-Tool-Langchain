# 🚀 Vercel Deployment Guide

This guide will walk you through deploying your News Research Tool to Vercel.

## 📋 Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
3. **API Keys** - You'll need at least one of:
   - OpenAI API Key
   - Anthropic API Key  
   - Google API Key

## 🔧 Step-by-Step Deployment

### Step 1: Prepare Your Repository

Your project structure should look like this:
```
your-project/
├── api/
│   ├── main.py          # FastAPI application
│   └── requirements.txt # Python dependencies
├── vercel.json          # Vercel configuration
├── .env                 # Environment variables (local only)
└── README.md
```

### Step 2: Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for Vercel deployment"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### Step 3: Connect to Vercel

1. **Go to [vercel.com](https://vercel.com)** and sign in
2. **Click "New Project"**
3. **Import your GitHub repository**
4. **Select the repository** you just pushed

### Step 4: Configure Environment Variables

In the Vercel dashboard, go to your project settings and add these environment variables:

```bash
# Required for OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Optional - for Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional - for Google Gemini  
GOOGLE_API_KEY=your_google_api_key_here
```

### Step 5: Deploy

1. **Click "Deploy"** in the Vercel dashboard
2. **Wait for build** (usually 2-5 minutes)
3. **Your app will be live** at `https://your-project-name.vercel.app`

## 🔍 Testing Your Deployment

1. **Visit your Vercel URL**
2. **Test the interface**:
   - Select an LLM provider
   - Choose embedding provider
   - Add some news URLs
   - Process the URLs
   - Ask questions

## ⚠️ Important Limitations

### Vercel Serverless Limitations

1. **No Persistent Storage**: ChromaDB files won't persist between requests
2. **Cold Starts**: First request may be slow
3. **Memory Limits**: 1024MB RAM limit on free tier
4. **Timeout**: 10-second timeout on free tier

### Workarounds

1. **Use External Vector Database**: Consider Pinecone, Weaviate, or Supabase
2. **Optimize Model Loading**: Use smaller models
3. **Handle Timeouts**: Implement proper error handling

## 🛠️ Alternative Deployment Options

### For Better Performance, Consider:

1. **Railway** - Better for Python apps with persistent storage
2. **Render** - Good free tier with persistent storage
3. **Heroku** - Reliable but paid service
4. **DigitalOcean App Platform** - Good performance

## 🔧 Troubleshooting

### Common Issues

**"Module not found" errors**
- Check that all dependencies are in `api/requirements.txt`
- Ensure `vercel.json` points to the correct file

**"Environment variable not found"**
- Verify environment variables are set in Vercel dashboard
- Check variable names match your code

**"Timeout" errors**
- Reduce model complexity
- Use faster LLM providers
- Implement caching

**"Memory exceeded" errors**
- Use smaller models
- Optimize imports
- Consider paid Vercel plan

### Debug Commands

```bash
# Test locally
cd api
pip install -r requirements.txt
python main.py

# Check Vercel logs
vercel logs your-project-name
```

## 📊 Monitoring

1. **Vercel Dashboard** - Monitor deployments and performance
2. **Function Logs** - Check for errors in real-time
3. **Analytics** - Track usage and performance

## 🔄 Updates

To update your deployment:

```bash
git add .
git commit -m "Update description"
git push origin main
```

Vercel will automatically redeploy on push to main branch.

## 💡 Pro Tips

1. **Use Environment Variables** for all API keys
2. **Test Locally First** before deploying
3. **Monitor Usage** to avoid rate limits
4. **Consider Caching** for better performance
5. **Use Smaller Models** for faster responses

## 🆘 Need Help?

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **GitHub Issues**: Create an issue in your repository

---

**Happy Deploying! 🚀** 