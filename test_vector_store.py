#!/usr/bin/env python3
"""
Test script for the EA Chatbot Vector Store
"""

from vector_store_builder import EAVectorStoreBuilder

def test_vector_store():
    """Test the vector store functionality."""
    print("Testing EA Chatbot Vector Store...")
    print("=" * 50)
    
    # Initialize the vector store builder
    builder = EAVectorStoreBuilder()
    
    # Get collection info
    info = builder.get_collection_info()
    print(f"Collection: {info['collection_name']}")
    print(f"Total Documents: {info['total_documents']}")
    print(f"Metadata: {info['collection_metadata']}")
    
    # Test various search queries
    test_queries = [
        "What are the key principles of enterprise architecture?",
        "How do I manage technical debt?",
        "What are the best practices for API design?",
        "How do I implement data governance?",
        "What is the process for vendor management?",
        "How do I create architecture decision records?",
        "What are the technology standards?",
        "How do I map business capabilities?",
        "What are the cost optimization strategies?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing Query: '{query}'")
        print("-" * 60)
        
        results = builder.search(query, n_results=3)
        
        for j, result in enumerate(results, 1):
            print(f"\n  Result {j}:")
            print(f"  Source: {result['metadata']['source']}")
            print(f"  Content: {result['content'][:150]}...")
            if result['distance']:
                print(f"  Distance: {result['distance']:.4f}")
    
    print(f"\nVector store testing completed successfully!")

if __name__ == "__main__":
    test_vector_store()
