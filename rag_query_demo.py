#!/usr/bin/env python3
"""
RAG Query Demo for EA Chatbot
Demonstrates how the vector store will be used for retrieval
"""

from vector_store_builder import EAVectorStoreBuilder
import json

class RAGQueryDemo:
    """Demo class for RAG query functionality."""
    
    def __init__(self):
        """Initialize the RAG demo."""
        self.vector_store = EAVectorStoreBuilder()
        
    def query_rag(self, question: str, n_results: int = 3) -> dict:
        """
        Query the RAG system with a question.
        
        Args:
            question: The user's question
            n_results: Number of relevant documents to retrieve
            
        Returns:
            Dictionary with question, retrieved documents, and response
        """
        # Retrieve relevant documents from vector store
        retrieved_docs = self.vector_store.search(question, n_results=n_results)
        
        # Format the response
        response = {
            "question": question,
            "retrieved_documents": retrieved_docs,
            "total_documents_found": len(retrieved_docs),
            "response_summary": self._generate_response_summary(question, retrieved_docs)
        }
        
        return response
    
    def _generate_response_summary(self, question: str, docs: list) -> str:
        """
        Generate a summary response based on retrieved documents.
        
        Args:
            question: The original question
            docs: Retrieved relevant documents
            
        Returns:
            Summary response string
        """
        if not docs:
            return "I couldn't find relevant information to answer your question."
        
        # Extract key information from documents
        sources = [doc['metadata']['source'] for doc in docs]
        unique_sources = list(set(sources))
        
        # Create a summary based on the question type
        if "principle" in question.lower():
            return f"Based on {len(unique_sources)} source(s), here are the key principles: {', '.join(unique_sources)}"
        elif "how" in question.lower():
            return f"I found {len(docs)} relevant sections from {len(unique_sources)} document(s) that address your question."
        elif "what" in question.lower():
            return f"Here's what I found from {len(unique_sources)} source(s) about your question."
        else:
            return f"I retrieved {len(docs)} relevant document sections from {len(unique_sources)} source(s)."
    
    def demo_queries(self):
        """Run a series of demo queries to showcase the RAG system."""
        demo_questions = [
            "What are the key principles of enterprise architecture?",
            "How do I manage technical debt effectively?",
            "What are the best practices for API design?",
            "How do I implement data governance?",
            "What is the process for vendor management?",
            "How do I create architecture decision records?",
            "What are the technology standards?",
            "How do I map business capabilities?",
            "What are the cost optimization strategies?",
            "How do I ensure compliance with GDPR?"
        ]
        
        print("EA Chatbot RAG System Demo")
        print("=" * 60)
        print("This demo shows how the RAG system retrieves relevant information")
        print("from the knowledge base to answer EA-related questions.\n")
        
        for i, question in enumerate(demo_questions, 1):
            print(f"Demo {i}: {question}")
            print("-" * 60)
            
            # Query the RAG system
            response = self.query_rag(question, n_results=2)
            
            # Display results
            print(f"Response: {response['response_summary']}")
            print(f"Documents Retrieved: {response['total_documents_found']}")
            
            for j, doc in enumerate(response['retrieved_documents'], 1):
                print(f"\n  Document {j}:")
                print(f"    Source: {doc['metadata']['source']}")
                print(f"    Content: {doc['content'][:100]}...")
                if doc['distance']:
                    print(f"    Relevance Score: {1 - doc['distance']:.3f}")
            
            print("\n" + "="*60 + "\n")
    
    def interactive_query(self):
        """Interactive query mode for testing."""
        print("Interactive RAG Query Mode")
        print("Type 'quit' to exit")
        print("-" * 40)
        
        while True:
            try:
                question = input("\nEnter your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not question:
                    continue
                
                # Query the RAG system
                response = self.query_rag(question, n_results=3)
                
                # Display results
                print(f"\nResponse: {response['response_summary']}")
                print(f"Documents Retrieved: {response['total_documents_found']}")
                
                for i, doc in enumerate(response['retrieved_documents'], 1):
                    print(f"\nDocument {i}:")
                    print(f"  Source: {doc['metadata']['source']}")
                    print(f"  Content: {doc['content'][:150]}...")
                    if doc['distance']:
                        relevance = 1 - doc['distance']
                        print(f"  Relevance: {relevance:.3f}")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    """Main function to run the RAG demo."""
    demo = RAGQueryDemo()
    
    print("Choose demo mode:")
    print("1. Run all demo queries")
    print("2. Interactive query mode")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        demo.demo_queries()
    elif choice == "2":
        demo.interactive_query()
    else:
        print("Invalid choice. Running demo queries...")
        demo.demo_queries()

if __name__ == "__main__":
    main()
