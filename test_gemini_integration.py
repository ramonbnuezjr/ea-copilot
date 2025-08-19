#!/usr/bin/env python3
"""
Test script for Gemini API integration
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai


def test_gemini_connection():
    """Test basic Gemini API connection."""
    print("Testing Gemini API Integration...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False
    
    print("✅ API Key loaded successfully")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # List available models first
        print("🔄 Checking available models...")
        models = genai.list_models()
        print(f"Available models: {[model.name for model in models]}")
        
        # Use gemini-1.5-flash instead of gemini-pro
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("🔄 Testing Gemini API with simple prompt...")
        
        response = model.generate_content(
            "Hello! Please respond with 'Gemini API is working correctly.'"
        )
        
        if response.text:
            print(f"✅ Gemini API Response: {response.text}")
            return True
        else:
            print("❌ No response received from Gemini")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini API: {str(e)}")
        return False


def test_gemini_with_ea_context():
    """Test Gemini with EA-specific context."""
    print("\n" + "=" * 50)
    print("Testing Gemini with EA Context...")
    print("=" * 50)
    
    try:
        # Configure Gemini
        load_dotenv()
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test with EA-specific prompt
        ea_prompt = """
        You are an Enterprise Architecture expert. Based on your knowledge, 
        what are the top 3 principles for managing technical debt in an organization?
        
        Please provide a brief, practical response.
        """
        
        print("🔄 Testing Gemini with EA expertise...")
        response = model.generate_content(ea_prompt)
        
        if response.text:
            print("✅ EA Expert Response:")
            print(response.text)
            return True
        else:
            print("❌ No response received")
            return False
            
    except Exception as e:
        print(f"❌ Error testing EA context: {str(e)}")
        return False


def test_gemini_response_quality():
    """Test the quality and consistency of Gemini responses."""
    print("\n" + "=" * 50)
    print("Testing Response Quality...")
    print("=" * 50)
    
    try:
        # Configure Gemini
        load_dotenv()
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test multiple prompts to check consistency
        test_prompts = [
            "What is the difference between a standard and tolerate technology status?",
            "How do you calculate technical debt risk score?",
            "What are the key components of a business capability map?"
        ]
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n🔄 Test {i}: {prompt}")
            response = model.generate_content(prompt)
            
            if response.text:
                print(f"✅ Response length: {len(response.text)} characters")
                print(f"✅ First 100 chars: {response.text[:100]}...")
            else:
                print("❌ No response")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing response quality: {str(e)}")
        return False


def main():
    """Run all Gemini integration tests."""
    print("🚀 Gemini API Integration Test Suite")
    print("=" * 60)
    
    # Test basic connection
    connection_ok = test_gemini_connection()
    
    if connection_ok:
        # Test EA context
        ea_context_ok = test_gemini_with_ea_context()
        
        # Test response quality
        quality_ok = test_gemini_response_quality()
        
        # Summary
        print("\n" + "=" * 60)
        print("🎯 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ API Connection: {'PASS' if connection_ok else 'FAIL'}")
        print(f"✅ EA Context: {'PASS' if ea_context_ok else 'FAIL'}")
        print(f"✅ Response Quality: {'PASS' if quality_ok else 'FAIL'}")
        
        if all([connection_ok, ea_context_ok, quality_ok]):
            print("\n🎉 All tests passed! Gemini integration is working correctly.")
            print("Ready to proceed with RAG + AI chatbot development.")
        else:
            print("\n⚠️  Some tests failed. Please check the errors above.")
    else:
        print("\n❌ Basic connection failed. Cannot proceed with other tests.")


if __name__ == "__main__":
    main()
