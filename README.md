# Mega Downloader

A Python-based downloader for Mega.nz links that supports downloading single files, videos, and entire folders.

## Features

- Download single files from Mega links
- Download entire folders recursively
- Progress tracking with real-time updates
- Resume support for interrupted downloads
- Automatic folder structure preservation
- Support for all file types (videos, documents, archives, etc.)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/RecklessEvadingDriver/Megadownload.git
cd Megadownload
```

2. Install system dependencies:

**Ubuntu/Debian:**
```bash
sudo apt-get install megatools
```

**macOS:**
```bash
brew install megatools
```

**Other platforms:**
Visit [https://megatools.megous.com/](https://megatools.megous.com/) for installation instructions.

3. Install Python dependencies (optional, minimal):
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Download a single file or folder:
```bash
python megadownload.py <mega_link>
```

### Advanced Usage

Specify output directory:
```bash
python megadownload.py <mega_link> -o /path/to/output
```

Download to current directory:
```bash
python megadownload.py <mega_link> -o .
```

### Examples

Download a single file:
```bash
python megadownload.py "https://mega.nz/file/XXXXXXXX#YYYYYYYY"
```

Download an entire folder:
```bash
python megadownload.py "https://mega.nz/folder/XXXXXXXX#YYYYYYYY"
```

## Link Formats Supported

- File links: `https://mega.nz/file/...` or `https://mega.nz/#!...`
- Folder links: `https://mega.nz/folder/...` or `https://mega.nz/#F!...`

## Requirements

- Python 3.6 or higher
- megatools (command-line tools for Mega.nz)
  - Ubuntu/Debian: `sudo apt-get install megatools`
  - macOS: `brew install megatools`
  - Visit: https://megatools.megous.com/ for other platforms

## Notes

- Large files may take time to download depending on your internet connection
- The script will create a `downloads` folder by default if no output directory is specified
- Folder structure is preserved when downloading folders

## Troubleshooting

If you encounter issues:
1. Ensure megatools is properly installed: `megadl --version`
2. Check that your internet connection is stable
3. Verify that the Mega link is valid and accessible
4. Make sure you have write permissions in the output directory
5. For large downloads, ensure you have sufficient disk space

## License

This project is open source and available for personal and educational use.
