# -*- coding: utf-8 -*-
"""
LLM Service for RAG Generation
"""
from typing import List, Dict, Any
from openai import OpenAI
from anthropic import Anthropic
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """LLM service for generating responses"""
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        if provider == "openai":
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = "gpt-4-turbo-preview"
        elif provider == "anthropic":
            self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = "claude-3-sonnet-20240229"
    
    async def generate(
        self, 
        query: str, 
        context_docs: List[Dict[str, Any]],
        system_prompt: str = None
    ) -> str:
        """Generate response using RAG"""
        try:
            # Build context from retrieved documents
            context = self._build_context(context_docs)
            
            # Default system prompt
            if not system_prompt:
                system_prompt = """Anda adalah asisten AI untuk panduan umrah yang ahli dalam fiqih Islam, manasik umrah, dan praktik ibadah. 
                
Tugas Anda:
1. Berikan jawaban yang akurat berdasarkan Al-Quran, Hadits, dan pendapat ulama
2. Gunakan konteks yang diberikan untuk menjawab
3. Jika tidak yakin, katakan "Saya tidak memiliki informasi yang cukup"
4. Berikan jawaban dalam Bahasa Indonesia yang jelas
5. Sertakan dalil jika relevan
6. Bersikap ramah dan membantu

Konteks dari knowledge base:
{context}
"""
            
            # Format prompt with context
            formatted_system = system_prompt.format(context=context)
            
            # Generate with OpenAI
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": formatted_system},
                        {"role": "user", "content": query}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content
            
            # Generate with Anthropic
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    system=formatted_system,
                    messages=[
                        {"role": "user", "content": query}
                    ]
                )
                return response.content[0].text
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Maaf, terjadi kesalahan dalam menghasilkan jawaban."
    
    def _build_context(self, docs: List[Dict[str, Any]]) -> str:
        """Build context string from documents"""
        if not docs:
            return "Tidak ada konteks yang ditemukan."
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            text = doc.get("text", "")
            metadata = doc.get("metadata", {})
            source = metadata.get("source", "Unknown")
            
            context_parts.append(f"[Dokumen {i} - {source}]\n{text}\n")
        
        return "\n".join(context_parts)