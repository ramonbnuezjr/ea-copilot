#!/usr/bin/env python3
"""
FastAPI Backend for EA Chatbot RAG System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our RAG system
from vector_store_builder import EAVectorStoreBuilder
import google.generativeai as genai

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# Initialize FastAPI app
app = FastAPI(
    title="EA Chatbot API",
    description="Enterprise Architecture Chatbot with RAG + AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vector store
vector_store = EAVectorStoreBuilder()

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    n_results: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    search_results: List[Dict[str, Any]]

class HealthResponse(BaseModel):
    status: str
    vector_store_info: Dict[str, Any]
    gemini_status: str

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "EA Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "System health and status",
            "/query": "Query the RAG system",
            "/search": "Search vector store only",
            "/docs": "API documentation"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check system health and status."""
    try:
        # Get vector store info
        vector_info = vector_store.get_collection_info()
        
        # Check Gemini status
        gemini_status = "Available" if model else "Not configured"
        
        return HealthResponse(
            status="healthy",
            vector_store_info=vector_info,
            gemini_status=gemini_status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system with a question.
    Returns AI-generated response based on retrieved documents.
    """
    try:
        # Search vector store
        search_results = vector_store.search(request.query, n_results=request.n_results)
        
        if not search_results:
            return QueryResponse(
                answer="I couldn't find any relevant information in our knowledge base for your question.",
                sources=[],
                confidence=0.0,
                search_results=[]
            )
        
        # Generate AI response using Gemini
        if model:
            answer = await generate_gemini_response(request.query, search_results)
        else:
            answer = generate_fallback_response(request.query, search_results)
        
        # Calculate confidence based on search relevance
        confidence = calculate_confidence(search_results)
        
        # Extract source names
        sources = [result["metadata"]["source"] for result in search_results]
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            search_results=search_results
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.post("/search")
async def search_only(request: QueryRequest):
    """
    Search the vector store only (no AI response generation).
    Returns raw search results.
    """
    try:
        search_results = vector_store.search(request.query, n_results=request.n_results)
        
        # Format results for frontend
        formatted_results = []
        for result in search_results:
            formatted_results.append({
                "content": result["content"],
                "metadata": result["metadata"],
                "distance": result.get("distance", None)
            })
        
        return {
            "query": request.query,
            "results": formatted_results,
            "total_results": len(formatted_results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

async def generate_gemini_response(query: str, search_results: List[Dict[str, Any]]) -> str:
    """Generate AI response using Gemini."""
    try:
        # Prepare context from search results
        context_parts = []
        for i, result in enumerate(search_results, 1):
            source = result["metadata"]["source"]
            doc_type = result["metadata"]["document_type"]
            content = result["content"][:500]  # Limit content length
            
            context_parts.append(f"Source {i}: {source} ({doc_type})\nContent: {content}")
        
        context = "\n\n".join(context_parts)
        
        # Create prompt for Gemini
        prompt = f"""
        You are an Enterprise Architecture expert. Answer the following question based on the provided context from our knowledge base.

        Question: {query}

        Context from our knowledge base:
        {context}

        Please provide a comprehensive, professional response that:
        1. Directly answers the question
        2. References specific sources when appropriate
        3. Provides actionable insights and recommendations
        4. Maintains a professional, enterprise-level tone
        5. Synthesizes information from multiple sources when relevant

        Response:
        """
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Error generating Gemini response: {str(e)}")
        # Fallback to basic response generation
        return generate_fallback_response(query, search_results)

def generate_fallback_response(query: str, search_results: List[Dict[str, Any]]) -> str:
    """Generate a fallback response when Gemini is not available."""
    
    # Group by document type
    by_type = {}
    for result in search_results:
        doc_type = result["metadata"]["document_type"]
        if doc_type not in by_type:
            by_type[doc_type] = []
        by_type[doc_type].append(result)
    
    response = f"Based on our Enterprise Architecture knowledge base, here's what I found about '{query}':\n\n"
    
    # Add insights from each document type
    if 'pdf_document' in by_type:
        response += "**From ServiceNow Documentation:**\n"
        for result in by_type['pdf_document']:
            source = result["metadata"]["source"]
            content = result["content"][:200] + "..."
            response += f"• {source}: {content}\n\n"
    
    if 'corpus_document' in by_type:
        response += "**From Our EA Framework:**\n"
        for result in by_type['corpus_document']:
            source = result["metadata"]["source"]
            content = result["content"][:200] + "..."
            response += f"• {source}: {content}\n\n"
    
    response += "\n**Key Insights:**\n"
    response += "• Multiple relevant sources were found across our knowledge base\n"
    response += "• Information spans both vendor documentation and our custom framework\n"
    response += "• This gives us a comprehensive view of best practices\n\n"
    
    response += "**Recommendations:**\n"
    response += "• Consider both ServiceNow best practices and our internal standards\n"
    response += "• Evaluate alignment with our business objectives\n"
    response += "• Document any architectural decisions using our ADR framework"
    
    return response

def calculate_confidence(search_results: List[Dict[str, Any]]) -> float:
    """Calculate confidence score based on search results."""
    if not search_results:
        return 0.0
    
    # Base confidence on number of results and relevance
    base_confidence = min(len(search_results) / 5.0, 1.0)  # More results = higher confidence
    
    # Adjust based on distance scores if available
    if search_results[0].get("distance") is not None:
        # Lower distance = higher relevance = higher confidence
        avg_distance = sum(r.get("distance", 0) for r in search_results) / len(search_results)
        distance_factor = max(0, 1 - avg_distance)  # Normalize distance to 0-1
        base_confidence = (base_confidence + distance_factor) / 2
    
    return round(base_confidence, 2)

if __name__ == "__main__":
    print("Starting EA Chatbot API...")
    print(f"Gemini API: {'Available' if model else 'Not configured'}")
    print("API will be available at: http://localhost:8000")
    print("Frontend can connect to: http://localhost:8000/query")
    
    uvicorn.run(
        "backend_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
