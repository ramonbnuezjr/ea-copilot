#!/usr/bin/env python3
"""
Demo script showing PDF integration with the EA Chatbot RAG system
"""

from pdf_upload_utility import PDFUploadUtility
from vector_store_builder import EAVectorStoreBuilder
import os

def demo_pdf_integration():
    """Demonstrate PDF integration with the RAG system."""
    print("PDF Integration Demo for EA Chatbot RAG System")
    print("=" * 60)
    
    # Initialize utilities
    pdf_utility = PDFUploadUtility()
    vector_builder = EAVectorStoreBuilder()
    
    print("1. PDF Directory Status")
    print("-" * 30)
    dir_info = pdf_utility.get_directory_info()
    print(f"PDF Directory: {dir_info['directory_path']}")
    print(f"Current PDFs: {dir_info['total_files']}")
    print(f"Total Size: {dir_info['total_size_mb']} MB")
    
    # Check if there are any PDFs
    current_pdfs = pdf_utility.list_uploaded_pdfs()
    
    if current_pdfs:
        print(f"\n2. Current PDFs in System")
        print("-" * 30)
        for pdf in current_pdfs:
            print(f"  📄 {pdf['filename']} ({pdf['size_mb']} MB)")
        
        print(f"\n3. Rebuilding Vector Store with PDFs")
        print("-" * 30)
        print("Rebuilding vector store to include PDF content...")
        
        # Rebuild vector store with PDFs
        vector_builder.build_vector_store(include_pdfs=True)
        
        # Show updated collection info
        info = vector_builder.get_collection_info()
        print(f"✅ Vector store updated!")
        print(f"   Total documents: {info['total_documents']}")
        
        # Test search with PDF content
        print(f"\n4. Testing Search with PDF Content")
        print("-" * 30)
        test_queries = [
            "What are the key principles?",
            "How do I manage technical debt?",
            "What are the best practices?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: '{query}'")
            results = vector_builder.search(query, n_results=2)
            
            for i, result in enumerate(results, 1):
                doc_type = result['metadata']['document_type']
                source = result['metadata']['source']
                print(f"  Result {i}: {source} ({doc_type})")
                print(f"    Content: {result['content'][:100]}...")
    
    else:
        print(f"\n2. No PDFs Found")
        print("-" * 30)
        print("To add PDFs to your RAG system:")
        print(f"1. Place PDF files in: {dir_info['directory_path']}")
        print("2. Run this demo again to process them")
        print("3. Or use the utility methods programmatically")
        
        print(f"\nExample usage:")
        print("  # Upload a single PDF")
        print("  pdf_utility.upload_pdf('/path/to/document.pdf')")
        print("  ")
        print("  # Upload all PDFs from a directory")
        print("  pdf_utility.upload_pdfs_from_directory('/path/to/pdf/folder')")
    
    print(f"\n5. PDF Management Commands")
    print("-" * 30)
    print("Available utility methods:")
    print("  pdf_utility.upload_pdf(source_path)")
    print("  pdf_utility.upload_pdfs_from_directory(source_dir)")
    print("  pdf_utility.list_uploaded_pdfs()")
    print("  pdf_utility.remove_pdf(filename)")
    print("  pdf_utility.clear_all_pdfs()")
    
    print(f"\n6. Next Steps")
    print("-" * 30)
    print("1. Add PDFs to the pdf_documents directory")
    print("2. Run this demo again to process them")
    print("3. Your RAG system will automatically include PDF content")
    print("4. Search results will show both markdown and PDF sources")

def show_pdf_processing_info():
    """Show information about PDF processing capabilities."""
    print(f"\n📚 PDF Processing Capabilities")
    print("=" * 40)
    print("✅ Text Extraction Methods:")
    print("   • PyMuPDF (primary) - Best text extraction")
    print("   • PyPDF2 (fallback) - Standard PDF processing")
    print("   • OCR (last resort) - For image-based PDFs")
    
    print(f"\n✅ Supported Features:")
    print("   • Automatic text extraction and cleaning")
    print("   • Intelligent chunking (800 chars with 100 char overlap)")
    print("   • Metadata tracking (file size, processing method)")
    print("   • Source citation in search results")
    
    print(f"\n✅ Best Practices:")
    print("   • Use text-based PDFs for best results")
    print("   • Avoid heavily image-based PDFs")
    print("   • Keep PDFs under 50MB for processing")
    print("   • Use descriptive filenames for better organization")

if __name__ == "__main__":
    demo_pdf_integration()
    show_pdf_processing_info()
