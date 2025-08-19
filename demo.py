#!/usr/bin/env python3
"""
EA Chatbot Demo Script
Demonstrates the chatbot capabilities with sample queries
"""

import os
import sys

def print_header():
    """Print demo header."""
    print("🏗️  EA Chatbot Demo")
    print("=" * 60)
    print("Enterprise Architecture Assistant powered by RAG + Gemini")
    print("=" * 60)

def print_sample_queries():
    """Print sample queries for demonstration."""
    print("\n📝 Sample Queries You Can Try:")
    print("-" * 40)
    
    queries = [
        "What applications support Customer Onboarding?",
        "Is Kubernetes a standard technology?",
        "Which vendors are up for renewal this quarter?",
        "What are our high-priority tech debt items?",
        "What business capabilities are core vs. supporting?",
        "Which systems have security risks?",
        "What is our total annual SaaS spend?",
        "Which technologies should we retire?",
        "What integrations support our CRM system?",
        "How mature are our business capabilities?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"{i:2d}. {query}")
    
    print("\n💡 These queries demonstrate the chatbot's ability to:")
    print("   • Map applications to business capabilities")
    print("   • Provide technology standards guidance")
    print("   • Analyze vendor contracts and renewals")
    print("   • Assess technical debt and risks")
    print("   • Give strategic architecture advice")

def print_mock_data_overview():
    """Print overview of available mock data."""
    print("\n📊 Available Mock Data:")
    print("-" * 30)
    
    data_sources = [
        ("Business Capabilities", "8 core and supporting capabilities"),
        ("Application Inventory", "6 applications with mappings"),
        ("Tech Standards", "10 technologies with status"),
        ("Integration Catalog", "5 system integrations"),
        ("Tech Debt Register", "5 debt items with priorities"),
        ("Roadmap", "4 strategic initiatives"),
        ("Cost & Licensing", "5 vendor contracts"),
        ("SLA Health", "5 service metrics"),
        ("Security Controls", "5 compliance frameworks"),
        ("Data Domains", "5 data classifications"),
        ("Vendor Contracts", "5 supplier relationships"),
        ("Architecture Decisions", "4 ADRs with outcomes")
    ]
    
    for source, description in data_sources:
        print(f"• {source:<20} - {description}")

def print_rag_corpus_info():
    """Print information about the RAG corpus."""
    print("\n📚 RAG Knowledge Corpus:")
    print("-" * 30)
    
    documents = [
        ("EA Principles", "Core architecture principles and governance"),
        ("NFR Checklist", "Non-functional requirements framework"),
        ("Security Baseline", "PII protection and compliance guidelines")
    ]
    
    for doc, description in documents:
        print(f"• {doc:<20} - {description}")

def print_quick_start():
    """Print quick start instructions."""
    print("\n🚀 Quick Start:")
    print("-" * 20)
    print("1. Set your Gemini API key:")
    print("   export GEMINI_API_KEY='your_key_here'")
    print("   # or create a .env file")
    print()
    print("2. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("3. Start the chatbot:")
    print("   python start_chatbot.py")
    print()
    print("4. Open in browser:")
    print("   http://localhost:8000/frontend/index.html")

def print_architecture_info():
    """Print architecture information."""
    print("\n🏗️  Architecture:")
    print("-" * 20)
    print("• Frontend: Modern HTML/JS with Tailwind CSS")
    print("• Backend: FastAPI with async support")
    print("• AI: Google Gemini Pro for reasoning")
    print("• Vector Store: ChromaDB for RAG")
    print("• Embeddings: Sentence Transformers")
    print("• Data: Realistic mock datasets")

def main():
    """Run the demo."""
    print_header()
    
    print_sample_queries()
    print_mock_data_overview()
    print_rag_corpus_info()
    print_architecture_info()
    print_quick_start()
    
    print("\n" + "=" * 60)
    print("🎯 Ready to build your Enterprise Architecture chatbot!")
    print("=" * 60)

if __name__ == "__main__":
    main()
