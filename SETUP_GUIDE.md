# RockyBot Setup Guide

## Quick Start (Free Options)

### Option 1: Google Gemini (Recommended)
1. Get free API key: https://makersuite.google.com/app/apikey
2. Add to `.env`: `GOOGLE_API_KEY=your-key`
3. Select "Google Gemini" in app

### Option 2: Ollama (Local - Completely Free)
1. Install Ollama: https://ollama.ai/
2. Run: `ollama pull llama2`
3. Select "Ollama (Local)" in app

## Installation
```bash
pip install -r requirements.txt
```

## Environment Variables (.env)
```env
# Choose one or more:
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key  
GOOGLE_API_KEY=your-google-key
```

## Usage
1. Run: `streamlit run main.py`
2. Select LLM provider in sidebar
3. Select embedding provider (Hugging Face = free)
4. Add news URLs and start!

## LLM Provider Options

### 1. **Ollama (Local - FREE)**
- **Pros:** Completely free, runs locally, no API limits
- **Cons:** Requires more RAM, slower than cloud options
- **Setup:**
  1. Install Ollama from https://ollama.ai/
  2. Download a model: `ollama pull llama2`
  3. Select "Ollama (Local)" in the app

### 2. **Google Gemini (FREE tier available)**
- **Pros:** Free tier with generous limits, good performance
- **Cons:** Requires Google account and API key
- **Setup:**
  1. Go to https://makersuite.google.com/app/apikey
  2. Create a new API key
  3. Add `GOOGLE_API_KEY=your-key` to `.env`
  4. Select "Google Gemini" in the app

### 3. **Anthropic Claude (Paid)**
- **Pros:** High quality responses, good for complex tasks
- **Cons:** Requires paid API key
- **Setup:**
  1. Sign up at https://console.anthropic.com/
  2. Get your API key
  3. Add `ANTHROPIC_API_KEY=sk-ant-your-key` to `.env`
  4. Select "Anthropic Claude" in the app

### 4. **OpenAI (Paid)**
- **Pros:** Most widely used, good documentation
- **Cons:** Requires paid API key with credits
- **Setup:**
  1. Add credits to your OpenAI account
  2. Add `OPENAI_API_KEY=sk-your-key` to `.env`
  3. Select "OpenAI" in the app

## Embedding Provider Options

### 1. **Hugging Face (FREE)**
- **Pros:** Completely free, runs locally
- **Cons:** Slower than cloud options
- **Setup:** Just select "Hugging Face (Free)" in the app

### 2. **OpenAI (Paid)**
- **Pros:** Fast and high quality
- **Cons:** Requires API credits
- **Setup:** Add OpenAI API key and select "OpenAI"

## Troubleshooting

### NLTK Data Issues
If you see NLTK errors, run:
```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
```

### Ollama Issues
- Make sure Ollama is running: `ollama serve`
- Check available models: `ollama list`
- Pull a model: `ollama pull llama2`

### API Key Issues
- Check your `.env` file format
- Verify API keys are valid
- Check account credits/limits

## Cost Comparison

| Provider | Cost | Quality | Speed |
|----------|------|---------|-------|
| Ollama (Local) | FREE | Good | Slow |
| Google Gemini | FREE tier | Very Good | Fast |
| Anthropic Claude | ~$0.015/1K tokens | Excellent | Fast |
| OpenAI | ~$0.002/1K tokens | Very Good | Fast | 