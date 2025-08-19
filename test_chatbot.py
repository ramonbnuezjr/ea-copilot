#!/usr/bin/env python3
"""
Test script for EA Chatbot
Tests basic functionality without requiring the full server
"""

import os
import sys
import json

def test_mock_data_generation():
    """Test mock data generation."""
    print("🧪 Testing mock data generation...")
    
    try:
        from mock_data_generator import EAMockDataGenerator
        
        # Test with temporary directory
        test_dir = "./test_mock_data"
        generator = EAMockDataGenerator(test_dir)
        
        # Generate all datasets
        datasets = generator.generate_all_data()
        
        # Verify datasets were created
        expected_datasets = [
            "business_capabilities", "application_inventory", "tech_standards",
            "integration_catalog", "tech_debt", "roadmap", "cost_licensing",
            "sla_health", "security_controls", "data_domains", 
            "vendor_contracts", "adrs"
        ]
        
        for dataset_name in expected_datasets:
            json_file = os.path.join(test_dir, f"{dataset_name}.json")
            csv_file = os.path.join(test_dir, f"{dataset_name}.csv")
            
            if not os.path.exists(json_file):
                print(f"❌ Missing JSON file: {json_file}")
                return False
            
            if not os.path.exists(csv_file):
                print(f"❌ Missing CSV file: {csv_file}")
                return False
        
        print("✅ Mock data generation test passed")
        
        # Clean up test directory
        import shutil
        shutil.rmtree(test_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Mock data generation test failed: {e}")
        return False

def test_config_loading():
    """Test configuration loading."""
    print("🧪 Testing configuration loading...")
    
    try:
        from config import Config
        
        config = Config()
        
        # Check required attributes
        required_attrs = [
            'GEMINI_API_KEY', 'GEMINI_MODEL', 'CHROMA_PERSIST_DIRECTORY',
            'EMBEDDING_MODEL', 'TOP_K_RESULTS', 'SIMILARITY_THRESHOLD',
            'MOCK_DATA_DIR', 'HOST', 'PORT', 'DEBUG'
        ]
        
        for attr in required_attrs:
            if not hasattr(config, attr):
                print(f"❌ Missing config attribute: {attr}")
                return False
        
        print("✅ Configuration loading test passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading test failed: {e}")
        return False

def test_rag_corpus():
    """Test RAG corpus setup."""
    print("🧪 Testing RAG corpus...")
    
    try:
        corpus_dir = "./rag_corpus"
        
        # Check if corpus directory exists
        if not os.path.exists(corpus_dir):
            print(f"❌ RAG corpus directory not found: {corpus_dir}")
            return False
        
        # Check for required documents
        required_docs = ["ea_principles.md", "nfr_checklist.md"]
        
        for doc in required_docs:
            doc_path = os.path.join(corpus_dir, doc)
            if not os.path.exists(doc_path):
                print(f"❌ Required document not found: {doc}")
                return False
        
        print("✅ RAG corpus test passed")
        return True
        
    except Exception as e:
        print(f"❌ RAG corpus test failed: {e}")
        return False

def test_frontend():
    """Test frontend files."""
    print("🧪 Testing frontend...")
    
    try:
        frontend_dir = "./frontend"
        
        if not os.path.exists(frontend_dir):
            print(f"❌ Frontend directory not found: {frontend_dir}")
            return False
        
        index_file = os.path.join(frontend_dir, "index.html")
        if not os.path.exists(index_file):
            print(f"❌ Frontend index file not found: {index_file}")
            return False
        
        # Check if HTML file contains required elements
        with open(index_file, 'r') as f:
            content = f.read()
            
        required_elements = [
            "EA Chatbot", "Enterprise Architecture Assistant", 
            "chat-messages", "message-input", "chat-form"
        ]
        
        for element in required_elements:
            if element not in content:
                print(f"❌ Required element not found in HTML: {element}")
                return False
        
        print("✅ Frontend test passed")
        return True
        
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🏗️  EA Chatbot Test Suite")
    print("=" * 50)
    
    tests = [
        test_config_loading,
        test_rag_corpus,
        test_frontend,
        test_mock_data_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("📊 Test Results")
    print("=" * 50)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! The EA Chatbot is ready to use.")
        print("\nNext steps:")
        print("1. Set your GEMINI_API_KEY in a .env file")
        print("2. Run: python start_chatbot.py")
        print("3. Open http://localhost:8000/frontend/index.html")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
