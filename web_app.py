#!/usr/bin/env python3
"""
Mega Downloader Web Interface
A Flask-based web application for downloading files and folders from Mega.nz
Optimized for Heroku deployment with automatic file cleanup
"""

import os
import sys
import threading
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
import uuid
import shutil

# Import the MegaDownloader class
from megadownload import MegaDownloader

app = Flask(__name__)

# Configuration - use environment variables for production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mega-downloader-secret-key-change-in-production')
app.config['DOWNLOAD_FOLDER'] = Path(os.environ.get('DOWNLOAD_FOLDER', 'web_downloads'))
app.config['DOWNLOAD_FOLDER'].mkdir(exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max request size

# Heroku-specific settings
CLEANUP_AGE = int(os.environ.get('CLEANUP_AGE', 3600))  # 1 hour default
CLEANUP_INTERVAL = int(os.environ.get('CLEANUP_INTERVAL', 300))  # 5 minutes default

# Store download status
download_status = {}


class WebDownloadManager:
    """Manages downloads with status tracking for web interface"""
    
    def __init__(self):
        self.active_downloads = {}
    
    def start_download(self, url, download_id):
        """Start a download in a background thread"""
        def download_task():
            try:
                download_status[download_id] = {
                    'status': 'downloading',
                    'message': 'Starting download...',
                    'url': url,
                    'files': []
                }
                
                # Create unique folder for this download
                output_dir = app.config['DOWNLOAD_FOLDER'] / download_id
                output_dir.mkdir(exist_ok=True)
                
                # Initialize downloader
                downloader = MegaDownloader(output_dir=str(output_dir))
                
                # Parse URL to get link type
                link_type, validated_url = downloader.parse_mega_url(url)
                
                download_status[download_id]['message'] = f'Downloading {link_type}...'
                
                # Download
                if link_type == 'file':
                    result = downloader.download_file(validated_url)
                elif link_type == 'folder':
                    result = downloader.download_folder(validated_url)
                
                # List downloaded files
                files = []
                for root, dirs, filenames in os.walk(output_dir):
                    for filename in filenames:
                        file_path = Path(root) / filename
                        rel_path = file_path.relative_to(output_dir)
                        files.append({
                            'name': filename,
                            'path': str(rel_path),
                            'size': file_path.stat().st_size
                        })
                
                download_status[download_id] = {
                    'status': 'completed',
                    'message': 'Download completed successfully!',
                    'url': url,
                    'link_type': link_type,
                    'files': files
                }
                
            except Exception as e:
                download_status[download_id] = {
                    'status': 'error',
                    'message': str(e),
                    'url': url,
                    'files': []
                }
        
        thread = threading.Thread(target=download_task, daemon=True)
        thread.start()
        self.active_downloads[download_id] = thread


manager = WebDownloadManager()


def cleanup_old_downloads():
    """Automatically cleanup downloads older than configured age"""
    while True:
        time.sleep(CLEANUP_INTERVAL)  # Check based on config
        try:
            current_time = time.time()
            download_folder = app.config['DOWNLOAD_FOLDER']
            
            if not download_folder.exists():
                continue
            
            # Check all download directories
            for item in download_folder.iterdir():
                if item.is_dir():
                    # Check if directory is older than configured age
                    dir_age = current_time - item.stat().st_mtime
                    if dir_age > CLEANUP_AGE:
                        print(f"[Cleanup] Removing old download directory: {item.name}")
                        shutil.rmtree(item)
                        # Remove from status if exists
                        if item.name in download_status:
                            del download_status[item.name]
                elif item.suffix == '.zip':
                    # Check if zip file is older than 10 minutes
                    zip_age = current_time - item.stat().st_mtime
                    if zip_age > 600:  # 10 minutes for ZIP files
                        print(f"[Cleanup] Removing old ZIP file: {item.name}")
                        item.unlink()
        except Exception as e:
            print(f"[Cleanup] Error during cleanup: {e}")


# Start cleanup task in background
cleanup_thread = threading.Thread(target=cleanup_old_downloads, daemon=True)
cleanup_thread.start()


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    """Handle download request"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Validate URL
    if 'mega.nz' not in url and 'mega.co.nz' not in url:
        return jsonify({'error': 'Invalid Mega link. URL must contain mega.nz or mega.co.nz'}), 400
    
    # Generate unique download ID
    download_id = str(uuid.uuid4())
    
    # Start download in background
    manager.start_download(url, download_id)
    
    return jsonify({
        'download_id': download_id,
        'message': 'Download started'
    })


@app.route('/status/<download_id>')
def status(download_id):
    """Get download status"""
    if download_id not in download_status:
        return jsonify({'error': 'Download not found'}), 404
    
    return jsonify(download_status[download_id])


@app.route('/download_file/<download_id>/<path:filename>')
def download_file(download_id, filename):
    """Download a specific file and cleanup after"""
    file_path = app.config['DOWNLOAD_FOLDER'] / download_id / filename
    
    if not file_path.exists():
        return jsonify({'error': 'File not found'}), 404
    
    # Send file and schedule cleanup after response
    response = send_file(file_path, as_attachment=True)
    
    # Note: File will be cleaned up when user calls cleanup endpoint
    # or after timeout (handled by automatic cleanup task)
    return response


@app.route('/download_all/<download_id>')
def download_all(download_id):
    """Download all files as a zip and cleanup after"""
    download_dir = app.config['DOWNLOAD_FOLDER'] / download_id
    
    if not download_dir.exists():
        return jsonify({'error': 'Download not found'}), 404
    
    # Create zip file
    zip_path = app.config['DOWNLOAD_FOLDER'] / f"{download_id}.zip"
    shutil.make_archive(str(zip_path.with_suffix('')), 'zip', download_dir)
    
    # Send file
    response = send_file(zip_path, as_attachment=True, download_name='mega_download.zip')
    
    # Schedule cleanup after sending
    def cleanup_after_download():
        time.sleep(2)  # Wait for download to complete
        try:
            # Remove download directory
            if download_dir.exists():
                shutil.rmtree(download_dir)
            # Remove zip file
            if zip_path.exists():
                zip_path.unlink()
            # Remove from status
            if download_id in download_status:
                del download_status[download_id]
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    # Start cleanup in background
    cleanup_thread = threading.Thread(target=cleanup_after_download, daemon=True)
    cleanup_thread.start()
    
    return response


@app.route('/cleanup/<download_id>', methods=['POST'])
def cleanup(download_id):
    """Clean up downloaded files"""
    download_dir = app.config['DOWNLOAD_FOLDER'] / download_id
    
    if download_dir.exists():
        shutil.rmtree(download_dir)
    
    # Remove from status
    if download_id in download_status:
        del download_status[download_id]
    
    return jsonify({'message': 'Cleanup completed'})


if __name__ == '__main__':
    # Get port from environment variable (Heroku sets this)
    port = int(os.environ.get('PORT', 5000))
    
    print("="*60)
    print("MEGA DOWNLOADER WEB INTERFACE")
    print("="*60)
    print("\nStarting web server...")
    print(f"Port: {port}")
    print(f"Cleanup age: {CLEANUP_AGE} seconds")
    print(f"Cleanup interval: {CLEANUP_INTERVAL} seconds")
    
    if 'PORT' in os.environ:
        print("Running in production mode (Heroku)")
        print("\nAutomatic cleanup enabled:")
        print(f"  - Files deleted after download")
        print(f"  - Old downloads cleaned every {CLEANUP_INTERVAL//60} minutes")
        print(f"  - Downloads older than {CLEANUP_AGE//3600} hour(s) removed")
    else:
        print(f"Open your browser and navigate to: http://localhost:{port}")
        print("\nPress CTRL+C to stop the server")
    
    print("="*60)
    
    # Run with debug off in production
    debug_mode = 'PORT' not in os.environ
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
