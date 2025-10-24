# Deployment Guide

This guide covers various deployment options for the Natural Language to SQL Accelerator.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Considerations](#production-considerations)

## Local Development

### Quick Start

See [QUICKSTART.md](QUICKSTART.md) for the fastest way to get started.

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Configure environment:**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys
```

2. **Start services:**
```bash
docker-compose up -d
```

3. **Check status:**
```bash
docker-compose ps
docker-compose logs -f
```

4. **Stop services:**
```bash
docker-compose down
```

### Building Individual Images

**Backend:**
```bash
docker build -f Dockerfile.backend -t nl-to-sql-backend .
docker run -p 8000:8000 --env-file backend/.env nl-to-sql-backend
```

**Frontend:**
```bash
docker build -f Dockerfile.frontend -t nl-to-sql-frontend .
docker run -p 3000:80 nl-to-sql-frontend
```

## Cloud Deployment

### AWS (Elastic Beanstalk)

1. **Install EB CLI:**
```bash
pip install awsebcli
```

2. **Initialize:**
```bash
eb init -p python-3.11 nl-to-sql-accelerator
```

3. **Create environment:**
```bash
eb create nl-to-sql-env
```

4. **Set environment variables:**
```bash
eb setenv LLM_PROVIDER=openai OPENAI_API_KEY=your_key
```

5. **Deploy:**
```bash
eb deploy
```

### Heroku

**Backend:**
```bash
heroku create nl-to-sql-backend
heroku config:set OPENAI_API_KEY=your_key
git subtree push --prefix backend heroku main
```

**Frontend:**
```bash
heroku create nl-to-sql-frontend
heroku buildpacks:set mars/create-react-app
git subtree push --prefix frontend heroku main
```

### DigitalOcean App Platform

1. **Create app** from GitHub repository
2. **Configure environment variables** in the dashboard
3. **Set build commands:**
   - Backend: `pip install -r backend/requirements.txt`
   - Frontend: `npm install && npm run build`
4. **Set run commands:**
   - Backend: `uvicorn app.main:app --host 0.0.0.0 --port ${PORT}`
   - Frontend: Serve from `build/` directory

### Google Cloud Platform (Cloud Run)

**Backend:**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/nl-to-sql-backend
gcloud run deploy --image gcr.io/PROJECT_ID/nl-to-sql-backend \
  --platform managed \
  --set-env-vars OPENAI_API_KEY=your_key
```

**Frontend:**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/nl-to-sql-frontend
gcloud run deploy --image gcr.io/PROJECT_ID/nl-to-sql-frontend \
  --platform managed
```

### Azure

**Using Azure Container Instances:**
```bash
az container create \
  --resource-group myResourceGroup \
  --name nl-to-sql-backend \
  --image myregistry.azurecr.io/nl-to-sql-backend \
  --dns-name-label nl-to-sql \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=your_key
```

### Kubernetes

1. **Create deployment manifest:**

```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nl-to-sql-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nl-to-sql-backend
  template:
    metadata:
      labels:
        app: nl-to-sql-backend
    spec:
      containers:
      - name: backend
        image: nl-to-sql-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-key
---
apiVersion: v1
kind: Service
metadata:
  name: nl-to-sql-backend
spec:
  selector:
    app: nl-to-sql-backend
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

2. **Apply configuration:**
```bash
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
```

## Production Considerations

### Security

1. **API Keys:**
   - Store in environment variables, not code
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault)
   - Rotate keys regularly

2. **HTTPS:**
   - Use SSL/TLS certificates
   - Force HTTPS redirects
   - Use Let's Encrypt for free certificates

3. **CORS:**
   - Restrict to specific domains
   - Don't use wildcard (*) in production

4. **Rate Limiting:**
   - Implement rate limiting per IP
   - Use Redis for distributed rate limiting
   - Configure in backend/.env

5. **Input Validation:**
   - Already implemented in backend
   - Don't allow dangerous SQL operations
   - Sanitize all user inputs

### Performance

1. **Caching:**
   - Enable query caching (Redis recommended)
   - Set appropriate TTL values
   - Cache schema information

2. **Database:**
   - Use connection pooling
   - Implement read replicas for heavy loads
   - Consider PostgreSQL/MySQL for production

3. **Frontend:**
   - Enable gzip compression
   - Use CDN for static assets
   - Implement lazy loading

4. **Monitoring:**
   - Set up logging (CloudWatch, Datadog)
   - Monitor API response times
   - Track error rates

### Scalability

1. **Load Balancing:**
   - Use Application Load Balancer (AWS)
   - Horizontal scaling with multiple instances
   - Session management with Redis

2. **Auto-scaling:**
   - Configure based on CPU/memory
   - Set min/max instance counts
   - Use container orchestration

3. **Database:**
   - Connection pooling
   - Read replicas
   - Consider sharding for very large datasets

### Backup and Recovery

1. **Database Backups:**
   - Automated daily backups
   - Store in multiple regions
   - Test recovery procedures

2. **Configuration Backups:**
   - Version control all configs
   - Document environment variables
   - Keep deployment playbooks

### Monitoring and Logging

1. **Application Monitoring:**
```python
# Add to backend/app/main.py
from loguru import logger

logger.add("logs/app.log", rotation="500 MB")
```

2. **Health Checks:**
   - Already implemented at `/health`
   - Monitor regularly
   - Set up alerts

3. **Metrics:**
   - Response times
   - Error rates
   - Query execution times
   - API usage

### Environment Variables

**Required:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=random_secret_key
```

**Optional:**
```env
MAX_QUERY_RESULTS=1000
QUERY_TIMEOUT=30
ENABLE_QUERY_CACHING=True
CACHE_TTL=300
LOG_LEVEL=INFO
```

### Database Migration

**From SQLite to PostgreSQL:**

1. **Export data:**
```bash
sqlite3 chinook.db .dump > chinook.sql
```

2. **Convert to PostgreSQL:**
```bash
# Install pgloader
pgloader chinook.db postgresql://user:pass@host/db
```

3. **Update configuration:**
```env
DATABASE_URL=postgresql://user:pass@host/db
```

### CI/CD Pipeline

**GitHub Actions Example:**

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Your deployment commands
```

### Cost Optimization

1. **LLM API Usage:**
   - Enable caching to reduce API calls
   - Use cheaper models for simple queries
   - Implement request batching

2. **Infrastructure:**
   - Use spot/preemptible instances
   - Shut down dev environments when not in use
   - Right-size your instances

3. **Storage:**
   - Compress large result sets
   - Clean up old query history
   - Use object storage for backups

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
```

**Docker build fails:**
```bash
# Clean Docker cache
docker system prune -a
# Rebuild
docker-compose build --no-cache
```

**Database connection fails:**
```bash
# Check database URL
echo $DATABASE_URL
# Test connection
python -c "from backend.app.database import test_connection; print(test_connection())"
```

## Support

For deployment issues:
- Check logs: `docker-compose logs -f`
- Review error messages
- Consult provider documentation
- Open GitHub issue

## Next Steps

After deployment:
1. ✅ Test all endpoints
2. ✅ Configure monitoring
3. ✅ Set up alerts
4. ✅ Document custom configurations
5. ✅ Train users
6. ✅ Plan maintenance windows

---

**Remember:** Always test in a staging environment before deploying to production!
