#!/usr/bin/env python3
"""
Digital Skills Assessment Platform - Complete Runner
Simple and reliable startup for the entire application
"""

import subprocess
import sys
import time
import webbrowser
import os
import signal
import threading
from pathlib import Path

class DigitalSkillsApp:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.backend_port = 8000
        self.frontend_port = 8080
        
    def print_banner(self):
        """Print application banner"""
        print("=" * 70)
        print("🧠 AI-Powered Digital Skills Assessment Platform")
        print("🏆 Hackathon Project - Complete System")
        print("=" * 70)
        print()
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        try:
            import fastapi
            import uvicorn
            print("✅ Core dependencies installed")
            return True
        except ImportError as e:
            print(f"❌ Missing dependency: {e}")
            print("💡 Install dependencies with: pip install -r requirements.txt")
            return False
            
    def start_backend_simple(self):
        """Start the backend server using main backend with RAG bot"""
        print(f"\n🚀 Starting backend server on port {self.backend_port}...")
        
        try:
            # Use the main backend with RAG bot
            self.backend_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "my-rag-bot.main:app",
                "--host", "0.0.0.0",
                "--port", str(self.backend_port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            time.sleep(3)
            
            # Test if server is running
            import urllib.request
            try:
                with urllib.request.urlopen(f"http://localhost:{self.backend_port}/health", timeout=5) as response:
                    if response.getcode() == 200:
                        print("✅ Backend server started successfully!")
                        return True
                    else:
                        print(f"❌ Backend server responded with status {response.getcode()}")
                        return False
            except Exception as e:
                print(f"❌ Backend server not responding: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
            
    def start_frontend(self):
        """Start the frontend HTTP server"""
        print(f"\n🌐 Starting frontend server on port {self.frontend_port}...")
        
        try:
            # Start HTTP server
            self.frontend_process = subprocess.Popen([
                sys.executable, "-m", "http.server", str(self.frontend_port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(2)
            print("✅ Frontend server started successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            return False
            
    def open_browser(self):
        """Open the application in browser"""
        print("\n🎯 Opening application in browser...")
        print("📋 Application URLs:")
        print(f"   📱 Main App: http://localhost:{self.frontend_port}/ui/index.html")
        print(f"   🔧 Backend API: http://localhost:{self.backend_port}")
        print(f"   📚 API Docs: http://localhost:{self.backend_port}/docs")
        print()
        
        try:
            webbrowser.open(f"http://localhost:{self.frontend_port}/ui/index.html")
            print("✅ Application opened in browser!")
        except Exception as e:
            print(f"❌ Error opening browser: {e}")
            print(f"💡 Manually open: http://localhost:{self.frontend_port}/ui/index.html")
            
    def wait_for_user(self):
        """Wait for user to stop the application"""
        print("\n" + "=" * 70)
        print("🎉 Application is running!")
        print("📱 Frontend: http://localhost:8080/ui/index.html")
        print("🔧 Backend: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("=" * 70)
        print("\n💡 Press Ctrl+C to stop the application")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()
            
    def cleanup(self):
        """Clean up processes on exit"""
        print("\n🛑 Stopping application...")
        
        if self.backend_process:
            self.backend_process.terminate()
            print("✅ Backend server stopped")
            
        if self.frontend_process:
            self.frontend_process.terminate()
            print("✅ Frontend server stopped")
            
        print("✅ Application stopped successfully!")
        
    def main(self):
        """Main application runner"""
        self.print_banner()
        
        # Check dependencies
        if not self.check_dependencies():
            return 1
            
        # Start backend
        if not self.start_backend_simple():
            print("\n❌ Failed to start backend. Exiting.")
            return 1
            
        # Start frontend
        if not self.start_frontend():
            print("\n❌ Failed to start frontend. Exiting.")
            self.cleanup()
            return 1
            
        # Open browser
        self.open_browser()
        
        # Wait for user
        self.wait_for_user()
        
        return 0

def main():
    """Entry point"""
    app = DigitalSkillsApp()
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        app.cleanup()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        return app.main()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        app.cleanup()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 