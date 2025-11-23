# -*- coding: utf-8 -*-
"""
Doa Agent with RAG
"""
from app.agents.base_agent import BaseAgent
from app.rag.retriever import RAGRetriever
from app.rag.llm import LLMService
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DoaAgent(BaseAgent):
    """Agent for doa & dzikir with RAG"""
    
    def __init__(self):
        super().__init__(
            name="Doa Agent",
            description="Provides doa and dzikir from authentic Islamic sources"
        )
        self.retriever = RAGRetriever()
        self.llm = LLMService(provider="openai")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute doa agent"""
        query = input_data.get("query")
        
        try:
            # Retrieve doa from knowledge base
            docs = await self.retriever.retrieve(
                query=query,
                top_k=3,
                category="doa"
            )
            
            # Generate formatted response
            system_prompt = """Anda adalah specialist doa dan dzikir Islam.

Format jawaban Anda harus:
1. Teks Arab (jika ada)
2. Transliterasi Latin
3. Terjemahan Indonesia
4. Keutamaan/penjelasan
5. Sumber (hadits/riwayat jika ada)

Konteks dari knowledge base:
{context}

Berikan jawaban yang lengkap dan mudah dipraktikkan."""

            response_text = await self.llm.generate(
                query=query,
                context_docs=docs,
                system_prompt=system_prompt
            )
            
            return {
                "agent": self.name,
                "response": response_text,
                "sources": [
                    {
                        "text": doc["text"],
                        "source": doc["metadata"].get("source", "Hisnul Muslim")
                    }
                    for doc in docs
                ],
                "query": query
            }
            
        except Exception as e:
            logger.error(f"Error in DoaAgent: {e}")
            return {
                "agent": self.name,
                "response": "Maaf, doa belum tersedia dalam database.",
                "sources": []
            }