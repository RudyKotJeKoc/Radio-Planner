#!/usr/bin/env python3
"""
Radio-Planner Requirements Checker
Sprawdź czy mamy wszystko co potrzeba do działania
"""

import json
import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    required_files = [
        'index.html',
        'app.js',
        'styles.css',
        'manifest.json',
        'playlist.json',
        'sw.js',
        'package.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def check_directories():
    """Check if all required directories exist"""
    required_dirs = [
        'icons',
        'locales',
        'music',
        'lib',
        'fonts'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not os.path.isdir(dir_name):
            missing_dirs.append(dir_name)
    
    return missing_dirs

def check_json_files():
    """Validate JSON files"""
    json_files = ['manifest.json', 'playlist.json']
    invalid_json = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            invalid_json.append(f"{json_file}: {e}")
    
    return invalid_json

def check_music_files():
    """Check if music files referenced in playlist exist"""
    missing_music = []
    
    try:
        with open('playlist.json', 'r', encoding='utf-8') as f:
            playlist = json.load(f)
            
        for track in playlist.get('tracks', []):
            src = track.get('src', '')
            if src.startswith('/'):
                src = src[1:]  # Remove leading slash for local files
            
            if not os.path.exists(src):
                missing_music.append(f"Track '{track.get('title', 'Unknown')}': {src}")
                
    except Exception as e:
        return [f"Error checking music files: {e}"]
    
    return missing_music

def check_icons():
    """Check if required icon files exist"""
    required_icons = [
        'icons/favicon.svg',
        'icons/icon-192x192.png',
        'icons/icon-512x512.png'
    ]
    
    missing_icons = []
    for icon in required_icons:
        if not os.path.exists(icon):
            missing_icons.append(icon)
    
    return missing_icons

def check_localization():
    """Check if localization files exist"""
    required_locales = [
        'locales/nl.json',
        'locales/pl.json'
    ]
    
    missing_locales = []
    for locale in required_locales:
        if not os.path.exists(locale):
            missing_locales.append(locale)
    
    return missing_locales

def check_fallback_libraries():
    """Check if fallback libraries exist"""
    fallback_libs = [
        'lib/gsap.min.js'
    ]
    
    missing_libs = []
    for lib in fallback_libs:
        if not os.path.exists(lib):
            missing_libs.append(lib)
    
    return missing_libs

def main():
    print("🔍 DAREMON Radio ETS - Requirements Checker")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check files
    missing_files = check_files()
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        all_checks_passed = False
    else:
        print("✅ All required files present")
    
    # Check directories
    missing_dirs = check_directories()
    if missing_dirs:
        print("❌ Missing required directories:")
        for dir_name in missing_dirs:
            print(f"   • {dir_name}/")
        all_checks_passed = False
    else:
        print("✅ All required directories present")
    
    # Check JSON files
    invalid_json = check_json_files()
    if invalid_json:
        print("❌ Invalid JSON files:")
        for error in invalid_json:
            print(f"   • {error}")
        all_checks_passed = False
    else:
        print("✅ All JSON files valid")
    
    # Check icons
    missing_icons = check_icons()
    if missing_icons:
        print("❌ Missing icon files:")
        for icon in missing_icons:
            print(f"   • {icon}")
        all_checks_passed = False
    else:
        print("✅ All icon files present")
    
    # Check localization
    missing_locales = check_localization()
    if missing_locales:
        print("❌ Missing localization files:")
        for locale in missing_locales:
            print(f"   • {locale}")
        all_checks_passed = False
    else:
        print("✅ All localization files present")
    
    # Check fallback libraries
    missing_libs = check_fallback_libraries()
    if missing_libs:
        print("❌ Missing fallback library files:")
        for lib in missing_libs:
            print(f"   • {lib}")
        all_checks_passed = False
    else:
        print("✅ All fallback libraries present")
    
    # Check music files (warning only)
    missing_music = check_music_files()
    if missing_music:
        print("⚠️  Music files not found (add them manually):")
        for music in missing_music[:5]:  # Show only first 5
            print(f"   • {music}")
        if len(missing_music) > 5:
            print(f"   ... and {len(missing_music) - 5} more")
    else:
        print("✅ All referenced music files found")
    
    print("=" * 50)
    if all_checks_passed:
        print("🎉 All requirements met! Application ready to run.")
        return 0
    else:
        print("❌ Some requirements are missing. Please fix the above issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())