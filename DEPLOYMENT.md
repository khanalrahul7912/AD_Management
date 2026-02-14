# Deployment Guide for AD Management System

## Production Deployment

### Using Gunicorn (Recommended for Linux)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create a Gunicorn configuration file** (`gunicorn_config.py`):
   ```python
   bind = "0.0.0.0:8000"
   workers = 4
   worker_class = "sync"
   timeout = 120
   keepalive = 5
   errorlog = "-"
   loglevel = "info"
   accesslog = "-"
   access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -c gunicorn_config.py app:app
   ```

### Using Systemd (Linux Service)

1. **Create systemd service file** (`/etc/systemd/system/ad-management.service`):
   ```ini
   [Unit]
   Description=AD Management Flask Application
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/AD_Management
   Environment="PATH=/var/www/AD_Management/venv/bin"
   EnvironmentFile=/var/www/AD_Management/.env
   ExecStart=/var/www/AD_Management/venv/bin/gunicorn -c gunicorn_config.py app:app

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and start the service**
   ```bash
   sudo systemctl enable ad-management
   sudo systemctl start ad-management
   sudo systemctl status ad-management
   ```

### Nginx Reverse Proxy

1. **Install Nginx**
   ```bash
   sudo apt-get install nginx
   ```

2. **Create Nginx configuration** (`/etc/nginx/sites-available/ad-management`):
   ```nginx
   server {
       listen 80;
       server_name ad-management.yourdomain.com;

       # Redirect to HTTPS
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl http2;
       server_name ad-management.yourdomain.com;

       ssl_certificate /etc/ssl/certs/your-cert.crt;
       ssl_certificate_key /etc/ssl/private/your-key.key;

       # SSL configuration
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_prefer_server_ciphers on;
       ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           
           # Increase timeouts for AD operations
           proxy_connect_timeout 300s;
           proxy_send_timeout 300s;
           proxy_read_timeout 300s;
       }

       location /static {
           alias /var/www/AD_Management/app/static;
           expires 30d;
       }
   }
   ```

3. **Enable the site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/ad-management /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### Docker Deployment

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   # Install dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt gunicorn

   # Copy application
   COPY . .

   # Create non-root user
   RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
   USER appuser

   EXPOSE 8000

   CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "--timeout", "120", "app:app"]
   ```

2. **Create docker-compose.yml**:
   ```yaml
   version: '3.8'

   services:
     web:
       build: .
       ports:
         - "8000:8000"
       env_file:
         - .env
       restart: unless-stopped
       volumes:
         - ./flask_session:/app/flask_session
   ```

3. **Build and run**:
   ```bash
   docker-compose up -d
   ```

## Security Checklist

- [ ] Set strong `SECRET_KEY` in production
- [ ] Enable SSL/TLS for LDAP connections (`AD_USE_SSL=True`)
- [ ] Use HTTPS for web access (configure SSL certificate)
- [ ] Restrict file permissions on `.env` file (`chmod 600 .env`)
- [ ] Use a dedicated AD service account with minimal permissions
- [ ] Enable firewall to restrict access to authorized IPs
- [ ] Regular backup of configuration files
- [ ] Monitor application logs
- [ ] Keep dependencies updated (`pip list --outdated`)
- [ ] Use environment-specific configuration files

## Performance Tuning

### Session Storage
For production with multiple workers, use Redis for session storage:

1. **Install Redis and Python client**:
   ```bash
   sudo apt-get install redis-server
   pip install redis
   ```

2. **Update `.env`**:
   ```env
   SESSION_TYPE=redis
   SESSION_REDIS=redis://localhost:6379
   ```

### LDAP Connection Pooling
The ldap3 library handles connection pooling automatically, but ensure:
- Use persistent connections when possible
- Set appropriate timeout values
- Monitor connection count

## Monitoring

### Application Logs
Configure logging in production:

```python
# Add to config.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    handler = RotatingFileHandler('ad_management.log', maxBytes=10240000, backupCount=10)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
```

### Health Check Endpoint
Add a health check for monitoring:

```python
# Add to app/main.py
@main_bp.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

## Backup and Recovery

### Configuration Backup
```bash
# Backup .env file
cp .env .env.backup

# Backup with timestamp
cp .env .env.backup.$(date +%Y%m%d)
```

### Application State
- Session data is stored in `flask_session/` directory
- Backup this directory if using filesystem sessions
- For Redis sessions, configure Redis persistence

## Troubleshooting Production Issues

### Application won't start
- Check logs: `journalctl -u ad-management -f`
- Verify environment variables are loaded
- Check file permissions
- Verify Python dependencies installed

### Slow performance
- Increase Gunicorn workers
- Use Redis for session storage
- Enable LDAP SSL for better security/performance
- Check AD server connectivity and latency

### Memory issues
- Reduce number of Gunicorn workers
- Monitor with: `ps aux | grep gunicorn`
- Check for connection leaks in AD operations

## Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin main

# Install updated dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl restart ad-management
```

### Updating Dependencies
```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all packages (use with caution)
pip freeze | cut -d= -f1 | xargs pip install --upgrade
```

## Load Balancing

For high availability, deploy multiple instances behind a load balancer:

### HAProxy Configuration
```haproxy
frontend ad_management
    bind *:80
    mode http
    default_backend ad_management_servers

backend ad_management_servers
    mode http
    balance roundrobin
    option httpchk GET /health
    server app1 10.0.0.1:8000 check
    server app2 10.0.0.2:8000 check
    server app3 10.0.0.3:8000 check
```

## Additional Resources

- [Flask Deployment Options](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [ldap3 Documentation](https://ldap3.readthedocs.io/)
