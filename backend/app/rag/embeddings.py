# -*- coding: utf-8 -*-
"""
Embedding Service for RAG
"""
from typing import List
from openai import OpenAI
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating embeddings"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"
        self.dimension = 1536
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for single text"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    async def embed_query(self, query: str) -> List[float]:
        """Generate embedding for search query"""
        return await self.embed_text(query)