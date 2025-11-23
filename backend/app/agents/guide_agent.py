# -*- coding: utf-8 -*-
"""
Guide Agent with RAG
"""
from app.agents.base_agent import BaseAgent
from app.rag.retriever import RAGRetriever
from app.rag.llm import LLMService
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class GuideAgent(BaseAgent):
    """Agent for manasik guidance with RAG"""
    
    def __init__(self):
        super().__init__(
            name="Guide Agent",
            description="Provides umrah guidance using RAG from Islamic knowledge base"
        )
        self.retriever = RAGRetriever()
        self.llm = LLMService(provider="openai")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute guide agent with RAG"""
        query = input_data.get("query")
        context = input_data.get("context", {})
        
        try:
            # Retrieve relevant documents
            docs = await self.retriever.retrieve(
                query=query,
                top_k=5,
                category="manasik"
            )
            
            # Generate response using LLM with context
            system_prompt = """Anda adalah ustadz yang ahli dalam panduan umrah dan fiqih Islam.

Berikan jawaban yang:
1. Berdasarkan Al-Quran, Hadits Shahih, dan pendapat ulama mu'tabar
2. Jelas, praktis, dan mudah dipahami
3. Menggunakan Bahasa Indonesia yang baik
4. Menyertakan dalil jika relevan
5. Ramah dan membantu

Konteks dari knowledge base:
{context}

Jika tidak ada informasi yang cukup dalam konteks, jawab berdasarkan pengetahuan umum tentang umrah yang shahih."""

            response_text = await self.llm.generate(
                query=query,
                context_docs=docs,
                system_prompt=system_prompt
            )
            
            # Build sources
            sources = [
                {
                    "text": doc["text"][:200] + "...",
                    "source": doc["metadata"].get("source", "Unknown"),
                    "score": doc["score"]
                }
                for doc in docs[:3]
            ]
            
            return {
                "agent": self.name,
                "response": response_text,
                "sources": sources,
                "query": query
            }
            
        except Exception as e:
            logger.error(f"Error in GuideAgent: {e}")
            return {
                "agent": self.name,
                "response": "Maaf, terjadi kesalahan. Silakan coba lagi.",
                "sources": [],
                "error": str(e)
            }