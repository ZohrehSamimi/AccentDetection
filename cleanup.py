#!/usr/bin/env python3
"""
Cleanup script to remove all the cached model files and temporary files
Run this to clean up your project directory
"""

import os
import shutil
from pathlib import Path

def cleanup_project_directory():
    """Clean up all model cache files and temporary files"""
    
    current_dir = Path(".")
    cleaned_items = []
    
    # List of directories/files to clean up
    cleanup_targets = [
        # Model cache directories
        "model_cache",
        "pretrained_models", 
        ".cache",
        "huggingface_cache",
        "transformers_cache",
        
        # SpeechBrain cache
        "lang-id-voxlingua107-ecapa",
        "accent-id-commonaccent_ecapa", 
        "accent-id-commonaccent_xlsr-en-english",
        
        # Temporary files
        "input_video.mp4",
        "audio.wav",
        "temp_video.mp4",
        "temp_audio.wav",
        
        # Python cache
        "__pycache__",
        "*.pyc",
        ".pytest_cache",
        
        # Jupyter notebook checkpoints
        ".ipynb_checkpoints",
        
        # Other common cache files
        ".DS_Store",
        "Thumbs.db"
    ]
    
    print("🧹 Starting cleanup of project directory...")
    print("=" * 50)
    
    for target in cleanup_targets:
        target_path = current_dir / target
        
        # Handle wildcard patterns
        if "*" in target:
            # Find files matching pattern
            pattern = target.replace("*", "")
            for item in current_dir.rglob(f"*{pattern}"):
                try:
                    if item.is_file():
                        item.unlink()
                        cleaned_items.append(str(item))
                        print(f"🗑️  Removed file: {item}")
                    elif item.is_dir():
                        shutil.rmtree(item)
                        cleaned_items.append(str(item))
                        print(f"🗑️  Removed directory: {item}")
                except Exception as e:
                    print(f"❌ Failed to remove {item}: {e}")
        else:
            # Handle direct paths
            if target_path.exists():
                try:
                    if target_path.is_file():
                        target_path.unlink()
                        cleaned_items.append(str(target_path))
                        print(f"🗑️  Removed file: {target_path}")
                    elif target_path.is_dir():
                        shutil.rmtree(target_path)
                        cleaned_items.append(str(target_path))
                        print(f"🗑️  Removed directory: {target_path}")
                except Exception as e:
                    print(f"❌ Failed to remove {target_path}: {e}")
    
    print("=" * 50)
    print(f"✅ Cleanup completed!")
    print(f"📊 Cleaned up {len(cleaned_items)} items")
    
    if cleaned_items:
        print("\n📋 Items removed:")
        for item in cleaned_items[:10]:  # Show first 10 items
            print(f"   - {item}")
        if len(cleaned_items) > 10:
            print(f"   ... and {len(cleaned_items) - 10} more items")
    else:
        print("💡 No cleanup needed - directory is already clean!")
    
    # Calculate freed space (rough estimate)
    print(f"\n💾 Your project directory should now be much cleaner!")
    print(f"🎯 Next time, the app will create files in organized cache directories.")


def show_current_directory_size():
    """Show current directory contents and sizes"""
    print("📁 Current directory contents:")
    print("=" * 50)
    
    current_dir = Path(".")
    total_size = 0
    
    for item in current_dir.iterdir():
        if item.is_file():
            size = item.stat().st_size
            total_size += size
            if size > 1024 * 1024:  # > 1MB
                print(f"📄 {item.name:<30} {size / (1024*1024):.1f} MB")
            elif size > 1024:  # > 1KB
                print(f"📄 {item.name:<30} {size / 1024:.1f} KB")
            else:
                print(f"📄 {item.name:<30} {size} bytes")
        elif item.is_dir() and not item.name.startswith('.'):
            try:
                dir_size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                total_size += dir_size
                if dir_size > 1024 * 1024:  # > 1MB
                    print(f"📁 {item.name:<30} {dir_size / (1024*1024):.1f} MB")
                elif dir_size > 1024:  # > 1KB
                    print(f"📁 {item.name:<30} {dir_size / 1024:.1f} KB")
                else:
                    print(f"📁 {item.name:<30} {dir_size} bytes")
            except:
                print(f"📁 {item.name:<30} (size unknown)")
    
    print("=" * 50)
    if total_size > 1024 * 1024 * 1024:  # > 1GB
        print(f"📊 Total directory size: {total_size / (1024*1024*1024):.1f} GB")
    elif total_size > 1024 * 1024:  # > 1MB
        print(f"📊 Total directory size: {total_size / (1024*1024):.1f} MB")
    else:
        print(f"📊 Total directory size: {total_size / 1024:.1f} KB")


if __name__ == "__main__":
    print("🧹 Project Directory Cleanup Tool")
    print("=" * 50)
    
    choice = input("What would you like to do?\n1. Show directory contents\n2. Clean up files\n3. Both\nEnter choice (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        show_current_directory_size()
        print()
    
    if choice in ['2', '3']:
        confirm = input("⚠️  This will delete model cache files and temporary files. Continue? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            cleanup_project_directory()
        else:
            print("❌ Cleanup cancelled.")
    
    print("\n✨ Done!")