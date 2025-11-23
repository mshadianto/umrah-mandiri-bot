# -*- coding: utf-8 -*-
"""
AI Service with Smart Fallback
Primary: Groq (FREE!)
Fallback: OpenAI (if needed)
"""
from typing import Optional, List, Dict, Any
import httpx
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class AIService:
    """
    Smart AI service with automatic fallback
    Primary: Groq (fast & free!)
    Fallback: OpenAI (if Groq fails)
    """
    
    def __init__(self):
        self.groq_key = settings.GROQ_API_KEY
        self.openai_key = getattr(settings, 'OPENAI_API_KEY', None)
        
        # Groq config (PRIMARY)
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.groq_model = "llama3-70b-8192"  # Best free model
        
        # OpenAI config (FALLBACK)
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.openai_model = "gpt-3.5-turbo"  # Cheapest
        
        self.timeout = 30.0
        
    async def generate(
        self,
        query: str,
        system_prompt: str = None,
        context: str = None
    ) -> Dict[str, Any]:
        """
        Generate response with smart routing
        
        Returns:
            {
                "response": str,
                "model": str,
                "provider": str,
                "tokens": int
            }
        """
        
        # Build system prompt
        if not system_prompt:
            system_prompt = self._default_umrah_prompt(context)
        
        # Try Groq first (PRIMARY - FREE!)
        if self.groq_key and self.groq_key != "your-groq-key-here":
            result = await self._call_groq(query, system_prompt)
            if result:
                logger.info("✅ Used Groq (FREE)")
                return result
        
        # Fallback to OpenAI (if configured)
        if self.openai_key and self.openai_key != "your-openai-key-here":
            result = await self._call_openai(query, system_prompt)
            if result:
                logger.warning("⚠️ Used OpenAI fallback (PAID)")
                return result
        
        # Last resort: keyword-based fallback
        logger.warning("⚠️ Using keyword fallback (no API)")
        return self._keyword_fallback(query)
    
    async def _call_groq(self, query: str, system_prompt: str) -> Optional[Dict]:
        """Call Groq API (PRIMARY - FREE!)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.groq_url,
                    headers={
                        "Authorization": f"Bearer {self.groq_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.groq_model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": query}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1024,
                        "top_p": 1
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "response": data["choices"][0]["message"]["content"],
                        "model": self.groq_model,
                        "provider": "Groq (FREE)",
                        "tokens": data.get("usage", {}).get("total_tokens", 0)
                    }
                else:
                    logger.warning(f"Groq API error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Groq error: {e}")
            return None
    
    async def _call_openai(self, query: str, system_prompt: str) -> Optional[Dict]:
        """Call OpenAI API (FALLBACK - PAID!)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.openai_url,
                    headers={
                        "Authorization": f"Bearer {self.openai_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.openai_model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": query}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1024
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "response": data["choices"][0]["message"]["content"],
                        "model": self.openai_model,
                        "provider": "OpenAI (PAID)",
                        "tokens": data.get("usage", {}).get("total_tokens", 0)
                    }
                else:
                    logger.warning(f"OpenAI API error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return None
    
    def _keyword_fallback(self, query: str) -> Dict[str, Any]:
        """Keyword-based fallback (NO API NEEDED)"""
        query_lower = query.lower()
        
        responses = {
            "ihram": """**Ihram**

Ihram adalah niat untuk melaksanakan umrah dengan memakai pakaian ihram dari miqat.

**Langkah:**
1. Mandi (sunnah)
2. Pakai pakaian ihram (putih untuk laki-laki)
3. Sholat sunnah 2 rakaat
4. Niat: "Labbaika Allahumma 'umratan"
5. Ucapkan talbiyah

💡 Aktifkan Groq AI (gratis!) untuk jawaban lebih detail.""",

            "thawaf": """**Thawaf**

Mengelilingi Ka'bah 7 putaran berlawanan arah jarum jam.

**Rukun:**
1. Niat
2. 7 putaran lengkap
3. Ka'bah di sebelah kiri
4. Mulai & akhiri di Hajar Aswad
5. Sholat 2 rakaat di Maqam Ibrahim

💡 Aktifkan Groq AI untuk panduan lengkap.""",

            "sai": """**Sa'i**

Berjalan antara Safa dan Marwa 7 kali.

**Detail:**
- Mulai dari Safa, akhiri di Marwa
- Laki-laki lari kecil di lampu hijau
- Boleh istirahat
- Dzikir & doa sepanjang jalan

💡 Aktifkan Groq AI untuk doa-doa sa'i."""
        }
        
        # Find matching keyword
        for keyword, response in responses.items():
            if keyword in query_lower:
                return {
                    "response": response,
                    "model": "keyword-matching",
                    "provider": "Fallback",
                    "tokens": 0
                }
        
        # Default
        return {
            "response": f"""Maaf, sistem AI belum diaktifkan.

Untuk pertanyaan: "{query}"

**Cara Aktifkan AI (GRATIS!):**
1. Daftar di https://console.groq.com
2. Dapatkan API key (gratis!)
3. Tambahkan ke .env: GROQ_API_KEY=your_key
4. Restart backend

Atau gunakan menu untuk topik umum.""",
            "model": "none",
            "provider": "None",
            "tokens": 0
        }
    
    def _default_umrah_prompt(self, context: str = None) -> str:
        """Default system prompt for umrah"""
        base_prompt = """Anda adalah asisten AI ahli dalam panduan umrah dan fiqih Islam.

**Tugas:**
1. Berikan jawaban akurat berdasarkan Al-Quran, Hadits Shahih, dan ulama
2. Jawaban dalam Bahasa Indonesia yang jelas dan mudah dipahami
3. Praktis dan aplikatif untuk jamaah umrah
4. Sertakan dalil jika relevan
5. Jika tidak yakin, katakan dengan jelas

**Gaya:**
- Ramah dan supportif
- Tidak menghakimi
- Fokus pada kemudahan
- Respect perbedaan pendapat ulama"""

        if context:
            base_prompt += f"\n\n**Konteks relevan:**\n{context}"
        
        return base_prompt

# Global instance
ai_service = AIService()