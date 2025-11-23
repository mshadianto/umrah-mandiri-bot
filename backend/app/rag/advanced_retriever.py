# -*- coding: utf-8 -*-
"""
Advanced RAG Retriever with Hybrid Search
"""
from typing import List, Dict, Any, Optional
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
import logging

logger = logging.getLogger(__name__)

class AdvancedRAGRetriever:
    """Advanced RAG with hybrid search, re-ranking, and context awareness"""
    
    def __init__(self):
        self.embeddings = EmbeddingService()
        self.vector_store = VectorStore()
        self.cache = {}  # Simple cache
    
    async def retrieve_with_context(
        self,
        query: str,
        user_context: Dict[str, Any],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve with user context awareness
        
        Args:
            query: User's query
            user_context: User profile, history, preferences
            top_k: Number of results
        
        Returns:
            List of relevant documents with scores
        """
        try:
            # Check cache
            cache_key = f"{query}_{user_context.get('language', 'id')}"
            if cache_key in self.cache:
                logger.info("Cache hit for query")
                return self.cache[cache_key]
            
            # Expand query with context
            expanded_query = self._expand_query(query, user_context)
            
            # Generate embedding
            query_vector = await self.embeddings.embed_query(expanded_query)
            
            # Determine category filter
            category = self._determine_category(query)
            filter_dict = {"category": category} if category else None
            
            # Search
            results = await self.vector_store.search(
                query_vector=query_vector,
                limit=top_k * 2,  # Get more for reranking
                filter_dict=filter_dict
            )
            
            # Rerank based on relevance and user preference
            reranked = self._rerank_results(results, query, user_context)
            
            # Cache results
            self.cache[cache_key] = reranked[:top_k]
            
            logger.info(f"Retrieved {len(reranked)} documents")
            return reranked[:top_k]
            
        except Exception as e:
            logger.error(f"Error in advanced retrieval: {e}")
            return []
    
    def _expand_query(self, query: str, context: Dict[str, Any]) -> str:
        """Expand query with user context"""
        expanded = query
        
        # Add language context
        lang = context.get("language", "id")
        if lang == "ar":
            expanded += " في العربية"
        
        # Add location context if relevant
        location = context.get("location")
        if location and any(word in query.lower() for word in ['hotel', 'tempat', 'lokasi']):
            expanded += f" dekat {location}"
        
        return expanded
    
    def _determine_category(self, query: str) -> Optional[str]:
        """Determine content category from query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['doa', 'dzikir', 'bacaan']):
            return "doa"
        elif any(word in query_lower for word in ['biaya', 'harga', 'budget']):
            return "budget"
        elif any(word in query_lower for word in ['hotel', 'lokasi', 'tempat']):
            return "location"
        elif any(word in query_lower for word in ['manasik', 'rukun', 'wajib', 'sunnah']):
            return "manasik"
        
        return None
    
    def _rerank_results(
        self,
        results: List[Dict[str, Any]],
        query: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Rerank results based on multiple factors"""
        
        # Simple reranking: boost based on user preferences
        preferences = context.get("preferences", {})
        preferred_sources = preferences.get("preferred_sources", [])
        
        def calculate_score(result):
            base_score = result["score"]
            
            # Boost if from preferred source
            source = result.get("metadata", {}).get("source", "")
            if any(pref in source for pref in preferred_sources):
                base_score *= 1.2
            
            # Boost recent content
            # TODO: Add recency boost
            
            return base_score
        
        # Sort by adjusted score
        reranked = sorted(results, key=calculate_score, reverse=True)
        return reranked