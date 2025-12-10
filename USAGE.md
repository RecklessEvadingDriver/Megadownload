# Megadownload - Usage Examples

This document provides examples of how to use the Mega downloader.

## Basic Examples

### 1. Download a Single File

```bash
python megadownload.py "https://mega.nz/file/XXXXXXXX#YYYYYYYY"
```

This will download the file to the `downloads` folder in the current directory.

### 2. Download a Folder

```bash
python megadownload.py "https://mega.nz/folder/XXXXXXXX#YYYYYYYY"
```

This will download all files in the folder recursively to the `downloads` folder.

### 3. Specify Custom Output Directory

```bash
python megadownload.py "https://mega.nz/file/XXXXXXXX#YYYYYYYY" -o /path/to/output
```

### 4. Download to Current Directory

```bash
python megadownload.py "https://mega.nz/folder/XXXXXXXX#YYYYYYYY" -o .
```

## Supported Link Formats

The downloader supports both old and new Mega link formats:

### File Links
- New format: `https://mega.nz/file/XXXXXXXX#YYYYYYYY`
- Old format: `https://mega.nz/#!XXXXXXXX!YYYYYYYY`

### Folder Links
- New format: `https://mega.nz/folder/XXXXXXXX#YYYYYYYY`
- Old format: `https://mega.nz/#F!XXXXXXXX!YYYYYYYY`

## Features

- **Automatic Detection**: The script automatically detects whether the link is for a file or folder
- **Recursive Downloads**: Folder links download all files within the folder
- **Progress Tracking**: Real-time progress display during downloads
- **Resume Support**: Interrupted downloads can be resumed
- **Error Handling**: Clear error messages for invalid links or failed downloads

## Advanced Usage

### Testing URL Parsing

You can test the URL parsing without downloading:

```bash
python test_downloader.py
```

This runs validation tests on the URL parsing logic.

## Common Issues and Solutions

### Issue: "megatools is not installed"
**Solution**: Install megatools using your package manager:
- Ubuntu/Debian: `sudo apt-get install megatools`
- macOS: `brew install megatools`

### Issue: "Permission denied"
**Solution**: Ensure you have write permissions in the output directory or use a different directory.

### Issue: Invalid link format
**Solution**: Make sure your link starts with `https://mega.nz/` and contains either `/file/` or `/folder/`.

## Notes

- Large files may take time to download depending on your connection
- The script preserves the folder structure when downloading folders
- Downloads are saved with their original filenames from Mega
- Free Mega accounts have bandwidth limitations

## Examples with Real Use Cases

### Downloading a Video Collection
```bash
python megadownload.py "https://mega.nz/folder/ABC123#XYZ" -o ~/Videos/MegaDownloads
```

### Downloading a Single Document
```bash
python megadownload.py "https://mega.nz/file/DEF456#UVW" -o ~/Documents
```

### Batch Download Script
```bash
#!/bin/bash
# Download multiple links
python megadownload.py "https://mega.nz/file/LINK1#KEY1" -o ./downloads
python megadownload.py "https://mega.nz/folder/LINK2#KEY2" -o ./downloads
python megadownload.py "https://mega.nz/file/LINK3#KEY3" -o ./downloads
```
