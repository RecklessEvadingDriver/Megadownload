# Deploying Mega Downloader to Heroku

This guide explains how to deploy the Mega Downloader web interface to Heroku with automatic file cleanup.

## Features for Heroku Deployment

✅ **Automatic Cleanup** - Files are automatically deleted after download
✅ **Background Cleanup** - Old downloads (>1 hour) are automatically removed
✅ **Ephemeral Storage** - Optimized for Heroku's temporary filesystem
✅ **Buildpack Support** - Uses custom buildpack for megatools
✅ **Production Ready** - Uses Gunicorn WSGI server

## Prerequisites

1. **Heroku Account** - Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI** - Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git** - Ensure git is installed

## Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

### 2. Create a New Heroku App

```bash
# Create app (Heroku will assign a name)
heroku create

# Or create with a specific name
heroku create your-app-name
```

### 3. Add Buildpacks

Heroku needs custom buildpacks for megatools:

```bash
# Add APT buildpack (for installing system packages)
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt

# Add Python buildpack
heroku buildpacks:add --index 2 heroku/python
```

### 4. Create Aptfile for Megatools

Create a file named `Aptfile` in the root directory:

```bash
echo "megatools" > Aptfile
```

This tells Heroku to install megatools.

### 5. Set Environment Variables (Optional)

```bash
# Set secret key for production
heroku config:set SECRET_KEY="your-random-secret-key-here"

# Set to production mode
heroku config:set FLASK_ENV=production
```

### 6. Deploy to Heroku

```bash
# Add all files to git
git add .

# Commit changes
git commit -m "Deploy to Heroku with auto-cleanup"

# Push to Heroku
git push heroku main
```

If you're on a different branch:
```bash
git push heroku your-branch:main
```

### 7. Open Your App

```bash
heroku open
```

## Automatic File Cleanup

The app includes three levels of automatic cleanup:

### 1. Immediate Cleanup (ZIP Downloads)
When users download all files as ZIP:
- Files are automatically deleted 2 seconds after the ZIP is sent
- Both the download folder and ZIP file are removed
- Status is cleared from memory

### 2. Background Cleanup Task
A background thread runs every 5 minutes and:
- Removes download folders older than 1 hour
- Removes ZIP files older than 10 minutes
- Clears stale status entries

### 3. Manual Cleanup Endpoint
Users can manually trigger cleanup via the `/cleanup/<download_id>` endpoint

## Monitoring and Logs

View real-time logs:
```bash
heroku logs --tail
```

View specific number of log lines:
```bash
heroku logs -n 200
```

Check dyno status:
```bash
heroku ps
```

## Configuration Files

### Procfile
Tells Heroku how to run the app:
```
web: gunicorn web_app:app
```

### runtime.txt
Specifies Python version:
```
python-3.12.3
```

### Aptfile
Lists system packages to install:
```
megatools
```

### requirements.txt
Python dependencies:
```
Flask>=3.0.0
gunicorn>=21.2.0
```

## Scaling

Heroku free tier includes:
- 550-1000 dyno hours per month
- Sleeps after 30 minutes of inactivity
- Automatic wake-up on first request

To prevent sleeping (requires paid dyno):
```bash
heroku ps:scale web=1
```

## Troubleshooting

### Issue: App crashes on startup

**Check logs:**
```bash
heroku logs --tail
```

**Common causes:**
- Megatools not installed (check Aptfile and buildpack)
- Missing dependencies (check requirements.txt)
- Port binding issues (app should use `PORT` env var)

### Issue: Downloads fail

**Verify megatools installation:**
```bash
heroku run bash
> which megadl
> megadl --version
```

### Issue: Files not cleaned up

**Check cleanup task:**
- Look for cleanup messages in logs: `heroku logs | grep Cleaning`
- Verify background thread is running
- Check folder permissions

### Issue: Out of disk space

**Solution:**
- Cleanup task should prevent this
- Manually restart dyno: `heroku restart`
- Consider smaller download limits

## Environment Variables

Set custom configuration:

```bash
# Maximum file age before cleanup (seconds)
heroku config:set CLEANUP_AGE=3600

# Cleanup check interval (seconds)  
heroku config:set CLEANUP_INTERVAL=300

# Download folder path
heroku config:set DOWNLOAD_FOLDER=web_downloads
```

## Security Recommendations

1. **Change Secret Key:**
```bash
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
```

2. **Enable HTTPS:**
Heroku provides free SSL certificates:
```bash
heroku certs:auto:enable
```

3. **Add Rate Limiting:**
Consider adding Flask-Limiter for rate limiting

4. **Add Authentication:**
For private use, add basic authentication

## Performance Optimization

### 1. Use CDN for Static Files
Upload CSS/JS to a CDN to reduce dyno load

### 2. Enable Compression
Add gzip compression in `web_app.py`:
```python
from flask_compress import Compress
Compress(app)
```

### 3. Worker Dynos
For heavy downloads, consider worker dynos

## Cost Estimation

**Free Tier:**
- Free for personal projects
- 550-1000 dyno hours/month
- Sleeps after inactivity

**Hobby Tier ($7/month):**
- No sleeping
- Custom domains
- Always available

## Updating Your Deployment

Make changes and deploy:
```bash
git add .
git commit -m "Update description"
git push heroku main
```

## Custom Domain

Add your own domain:
```bash
heroku domains:add www.yourdomain.com
```

Then configure DNS:
- Type: CNAME
- Name: www
- Value: your-app-name.herokuapp.com

## Backup and Restore

Heroku uses ephemeral storage - downloaded files are NOT persistent.
This is by design for the Mega downloader.

## Maintenance Mode

Enable maintenance mode during updates:
```bash
heroku maintenance:on
heroku maintenance:off
```

## Useful Commands

```bash
# Restart app
heroku restart

# Run shell
heroku run bash

# Check dyno info
heroku ps:type

# View config
heroku config

# Check quota
heroku ps:info
```

## Support

For issues:
1. Check logs: `heroku logs --tail`
2. Verify buildpacks: `heroku buildpacks`
3. Test locally: `heroku local web`
4. Check Heroku status: [status.heroku.com](https://status.heroku.com)

## Alternative: Docker Deployment

If you prefer Docker, create `Dockerfile`:
```dockerfile
FROM python:3.12
RUN apt-get update && apt-get install -y megatools
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn web_app:app --bind 0.0.0.0:$PORT
```

Deploy to Heroku Container Registry:
```bash
heroku container:push web
heroku container:release web
```

## Next Steps

After deployment:
1. Test with a small file download
2. Verify automatic cleanup works
3. Monitor logs for any errors
4. Set up custom domain (optional)
5. Enable SSL (automatic on Heroku)

Your app should now be live at: `https://your-app-name.herokuapp.com`

## Notes

- Files are stored temporarily and deleted automatically
- Heroku's filesystem is ephemeral - files are lost on dyno restart
- This is perfect for a download proxy service
- No persistent storage needed or recommended
