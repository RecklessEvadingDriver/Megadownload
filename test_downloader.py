#!/usr/bin/env python3
"""
Test script for megadownload.py
Demonstrates the URL parsing and validation capabilities
"""

from megadownload import MegaDownloader
import sys

def test_url_parsing():
    """Test URL parsing functionality"""
    print("="*60)
    print("TESTING MEGA DOWNLOADER URL PARSING")
    print("="*60)
    
    try:
        downloader = MegaDownloader(output_dir="/tmp/test_downloads")
        
        # Test cases
        test_cases = [
            ("https://mega.nz/file/ABC123#XYZ", "file"),
            ("https://mega.nz/folder/DEF456#UVW", "folder"),
            ("https://mega.nz/#!ABC123", "file"),
            ("https://mega.nz/#F!ABC123#KEY", "folder"),
        ]
        
        print("\nTesting URL detection:")
        all_passed = True
        for url, expected_type in test_cases:
            try:
                detected_type, _ = downloader.parse_mega_url(url)
                status = "✓" if detected_type == expected_type else "✗"
                print(f"  {status} {url[:50]:50s} -> {detected_type}")
                if detected_type != expected_type:
                    all_passed = False
                    print(f"    Expected: {expected_type}, Got: {detected_type}")
            except Exception as e:
                print(f"  ✗ {url[:50]:50s} -> ERROR: {e}")
                all_passed = False
        
        # Test invalid URLs
        print("\nTesting invalid URL detection:")
        invalid_urls = [
            "https://example.com/test",
            "https://mega.nz/invalid",
            "not a url at all",
        ]
        
        for url in invalid_urls:
            try:
                detected_type, _ = downloader.parse_mega_url(url)
                print(f"  ✗ {url[:50]:50s} -> Should have failed but detected as {detected_type}")
                all_passed = False
            except ValueError as e:
                print(f"  ✓ {url[:50]:50s} -> Correctly rejected")
        
        print("\n" + "="*60)
        if all_passed:
            print("ALL TESTS PASSED ✓")
            print("="*60)
            return 0
        else:
            print("SOME TESTS FAILED ✗")
            print("="*60)
            return 1
            
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(test_url_parsing())
