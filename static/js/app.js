// Mega Downloader Web App JavaScript

// Configuration constants
const STATUS_CHECK_INTERVAL = 2000; // 2 seconds
const AUTO_RESET_DELAY = 3000; // 3 seconds

let currentDownloadId = null;
let statusCheckInterval = null;

// DOM Elements
const urlInput = document.getElementById('mega-url');
const downloadBtn = document.getElementById('download-btn');
const statusSection = document.getElementById('status-section');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');
const statusMessage = document.getElementById('status-message');
const errorMessage = document.getElementById('error-message');
const filesList = document.getElementById('files-list');
const downloadAllBtn = document.getElementById('download-all-btn');
const newDownloadBtn = document.getElementById('new-download-btn');
const retryBtn = document.getElementById('retry-btn');

// Event Listeners
downloadBtn.addEventListener('click', startDownload);
urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        startDownload();
    }
});
newDownloadBtn.addEventListener('click', resetForm);
retryBtn.addEventListener('click', resetForm);

// Start download
async function startDownload() {
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Please enter a Mega.nz URL');
        return;
    }
    
    if (!url.includes('mega.nz') && !url.includes('mega.co.nz')) {
        showError('Please enter a valid Mega.nz URL');
        return;
    }
    
    // Hide all sections
    hideAllSections();
    
    // Show status section
    statusSection.style.display = 'block';
    statusMessage.textContent = 'Initializing download...';
    downloadBtn.disabled = true;
    
    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to start download');
        }
        
        currentDownloadId = data.download_id;
        
        // Start checking status
        checkStatus();
        
    } catch (error) {
        showError(error.message);
        downloadBtn.disabled = false;
    }
}

// Check download status
async function checkStatus() {
    if (!currentDownloadId) return;
    
    try {
        const response = await fetch(`/status/${currentDownloadId}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to get status');
        }
        
        statusMessage.textContent = data.message;
        
        if (data.status === 'completed') {
            // Download completed
            clearInterval(statusCheckInterval);
            showResults(data);
        } else if (data.status === 'error') {
            // Error occurred
            clearInterval(statusCheckInterval);
            showError(data.message);
        } else {
            // Still downloading, check again after configured interval
            statusCheckInterval = setTimeout(checkStatus, STATUS_CHECK_INTERVAL);
        }
        
    } catch (error) {
        clearInterval(statusCheckInterval);
        showError(error.message);
    }
}

// Show results
function showResults(data) {
    hideAllSections();
    resultsSection.style.display = 'block';
    downloadBtn.disabled = false;
    
    // Clear previous files list
    filesList.innerHTML = '';
    
    if (data.files && data.files.length > 0) {
        const filesListDiv = document.createElement('div');
        filesListDiv.className = 'files-list';
        
        data.files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            
            const fileInfo = document.createElement('div');
            fileInfo.className = 'file-info';
            
            const fileIcon = document.createElement('span');
            fileIcon.className = 'file-icon';
            fileIcon.textContent = getFileIcon(file.name);
            
            const fileDetails = document.createElement('div');
            
            const fileName = document.createElement('div');
            fileName.className = 'file-name';
            fileName.textContent = file.name;
            
            const fileSize = document.createElement('div');
            fileSize.className = 'file-size';
            fileSize.textContent = formatBytes(file.size);
            
            fileDetails.appendChild(fileName);
            fileDetails.appendChild(fileSize);
            
            fileInfo.appendChild(fileIcon);
            fileInfo.appendChild(fileDetails);
            
            const downloadFileBtn = document.createElement('button');
            downloadFileBtn.className = 'file-download-btn';
            downloadFileBtn.textContent = 'Download';
            downloadFileBtn.onclick = () => downloadFile(file.path);
            
            fileItem.appendChild(fileInfo);
            fileItem.appendChild(downloadFileBtn);
            filesListDiv.appendChild(fileItem);
        });
        
        filesList.appendChild(filesListDiv);
    }
    
    // Set up download all button
    downloadAllBtn.onclick = () => downloadAll();
}

// Download individual file
function downloadFile(filePath) {
    window.location.href = `/download_file/${currentDownloadId}/${filePath}`;
}

// Download all files as ZIP
function downloadAll() {
    window.location.href = `/download_all/${currentDownloadId}`;
    
    // Automatically start a new download session after a brief delay
    setTimeout(() => {
        resetForm();
    }, AUTO_RESET_DELAY);
}

// Show error
function showError(message) {
    hideAllSections();
    errorSection.style.display = 'block';
    errorMessage.textContent = message;
    downloadBtn.disabled = false;
}

// Hide all sections
function hideAllSections() {
    statusSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
}

// Reset form
function resetForm() {
    urlInput.value = '';
    currentDownloadId = null;
    hideAllSections();
    downloadBtn.disabled = false;
    
    // Clear interval if exists
    if (statusCheckInterval) {
        clearTimeout(statusCheckInterval);
        statusCheckInterval = null;
    }
}

// Helper: Get file icon based on extension
function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    
    const iconMap = {
        'mp4': '🎥', 'avi': '🎥', 'mkv': '🎥', 'mov': '🎥',
        'mp3': '🎵', 'wav': '🎵', 'flac': '🎵',
        'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️',
        'pdf': '📄', 'doc': '📄', 'docx': '📄', 'txt': '📄',
        'zip': '📦', 'rar': '📦', '7z': '📦',
        'exe': '⚙️', 'msi': '⚙️'
    };
    
    return iconMap[ext] || '📁';
}

// Helper: Format bytes to human readable
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Initialize
console.log('Mega Downloader Web App loaded');
