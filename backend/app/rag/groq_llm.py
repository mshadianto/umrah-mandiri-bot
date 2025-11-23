# -*- coding: utf-8 -*-
"""
Groq LLM Service - FREE & FAST!
Get API key from: https://console.groq.com
"""
from typing import List, Dict, Any
from groq import Groq
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class GroqLLMService:
    """
    Groq LLM service - FREE tier available!
    Models: llama3-8b-8192, llama3-70b-8192, mixtral-8x7b-32768
    """
    
    def __init__(self):
        if not settings.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY not set, using fallback responses")
            self.client = None
        else:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        
        # FREE models available on Groq
        self.model = "llama3-70b-8192"  # Best free model
        # Alternatives:
        # - llama3-8b-8192 (faster, lighter)
        # - mixtral-8x7b-32768 (good for long context)
    
    async def generate(
        self, 
        query: str, 
        context_docs: List[Dict[str, Any]] = None,
        system_prompt: str = None
    ) -> str:
        """
        Generate response using Groq
        
        Args:
            query: User's query
            context_docs: Retrieved documents from RAG
            system_prompt: Custom system prompt
        
        Returns:
            Generated response text
        """
        if not self.client:
            return self._fallback_response(query)
        
        try:
            # Build context from retrieved documents
            context = self._build_context(context_docs) if context_docs else ""
            
            # Default system prompt for umrah
            if not system_prompt:
                system_prompt = f"""Anda adalah asisten AI ahli dalam panduan umrah dan fiqih Islam.

Tugas Anda:
1. Berikan jawaban akurat berdasarkan Al-Quran, Hadits Shahih, dan pendapat ulama
2. Gunakan konteks yang diberikan untuk menjawab
3. Jika tidak yakin, katakan "Saya tidak memiliki informasi yang cukup"
4. Berikan jawaban dalam Bahasa Indonesia yang jelas dan mudah dipahami
5. Sertakan dalil jika relevan

{f'Konteks dari knowledge base:{context}' if context else ''}

Jawab dengan ramah, informatif, dan praktis."""
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            response = chat_completion.choices[0].message.content
            logger.info(f"Generated response using Groq {self.model}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return self._fallback_response(query)
    
    def _build_context(self, docs: List[Dict[str, Any]]) -> str:
        """Build context string from documents"""
        if not docs:
            return ""
        
        context_parts = []
        for i, doc in enumerate(docs[:3], 1):  # Max 3 docs
            text = doc.get("text", "")
            source = doc.get("metadata", {}).get("source", "Unknown")
            context_parts.append(f"\n[Sumber {i}: {source}]\n{text}")
        
        return "\n".join(context_parts)
    
    def _fallback_response(self, query: str) -> str:
        """Fallback response when API not available"""
        return f"""Maaf, sistem AI sedang tidak tersedia.

Untuk pertanyaan: "{query}"

Silakan:
1. Gunakan menu panduan untuk topik umum
2. Hubungi ustadz atau travel agent Anda
3. Coba lagi nanti

Untuk mendapatkan jawaban AI yang lengkap, admin perlu mengaktifkan Groq API key (gratis di console.groq.com).
"""

# Global instance
groq_llm = GroqLLMService()