import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from config import Config

# Initialize FastAPI app
app = FastAPI(title="EA Chatbot", description="Enterprise Architecture Chatbot with RAG")

# Initialize Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel(Config.GEMINI_MODEL)

# Initialize sentence transformer for embeddings
embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path=Config.CHROMA_PERSIST_DIRECTORY)
collection = chroma_client.get_or_create_collection(
    name="ea_documents",
    metadata={"hnsw:space": "cosine"}
)

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    confidence: float

class EAChatbot:
    """Enterprise Architecture Chatbot with RAG capabilities."""
    
    def __init__(self):
        self.config = Config()
        self.load_mock_data()
        self.setup_rag_corpus()
    
    def load_mock_data(self):
        """Load mock datasets for context."""
        self.mock_data = {}
        mock_data_dir = self.config.MOCK_DATA_DIR
        
        if os.path.exists(mock_data_dir):
            for filename in os.listdir(mock_data_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(mock_data_dir, filename), 'r') as f:
                        dataset_name = filename.replace('.json', '')
                        self.mock_data[dataset_name] = json.load(f)
    
    def setup_rag_corpus(self):
        """Set up RAG corpus with documents and embeddings."""
        corpus_dir = "./rag_corpus"
        if not os.path.exists(corpus_dir):
            return
        
        # Load and embed documents
        for filename in os.listdir(corpus_dir):
            if filename.endswith('.md'):
                with open(os.path.join(corpus_dir, filename), 'r') as f:
                    content = f.read()
                    # Create chunks for better retrieval
                    chunks = self.chunk_document(content, filename)
                    for i, chunk in enumerate(chunks):
                        doc_id = f"{filename}_{i}"
                        collection.add(
                            documents=[chunk],
                            metadatas=[{"source": filename, "chunk": i}],
                            ids=[doc_id]
                        )
    
    def chunk_document(self, content: str, filename: str, chunk_size: int = 500) -> List[str]:
        """Split document into chunks for better retrieval."""
        words = content.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks
    
    def retrieve_relevant_context(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve relevant context using vector similarity search."""
        # Generate query embedding
        query_embedding = embedding_model.encode([query])
        
        # Search in vector store
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        if results['documents']:
            return results['documents'][0]
        return []
    
    def get_mock_data_context(self, query: str) -> str:
        """Get relevant mock data context based on query."""
        context_parts = []
        
        # Simple keyword matching for mock data
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['app', 'application', 'system']):
            if 'application_inventory' in self.mock_data:
                apps = self.mock_data['application_inventory'][:3]
                context_parts.append(f"Application Inventory: {json.dumps(apps, indent=2)}")
        
        if any(word in query_lower for word in ['capability', 'business']):
            if 'business_capabilities' in self.mock_data:
                caps = self.mock_data['business_capabilities'][:3]
                context_parts.append(f"Business Capabilities: {json.dumps(caps, indent=2)}")
        
        if any(word in query_lower for word in ['tech', 'technology', 'standard']):
            if 'tech_standards' in self.mock_data:
                standards = self.mock_data['tech_standards'][:3]
                context_parts.append(f"Tech Standards: {json.dumps(standards, indent=2)}")
        
        if any(word in query_lower for word in ['cost', 'license', 'vendor']):
            if 'cost_licensing' in self.mock_data:
                costs = self.mock_data['cost_licensing'][:3]
                context_parts.append(f"Cost & Licensing: {json.dumps(costs, indent=2)}")
        
        return "\n\n".join(context_parts)
    
    def generate_response(self, query: str, context: List[str], mock_context: str) -> str:
        """Generate response using Gemini with RAG context."""
        # Construct prompt with context
        prompt = f"""
        You are an Enterprise Architecture expert chatbot. Answer the user's question based on the provided context and knowledge.

        User Question: {query}

        Relevant Documentation Context:
        {'\n\n'.join(context) if context else 'No specific documentation found.'}

        Mock Data Context:
        {mock_context if mock_context else 'No specific data found.'}

        Instructions:
        1. Answer the question based on the provided context
        2. If the context doesn't fully answer the question, provide general EA best practices
        3. Always cite sources when possible
        4. Be concise but informative
        5. Focus on practical, actionable advice

        Response:
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error generating a response. Please try rephrasing your question. Error: {str(e)}"
    
    def chat(self, message: str) -> ChatResponse:
        """Main chat method that orchestrates RAG and response generation."""
        # Retrieve relevant context
        context = self.retrieve_relevant_context(message)
        
        # Get mock data context
        mock_context = self.get_mock_data_context(message)
        
        # Generate response
        response = self.generate_response(message, context, mock_context)
        
        # Extract sources
        sources = [ctx[:100] + "..." if len(ctx) > 100 else ctx for ctx in context[:3]]
        
        # Calculate confidence (simple heuristic)
        confidence = min(0.9, 0.5 + (len(context) * 0.1))
        
        return ChatResponse(
            response=response,
            sources=sources,
            confidence=confidence
        )

# Initialize chatbot
chatbot = EAChatbot()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint for the EA chatbot."""
    try:
        response = chatbot.chat(request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "EA Chatbot"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
