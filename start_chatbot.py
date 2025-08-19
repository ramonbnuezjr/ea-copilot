#!/usr/bin/env python3
"""
EA Chatbot Startup Script
Generates mock data and starts the chatbot server
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'fastapi', 'uvicorn', 'google-generativeai', 'chromadb', 
        'sentence-transformers', 'pandas', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install them using:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_environment():
    """Check if required environment variables are set."""
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY environment variable is not set")
        print("Please set it in your .env file or environment")
        return False
    
    print("✅ Environment variables are configured")
    return True

def generate_mock_data():
    """Generate mock datasets."""
    print("📊 Generating mock datasets...")
    
    try:
        from mock_data_generator import EAMockDataGenerator
        generator = EAMockDataGenerator()
        generator.generate_all_data()
        print("✅ Mock data generated successfully")
        return True
    except Exception as e:
        print(f"❌ Error generating mock data: {e}")
        return False

def setup_rag_corpus():
    """Set up RAG corpus directory."""
    print("📚 Setting up RAG corpus...")
    
    corpus_dir = "./rag_corpus"
    if not os.path.exists(corpus_dir):
        os.makedirs(corpus_dir)
        print("✅ RAG corpus directory created")
    else:
        print("✅ RAG corpus directory already exists")
    
    return True

def start_server():
    """Start the FastAPI server."""
    print("🚀 Starting EA Chatbot server...")
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "ea_chatbot:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main startup function."""
    print("🏗️  EA Chatbot Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Check environment
    if not check_environment():
        return 1
    
    # Setup RAG corpus
    if not setup_rag_corpus():
        return 1
    
    # Generate mock data
    if not generate_mock_data():
        return 1
    
    print("\n🎯 Starting chatbot server...")
    print("📱 Open http://localhost:8000/frontend/index.html in your browser")
    print("🔌 API available at http://localhost:8000")
    print("📖 API docs at http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    
    # Start server
    return start_server()

if __name__ == "__main__":
    sys.exit(main())
