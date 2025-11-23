# -*- coding: utf-8 -*-
"""
RAG Retriever with Re-ranking
"""
from typing import List, Dict, Any
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
import logging

logger = logging.getLogger(__name__)

class RAGRetriever:
    """RAG retriever with semantic search"""
    
    def __init__(self):
        self.embeddings = EmbeddingService()
        self.vector_store = VectorStore()
    
    async def retrieve(
        self, 
        query: str, 
        top_k: int = 5,
        category: str = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for query"""
        try:
            # Generate query embedding
            query_vector = await self.embeddings.embed_query(query)
            
            # Search vector store
            filter_dict = {"category": category} if category else None
            results = await self.vector_store.search(
                query_vector=query_vector,
                limit=top_k,
                filter_dict=filter_dict
            )
            
            logger.info(f"Retrieved {len(results)} documents for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    async def retrieve_with_rerank(
        self, 
        query: str, 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve and rerank documents"""
        # First retrieve more documents
        initial_results = await self.retrieve(query, top_k=top_k * 2)
        
        # Simple reranking based on score (can be enhanced with Cohere Rerank)
        reranked = sorted(initial_results, key=lambda x: x["score"], reverse=True)
        
        return reranked[:top_k]