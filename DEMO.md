# Mega Downloader - Live Demo

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/RecklessEvadingDriver/Megadownload.git
cd Megadownload

# 2. Install megatools (Ubuntu/Debian)
sudo apt-get install megatools

# 3. Make script executable (optional)
chmod +x megadownload.py
```

## Usage Examples

### Example 1: Download a Single File
```bash
python3 megadownload.py "https://mega.nz/file/ABC123#KEY456"
```

**Output:**
```
[*] Output directory: /home/user/Megadownload/downloads
============================================================
MEGA DOWNLOADER
============================================================
[*] Detected link type: file

[*] Downloading file from: https://mega.nz/file/ABC123#KEY456
[*] Downloading to: downloads
[*] Running: megadl --path downloads https://mega.nz/file/ABC123#KEY456

[Downloading: myfile.mp4]
[100%] ████████████████████████ 45.2 MB/45.2 MB

[+] Successfully downloaded file

============================================================
DOWNLOAD COMPLETE
============================================================
```

### Example 2: Download an Entire Folder
```bash
python3 megadownload.py "https://mega.nz/folder/fMVAFQpK#RQbzNYN_0tRjcnI1TjMAMw"
```

**Output:**
```
[*] Output directory: /home/user/Megadownload/downloads
============================================================
MEGA DOWNLOADER
============================================================
[*] Detected link type: folder

[*] Downloading folder from: https://mega.nz/folder/fMVAFQpK#RQbzNYN_0tRjcnI1TjMAMw
[*] Downloading to: downloads
[*] Running: megadl --path downloads https://mega.nz/folder/fMVAFQpK#RQbzNYN_0tRjcnI1TjMAMw
[*] This may take a while for large folders...

[Downloading: file1.mp4]
[100%] ████████████████████████ 125.4 MB/125.4 MB
[Downloading: file2.pdf]
[100%] ████████████████████████ 2.3 MB/2.3 MB
[Downloading: file3.zip]
[100%] ████████████████████████ 67.8 MB/67.8 MB

[+] Successfully downloaded folder to: downloads

============================================================
DOWNLOAD COMPLETE
============================================================
```

### Example 3: Custom Output Directory
```bash
python3 megadownload.py "https://mega.nz/folder/ABC#KEY" -o ~/Videos/MyDownloads
```

**Output:**
```
[*] Output directory: /home/user/Videos/MyDownloads
============================================================
MEGA DOWNLOADER
============================================================
[*] Detected link type: folder

[*] Downloading folder from: https://mega.nz/folder/ABC#KEY
[*] Downloading to: /home/user/Videos/MyDownloads
...
```

### Example 4: Error Handling - Invalid Link
```bash
python3 megadownload.py "https://example.com/notamegalink"
```

**Output:**
```
[!] Error: Invalid Mega link. URL must contain 'mega.nz' or 'mega.co.nz'
```

### Example 5: Help Command
```bash
python3 megadownload.py --help
```

**Output:**
```
usage: megadownload.py [-h] [-o OUTPUT] url

Download files and folders from Mega.nz links

positional arguments:
  url                   Mega.nz file or folder URL

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: downloads)

Examples:
  Download a file:
    python megadownload.py "https://mega.nz/file/XXXXXXXX#YYYYYYYY"
  
  Download a folder:
    python megadownload.py "https://mega.nz/folder/XXXXXXXX#YYYYYYYY"
  
  Specify output directory:
    python megadownload.py "https://mega.nz/file/XXX#YYY" -o ./my_downloads
```

## Features Demonstrated

✅ **Automatic Link Detection**
- Detects file vs folder links automatically
- Supports both old and new Mega URL formats

✅ **Progress Tracking**
- Real-time download progress bars
- File size and transfer speed information

✅ **Recursive Folder Downloads**
- Downloads all files in a folder
- Preserves folder structure

✅ **Error Handling**
- Clear error messages
- Validates URLs before attempting download

✅ **Flexible Output**
- Default downloads folder
- Custom output directory support

## Supported Link Formats

| Format | Example | Type |
|--------|---------|------|
| New file format | `https://mega.nz/file/ABC123#KEY` | File |
| Old file format | `https://mega.nz/#!ABC123` | File |
| New folder format | `https://mega.nz/folder/ABC123#KEY` | Folder |
| Old folder format | `https://mega.nz/#F!ABC123#KEY` | Folder |

## Real-World Use Cases

### 1. Backup Download
```bash
# Download a backup folder to external drive
python3 megadownload.py "https://mega.nz/folder/BACKUP#KEY" -o /mnt/external/backups
```

### 2. Video Collection
```bash
# Download video tutorials to Videos folder
python3 megadownload.py "https://mega.nz/folder/VIDEOS#KEY" -o ~/Videos/Tutorials
```

### 3. Document Archive
```bash
# Download important documents
python3 megadownload.py "https://mega.nz/folder/DOCS#KEY" -o ~/Documents/Archive
```

## Notes

- Large files/folders may take time depending on internet speed
- Free Mega accounts have bandwidth limitations
- Downloads can be resumed if interrupted
- All files preserve original names and timestamps
