#!/usr/bin/env python3
"""
Launcher script for the Streamlit web interface.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        print("✅ Streamlit is installed")
        return True
    except ImportError:
        print("❌ Streamlit is not installed")
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def check_api_key():
    """Check if API key is configured."""
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key found in environment")
        return True
    else:
        print("⚠️  No OpenAI API key found in environment")
        print("   You can set it with: export OPENAI_API_KEY='your-key-here'")
        print("   Or enter it in the web interface")
        return False

def main():
    """Launch the Streamlit app."""
    print("🚀 Launching OpenAI Responses API Web Interface")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check API key
    check_api_key()
    
    print("\n🌐 Starting Streamlit app...")
    print("   The app will open in your default browser")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

if __name__ == "__main__":
    main() 