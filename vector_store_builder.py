import json
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import pandas as pd
from typing import List, Dict, Any
import logging
from pathlib import Path
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EAVectorStoreBuilder:
    """Builds and manages the vector store for EA chatbot RAG system."""
    
    def __init__(self, 
                 corpus_dir: str = "./rag_corpus",
                 vector_db_dir: str = "./vector_db",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        """Initialize the vector store builder."""
        self.corpus_dir = Path(corpus_dir)
        self.vector_db_dir = Path(vector_db_dir)
        self.embedding_model = embedding_model
        
        # Create directories if they don't exist
        self.vector_db_dir.mkdir(exist_ok=True)
        
        # Initialize the embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.vector_db_dir),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name="ea_corpus",
            metadata={"description": "Enterprise Architecture Knowledge Base"}
        )
        
        logger.info("Vector store builder initialized successfully")
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text for better embedding quality."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove markdown formatting
        text = re.sub(r'#+\s*', '', text)  # Remove headers
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)  # Remove italic
        text = re.sub(r'`(.*?)`', r'\1', text)  # Remove code
        
        # Clean up bullet points
        text = re.sub(r'^\s*[-*]\s*', '', text, flags=re.MULTILINE)
        
        # Remove empty lines
        text = re.sub(r'\n\s*\n', '\n', text)
        
        return text.strip()
    
    def chunk_text(self, text: str, chunk_size: int = 500, 
                   overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks for better retrieval."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # If this isn't the last chunk, try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                search_start = max(start, end - 100)
                search_text = text[search_start:end]
                
                # Find the last sentence ending
                sentence_endings = ['.', '!', '?', '\n\n']
                last_ending = -1
                for ending in sentence_endings:
                    pos = search_text.rfind(ending)
                    if pos > last_ending:
                        last_ending = pos
                
                if last_ending != -1:
                    end = search_start + last_ending + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position, accounting for overlap
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def process_markdown_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Process a markdown file and extract structured content."""
        logger.info(f"Processing file: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clean the text
            cleaned_content = self.clean_text(content)
            
            # Split into chunks
            chunks = self.chunk_text(cleaned_content)
            
            # Create document chunks with metadata
            documents = []
            for i, chunk in enumerate(chunks):
                doc = {
                    "content": chunk,
                    "metadata": {
                        "source": file_path.name,
                        "chunk_id": i,
                        "total_chunks": len(chunks),
                        "file_path": str(file_path),
                        "document_type": "corpus_document"
                    }
                }
                documents.append(doc)
            
            logger.info(f"Created {len(chunks)} chunks from {file_path.name}")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return []
    
    def build_vector_store(self) -> None:
        """Build the complete vector store from all corpus documents."""
        logger.info("Starting vector store construction...")
        
        # Get all markdown files in the corpus directory
        markdown_files = list(self.corpus_dir.glob("*.md"))
        
        if not markdown_files:
            logger.warning(f"No markdown files found in {self.corpus_dir}")
            return
        
        logger.info(f"Found {len(markdown_files)} markdown files")
        
        # Process all documents
        all_documents = []
        for file_path in markdown_files:
            documents = self.process_markdown_file(file_path)
            all_documents.extend(documents)
        
        if not all_documents:
            logger.error("No documents were processed successfully")
            return
        
        logger.info(f"Total document chunks: {len(all_documents)}")
        
        # Prepare data for ChromaDB
        documents = [doc["content"] for doc in all_documents]
        metadatas = [doc["metadata"] for doc in all_documents]
        ids = [f"{doc['metadata']['source']}_{doc['metadata']['chunk_id']}" 
               for doc in all_documents]
        
        # Add documents to the collection
        logger.info("Adding documents to vector store...")
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Successfully added {len(documents)} document chunks")
        
        # Create a summary of the vector store
        self._create_vector_store_summary(all_documents)
    
    def _create_vector_store_summary(self, documents: List[Dict[str, Any]]) -> None:
        """Create a summary of the vector store contents."""
        summary = {
            "total_chunks": len(documents),
            "sources": list(set(doc["metadata"]["source"] for doc in documents)),
            "total_characters": sum(len(doc["content"]) for doc in documents),
            "average_chunk_size": (sum(len(doc["content"]) for doc in documents) 
                                 / len(documents)),
            "build_timestamp": pd.Timestamp.now().isoformat()
        }
        
        # Save summary
        summary_path = self.vector_db_dir / "vector_store_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Vector store summary saved to {summary_path}")
        logger.info(f"Summary: {summary}")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search the vector store for relevant documents."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results["documents"][0])):
            result = {
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": (results["distances"][0][i] 
                           if "distances" in results else None)
            }
            formatted_results.append(result)
        
        return formatted_results
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the vector store collection."""
        count = self.collection.count()
        
        info = {
            "collection_name": self.collection.name,
            "total_documents": count,
            "collection_metadata": self.collection.metadata
        }
        
        return info
    
    def reset_collection(self) -> None:
        """Reset the collection (remove all documents)."""
        logger.warning("Resetting vector store collection...")
        self.client.delete_collection(name=self.collection.name)
        self.collection = self.client.create_collection(
            name="ea_corpus",
            metadata={"description": "Enterprise Architecture Knowledge Base"}
        )
        logger.info("Vector store collection reset successfully")


def main():
    """Main function to build the vector store."""
    print("Building EA Chatbot Vector Store...")
    print("=" * 50)
    
    # Initialize the vector store builder
    builder = EAVectorStoreBuilder()
    
    # Build the vector store
    builder.build_vector_store()
    
    # Display collection information
    info = builder.get_collection_info()
    print(f"\nVector Store Information:")
    print(f"Collection: {info['collection_name']}")
    print(f"Total Documents: {info['total_documents']}")
    print(f"Metadata: {info['collection_metadata']}")
    
    # Test search functionality
    print(f"\nTesting search functionality...")
    test_query = "What are the key principles of enterprise architecture?"
    results = builder.search(test_query, n_results=3)
    
    print(f"\nSearch Results for: '{test_query}'")
    print("-" * 50)
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Source: {result['metadata']['source']}")
        print(f"Content: {result['content'][:200]}...")
        if result['distance']:
            print(f"Distance: {result['distance']:.4f}")
    
    print(f"\nVector store construction completed successfully!")
    print(f"Vector database location: {builder.vector_db_dir}")


if __name__ == "__main__":
    main()
