# 🚀 Deployment Guide

## Deploy to Streamlit Cloud (Recommended)

Streamlit Cloud is free and perfect for Streamlit apps!

### Prerequisites
- GitHub repository with your code
- Streamlit Cloud account (free)

### Steps

1. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

2. **Click "New app"**

3. **Configure your app:**
   - Repository: `yourusername/ai-study-assistant`
   - Branch: `main`
   - Main file path: `app.py`

4. **Add secrets (API keys):**
   Click "Advanced settings" → "Secrets"
   
   Add your secrets in TOML format:
   ```toml
   OPENAI_API_KEY = "your-actual-key"
   HUGGING_FACE_TOKEN = "your-token"
   ```

5. **Deploy!**
   Click "Deploy" and wait 2-3 minutes

6. **Share your link:**
   You'll get a URL like: `https://yourusername-ai-study-assistant.streamlit.app`

### Update Your Deployed App

```bash
git add .
git commit -m "Update: Description of changes"
git push
```

Your app will automatically redeploy!

---

## Deploy to Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Setup Files

Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

Create `runtime.txt`:
```
python-3.9.16
```

### Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create ai-study-assistant

# Set environment variables
heroku config:set OPENAI_API_KEY="your-key"
heroku config:set HUGGING_FACE_TOKEN="your-token"

# Deploy
git push heroku main

# Open app
heroku open
```

---

## Deploy to Google Cloud Run

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

### Deploy

```bash
# Build and deploy
gcloud run deploy ai-study-assistant \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Set environment variables
gcloud run services update ai-study-assistant \
  --update-env-vars OPENAI_API_KEY=your-key,HUGGING_FACE_TOKEN=your-token
```

---

## Deploy to AWS EC2

### Launch EC2 Instance

1. Choose Ubuntu Server 22.04 LTS
2. Instance type: t2.medium (recommended)
3. Configure security group (allow ports 22, 80, 8501)

### Setup on EC2

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Clone your repository
git clone https://github.com/yourusername/ai-study-assistant.git
cd ai-study-assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
# Add your API keys, save and exit

# Run with screen (keeps running after disconnect)
screen -S streamlit
streamlit run app.py --server.port 8501

# Detach: Ctrl+A, then D
# Reattach: screen -r streamlit
```

### Optional: Setup as System Service

Create `/etc/systemd/system/streamlit.service`:

```ini
[Unit]
Description=Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-study-assistant
Environment="PATH=/home/ubuntu/ai-study-assistant/venv/bin"
ExecStart=/home/ubuntu/ai-study-assistant/venv/bin/streamlit run app.py

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable streamlit
sudo systemctl start streamlit
```

---

## Deploy to DigitalOcean App Platform

### Via GUI

1. Go to [DigitalOcean Apps](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository
4. Select branch: `main`
5. Add environment variables:
   - `OPENAI_API_KEY`
   - `HUGGING_FACE_TOKEN`
6. Deploy!

### Via CLI

```bash
# Install doctl
# Configure with your token

# Create app
doctl apps create --spec .do/app.yaml

# Update app
doctl apps update YOUR_APP_ID --spec .do/app.yaml
```

Create `.do/app.yaml`:
```yaml
name: ai-study-assistant
services:
- name: web
  github:
    repo: yourusername/ai-study-assistant
    branch: main
  run_command: streamlit run app.py
  envs:
  - key: OPENAI_API_KEY
    value: ${OPENAI_API_KEY}
  - key: HUGGING_FACE_TOKEN
    value: ${HUGGING_FACE_TOKEN}
```

---

## Performance Optimization

### Caching

Add to your app.py:

```python
@st.cache_data
def extract_text_from_pdf(pdf_file):
    # Your existing code
    pass

@st.cache_resource
def load_qa_model():
    return pipeline("question-answering", 
                   model="distilbert-base-cased-distilled-squad")
```

### Reduce Dependencies

For faster deployment, consider:
- Using smaller transformer models
- Lazy loading heavy libraries
- Docker multi-stage builds

---

## Monitoring and Analytics

### Add Google Analytics

Add to your Streamlit app:

```python
# Add this to your main() function
st.components.v1.html("""
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'YOUR_GA_ID');
    </script>
""", height=0)
```

### Error Tracking

Use Sentry:

```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

---

## Cost Estimates

### Free Tiers
- **Streamlit Cloud**: Free for public apps
- **Heroku**: $0-7/month (free tier available)
- **Google Cloud Run**: ~$0-5/month (generous free tier)

### Paid Options
- **AWS EC2**: ~$10-30/month (t2.medium)
- **DigitalOcean**: ~$12/month (Basic Droplet)

### API Costs
- **OpenAI GPT-4**: ~$0.03 per 1K tokens
- **Hugging Face**: Free for public models

---

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
lsof -ti:8501 | xargs kill -9
streamlit run app.py
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**Out of memory:**
- Use smaller models
- Limit text chunk sizes
- Increase instance size

**Slow loading:**
- Implement caching
- Use lighter models
- Consider CDN for static assets

---

## Maintenance Checklist

- [ ] Regular dependency updates
- [ ] Monitor API usage and costs
- [ ] Check error logs weekly
- [ ] Update models when available
- [ ] Backup configuration
- [ ] Test after major updates
- [ ] Monitor user feedback

---

## Need Help?

- Streamlit Docs: https://docs.streamlit.io
- Community Forum: https://discuss.streamlit.io
- GitHub Issues: Your repo issues page

Happy deploying! 🚀