#!/usr/bin/env python3
"""
LifeLink - Blood & Organ Donation System
Professional run script for easy startup
"""

import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        print("✅ Flask is installed")
        return True
    except ImportError:
        print("❌ Flask is not installed")
        return False

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("✅ Flask installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Flask")
        return False

def main():
    print("❤️  Starting LifeLink - Blood & Organ Donation System")
    print("=" * 60)

    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing Flask...")
        if not install_dependencies():
            print("Please install Flask manually: pip install flask")
            return

    # Start the application
    print("\n🚀 Starting the application...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)

    # Import and run the app
    try:
        print("\n🔄 Loading LifeLink application...")
        from blood_donation_app import app
        print("✅ Application loaded successfully!")
        print("\n💝 Features available:")
        print("   • Professional donor registration system")
        print("   • Real-time donation request matching")
        print("   • Location-based donor notification")
        print("   • Comprehensive dashboard interfaces")
        print("   • Blood type compatibility checking")
        print("   • Organ donation coordination")
        print("\n🚀 Server starting...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 LifeLink stopped safely!")
        print("Thank you for supporting life-saving donations! ❤️")
    except ImportError:
        print("❌ Could not find blood_donation_app.py")
        print("Make sure the main app file is in the current directory")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("Make sure all template files are in the 'templates/' folder")

if __name__ == "__main__":
    main()
