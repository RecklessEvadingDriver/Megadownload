# Mega Downloader Web Interface

A beautiful, user-friendly web interface for downloading files and folders from Mega.nz links.

## Features

- 🌐 **Web-based Interface** - Easy to use, no command line needed
- 📁 **Folder Support** - Download entire folders recursively
- 🎥 **All File Types** - Videos, documents, images, archives, and more
- ⚡ **Real-time Progress** - Live status updates during downloads
- 📦 **ZIP Downloads** - Download all files as a single ZIP archive
- 🗑️ **Auto Cleanup** - Files automatically deleted after download (Heroku-ready)
- 🎨 **Modern UI** - Beautiful gradient design with smooth animations
- 📱 **Responsive** - Works on desktop, tablet, and mobile devices
- ☁️ **Heroku Ready** - Deploy to Heroku with one click

## Installation

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install megatools
```

**macOS:**
```bash
brew install megatools
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install Flask, which is required for the web interface.

## Usage

### Starting the Web Server (Local)

```bash
python3 web_app.py
```

The server will start on `http://localhost:5000`

### Deploying to Heroku

For production deployment on Heroku with automatic cleanup:

**See [HEROKU_DEPLOY.md](HEROKU_DEPLOY.md) for complete Heroku deployment instructions.**

Quick deployment:
```bash
heroku create
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
heroku buildpacks:add --index 2 heroku/python
git push heroku main
```

You should see:
```
============================================================
MEGA DOWNLOADER WEB INTERFACE
============================================================

Starting web server...
Open your browser and navigate to: http://localhost:5000

Press CTRL+C to stop the server
============================================================
```

### Using the Web Interface

1. **Open your browser** and go to `http://localhost:5000`

2. **Paste a Mega.nz link** into the input field
   - File link: `https://mega.nz/file/XXXXX#YYYYY`
   - Folder link: `https://mega.nz/folder/XXXXX#YYYYY`

3. **Click "Download"** button

4. **Wait for the download** to complete
   - You'll see real-time status updates
   - Progress messages will show what's happening

5. **Download your files**
   - Download individual files by clicking on them
   - Download all files as a ZIP using "Download All as ZIP" button

### Screenshots

The web interface features:
- Clean, modern design with purple gradient
- Large input field for Mega links
- Real-time download status with loading spinner
- File list with icons and sizes
- Individual file download buttons
- One-click ZIP download for all files

## API Endpoints

The web app provides several REST API endpoints:

### POST /download
Start a new download

**Request:**
```json
{
  "url": "https://mega.nz/folder/XXXXX#YYYYY"
}
```

**Response:**
```json
{
  "download_id": "uuid-string",
  "message": "Download started"
}
```

### GET /status/<download_id>
Get download status

**Response:**
```json
{
  "status": "downloading|completed|error",
  "message": "Status message",
  "url": "original url",
  "files": [
    {
      "name": "filename.mp4",
      "path": "relative/path",
      "size": 1234567
    }
  ]
}
```

### GET /download_file/<download_id>/<path>
Download a specific file

### GET /download_all/<download_id>
Download all files as ZIP

### POST /cleanup/<download_id>
Clean up downloaded files from server

## Configuration

### Custom Port

To run on a different port:

```python
# Edit web_app.py, line 178
app.run(host='0.0.0.0', port=8080, debug=True)  # Change 5000 to your port
```

### Custom Download Directory

To change where files are downloaded:

```python
# Edit web_app.py, line 20
app.config['DOWNLOAD_FOLDER'] = Path('custom_path')
```

### Production Deployment

For production, use a proper WSGI server like Gunicorn:

```bash
# Install gunicorn
pip install gunicorn

# Run the app
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

## File Structure

```
Megadownload/
├── web_app.py              # Flask application
├── megadownload.py         # Core downloader logic
├── templates/
│   └── index.html          # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css       # Styles and animations
│   └── js/
│       └── app.js          # Frontend JavaScript
└── web_downloads/          # Downloaded files (auto-created)
```

## Security Considerations

- The web app generates unique UUIDs for each download session
- Files are stored in isolated directories per download
- The default secret key should be changed in production
- Consider implementing authentication for public deployments
- Rate limiting is recommended for production use

## Troubleshooting

### Port already in use
If port 5000 is already in use:
```bash
# Find and kill the process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port (edit web_app.py)
```

### Megatools not found
Ensure megatools is installed:
```bash
which megadl
megadl --version
```

### Downloads not working
- Check that the Mega link is valid and accessible
- Ensure you have network connectivity
- Check the console output for error messages
- Verify megatools can access mega.nz: `ping mega.nz`

### Files not appearing
- Check the `web_downloads/` directory
- Look at the server console for error messages
- Ensure proper file permissions

## Advanced Usage

### Running in Background

```bash
# Using nohup
nohup python3 web_app.py > web_app.log 2>&1 &

# Using screen
screen -S megadownloader
python3 web_app.py
# Press Ctrl+A then D to detach
```

### Using with Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.12
RUN apt-get update && apt-get install -y megatools
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "web_app.py"]
```

Build and run:
```bash
docker build -t megadownloader .
docker run -p 5000:5000 megadownloader
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Contributing

To add new features to the web interface:

1. Backend changes: Edit `web_app.py`
2. Frontend HTML: Edit `templates/index.html`
3. Styling: Edit `static/css/style.css`
4. JavaScript: Edit `static/js/app.js`

## License

This web interface is part of the Megadownload project and is available for personal and educational use.

## Support

For issues or questions:
- Check the main README.md
- Review the troubleshooting section above
- Check console logs for error messages
