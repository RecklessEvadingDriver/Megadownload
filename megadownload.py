#!/usr/bin/env python3
"""
Mega Downloader - Download files and folders from Mega.nz links
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path


class MegaDownloader:
    """Class to handle Mega.nz downloads using megatools"""
    
    def __init__(self, output_dir="downloads"):
        """
        Initialize the Mega downloader
        
        Args:
            output_dir (str): Directory where files will be downloaded
        """
        # Check if megatools is installed
        if not shutil.which('megadl'):
            raise RuntimeError(
                "megatools is not installed. Please install it:\n"
                "  Ubuntu/Debian: sudo apt-get install megatools\n"
                "  MacOS: brew install megatools\n"
                "  Or visit: https://megatools.megous.com/"
            )
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"[*] Output directory: {self.output_dir.absolute()}")
    
    def parse_mega_url(self, url):
        """
        Parse and validate Mega URL
        
        Args:
            url (str): Mega.nz URL
            
        Returns:
            tuple: (link_type, url) where link_type is 'file' or 'folder'
        """
        url = url.strip()
        
        # Detect link type
        if '/folder/' in url or '/#F!' in url or '#F!' in url:
            return ('folder', url)
        elif '/file/' in url or '/#!' in url or '#!' in url:
            return ('file', url)
        else:
            raise ValueError("Invalid Mega link format. Link must be a file or folder link.")
    
    def download_file(self, url, output_path=None):
        """
        Download a single file from Mega using megadl
        
        Args:
            url (str): Mega file URL
            output_path (str): Optional custom output path
            
        Returns:
            str: Path to downloaded file
        """
        try:
            print(f"\n[*] Downloading file from: {url}")
            
            # Build megadl command
            if output_path:
                dest_path = Path(output_path)
                dest_dir = dest_path.parent
                dest_dir.mkdir(parents=True, exist_ok=True)
                cmd = ['megadl', '--path', str(dest_dir), url]
            else:
                cmd = ['megadl', '--path', str(self.output_dir), url]
            
            print(f"[*] Running: {' '.join(cmd)}")
            
            # Execute download
            result = subprocess.run(
                cmd,
                capture_output=False,
                text=True,
                check=True
            )
            
            if result.returncode == 0:
                print(f"[+] Successfully downloaded file")
                return str(self.output_dir)
            else:
                raise RuntimeError(f"Download failed with exit code {result.returncode}")
            
        except subprocess.CalledProcessError as e:
            print(f"[!] Error downloading file: {e}")
            raise
        except Exception as e:
            print(f"[!] Error: {e}")
            raise
    
    def download_folder(self, url, base_path=None):
        """
        Download an entire folder from Mega recursively using megadl
        
        Args:
            url (str): Mega folder URL
            base_path (str): Base path for downloads
            
        Returns:
            list: List of downloaded file paths
        """
        try:
            print(f"\n[*] Downloading folder from: {url}")
            
            # Determine output directory
            if base_path:
                output_dir = Path(base_path)
            else:
                output_dir = self.output_dir
            
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"[*] Downloading to: {output_dir}")
            
            # Build megadl command for folder
            cmd = ['megadl', '--path', str(output_dir), url]
            
            print(f"[*] Running: {' '.join(cmd)}")
            print("[*] This may take a while for large folders...")
            
            # Execute download
            result = subprocess.run(
                cmd,
                capture_output=False,
                text=True,
                check=True
            )
            
            if result.returncode == 0:
                print(f"\n[+] Successfully downloaded folder to: {output_dir}")
                return [str(output_dir)]
            else:
                raise RuntimeError(f"Download failed with exit code {result.returncode}")
            
        except subprocess.CalledProcessError as e:
            print(f"[!] Error downloading folder: {e}")
            raise
        except Exception as e:
            print(f"[!] Error: {e}")
            raise
    
    def download(self, url):
        """
        Auto-detect and download from Mega link (file or folder)
        
        Args:
            url (str): Mega.nz URL
            
        Returns:
            Appropriate download result based on link type
        """
        try:
            link_type, validated_url = self.parse_mega_url(url)
            
            print(f"[*] Detected link type: {link_type}")
            
            if link_type == 'file':
                return self.download_file(validated_url)
            elif link_type == 'folder':
                return self.download_folder(validated_url)
            else:
                raise ValueError(f"Unknown link type: {link_type}")
                
        except Exception as e:
            print(f"[!] Error: {e}")
            raise


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Download files and folders from Mega.nz links',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Download a file:
    python megadownload.py "https://mega.nz/file/XXXXXXXX#YYYYYYYY"
  
  Download a folder:
    python megadownload.py "https://mega.nz/folder/XXXXXXXX#YYYYYYYY"
  
  Specify output directory:
    python megadownload.py "https://mega.nz/file/XXX#YYY" -o ./my_downloads
        """
    )
    
    parser.add_argument(
        'url',
        help='Mega.nz file or folder URL'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='downloads',
        help='Output directory (default: downloads)'
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url:
        parser.error("Mega URL is required")
    
    if 'mega.nz' not in args.url and 'mega.co.nz' not in args.url:
        print("[!] Error: Invalid Mega link. URL must contain 'mega.nz' or 'mega.co.nz'")
        sys.exit(1)
    
    try:
        # Create downloader instance
        downloader = MegaDownloader(output_dir=args.output)
        
        # Download
        print("="*60)
        print("MEGA DOWNLOADER")
        print("="*60)
        
        result = downloader.download(args.url)
        
        print("\n" + "="*60)
        print("DOWNLOAD COMPLETE")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n[!] Download interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
