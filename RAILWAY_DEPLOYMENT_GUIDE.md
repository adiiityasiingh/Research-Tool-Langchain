# 🚀 Railway Deployment Guide

Complete step-by-step guide to deploy your News Research Tool to Railway.

## 📋 Prerequisites

1. **GitHub Repository** - Your code must be on GitHub
2. **Railway Account** - Sign up at [railway.app](https://railway.app)
3. **API Keys** - At least one of:
   - OpenAI API Key
   - Anthropic API Key
   - Google API Key

## 🔧 Step-by-Step Deployment

### Step 1: Prepare Your Repository

Your project structure should look like this:
```
your-project/
├── main.py              # Your Streamlit app
├── requirements.txt     # Python dependencies
├── railway.json         # Railway configuration
├── .env                 # Environment variables (local only)
└── README.md
```

### Step 2: Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Prepare for Railway deployment"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### Step 3: Install Railway CLI

```bash
# Install Railway CLI globally
npm install -g @railway/cli

# Verify installation
railway --version
```

### Step 4: Login to Railway

```bash
# Login to your Railway account
railway login
```

This will open your browser to authenticate with Railway.

### Step 5: Initialize Railway Project

```bash
# Navigate to your project directory
cd your-project-directory

# Initialize Railway project
railway init
```

This will:
- Create a new Railway project
- Link it to your current directory
- Ask you to select/create a project

### Step 6: Deploy Your App

```bash
# Deploy to Railway
railway up
```

This will:
- Build your application
- Install dependencies
- Deploy to Railway's servers
- Give you a live URL

### Step 7: Set Environment Variables

```bash
# Set your API keys
railway variables set OPENAI_API_KEY=your_openai_api_key_here
railway variables set ANTHROPIC_API_KEY=your_anthropic_api_key_here
railway variables set GOOGLE_API_KEY=your_google_api_key_here
```

### Step 8: Verify Deployment

```bash
# Check deployment status
railway status

# View logs
railway logs

# Open your app
railway open
```

## 🔍 Testing Your Deployment

1. **Visit your Railway URL** (shown after deployment)
2. **Test the interface**:
   - Select an LLM provider
   - Choose embedding provider
   - Add some news URLs
   - Process the URLs
   - Ask questions

## 🛠️ Railway Commands Reference

### Basic Commands
```bash
railway login          # Login to Railway
railway init           # Initialize project
railway up             # Deploy application
railway status         # Check deployment status
railway logs           # View application logs
railway open           # Open app in browser
```

### Environment Variables
```bash
railway variables      # List all variables
railway variables set KEY=value    # Set variable
railway variables unset KEY        # Remove variable
```

### Project Management
```bash
railway projects       # List all projects
railway link           # Link to existing project
railway unlink         # Unlink from project
```

## 🔧 Troubleshooting

### Common Issues

**"Command not found: railway"**
```bash
# Reinstall Railway CLI
npm uninstall -g @railway/cli
npm install -g @railway/cli
```

**"Build failed"**
```bash
# Check your requirements.txt
# Ensure all dependencies are listed
# Check Railway logs for specific errors
railway logs
```

**"Environment variable not found"**
```bash
# Verify variables are set
railway variables

# Set missing variables
railway variables set KEY=value
```

**"App not starting"**
```bash
# Check logs for errors
railway logs

# Verify start command in railway.json
# Ensure main.py exists and is correct
```

### Debug Commands

```bash
# View detailed logs
railway logs --follow

# Check build process
railway up --debug

# View project settings
railway status
```

## 📊 Monitoring Your App

### Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Select your project
3. View:
   - Deployment status
   - Resource usage
   - Logs
   - Environment variables

### Performance Monitoring
- **CPU Usage**: Monitor in Railway dashboard
- **Memory Usage**: Check resource consumption
- **Response Times**: Test your app regularly
- **Error Rates**: Monitor logs for issues

## 🔄 Updates and Maintenance

### Deploy Updates
```bash
# Make changes to your code
git add .
git commit -m "Update description"
git push origin main

# Deploy to Railway
railway up
```

### Rollback Deployment
```bash
# View deployment history
railway status

# Rollback to previous version
railway rollback
```

## 💰 Cost Management

### Railway Pricing
- **Free Tier**: $5 credit monthly
- **Pay-as-you-go**: $0.000463/second after free tier
- **Predictable**: No surprise charges

### Cost Optimization
1. **Monitor usage** in Railway dashboard
2. **Use smaller models** for faster responses
3. **Implement caching** to reduce API calls
4. **Optimize code** to reduce resource usage

## 🔐 Security Best Practices

1. **Never commit API keys** to Git
2. **Use environment variables** for all secrets
3. **Regularly rotate** API keys
4. **Monitor access logs** for suspicious activity

## 🎯 Pro Tips

1. **Use Railway's persistent storage** for ChromaDB
2. **Set up custom domains** for professional appearance
3. **Enable auto-deploy** from GitHub
4. **Monitor logs regularly** for issues
5. **Test locally first** before deploying

## 🆘 Getting Help

- **Railway Documentation**: [railway.app/docs](https://railway.app/docs)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: Create an issue in your repository

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Railway CLI installed
- [ ] Logged into Railway
- [ ] Project initialized
- [ ] App deployed successfully
- [ ] Environment variables set
- [ ] App tested and working
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up

---

**Your app is now live on Railway! 🚀**

Visit your Railway URL to start using your News Research Tool. 