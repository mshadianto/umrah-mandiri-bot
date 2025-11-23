# -*- coding: utf-8 -*-
"""Chat API - Clean Version"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    agent: str
    query: str

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Simple chat with keyword matching"""
    try:
        query = request.message.lower()
        
        # Keyword responses
        if "ihram" in query or "miqat" in query:
            response = """IHRAM & MIQAT

Ihram adalah niat untuk melaksanakan umrah dengan memakai pakaian ihram.

Langkah:
1. Mandi (sunnah)
2. Pakai pakaian ihram (putih untuk laki-laki)
3. Sholat sunnah 2 rakaat
4. Niat: Labbaika Allahumma umratan
5. Ucapkan talbiyah

Miqat adalah batas tempat untuk niat ihram."""

        elif "thawaf" in query or "tawaf" in query:
            response = """TATA CARA THAWAF

Thawaf adalah mengelilingi Kabah 7 putaran.

Langkah:
1. Mulai dari Hajar Aswad
2. Kabah di sebelah kiri
3. 7 putaran lengkap
4. Ramal (3 putaran pertama, laki-laki cepat)
5. Sentuh Rukun Yamani jika bisa
6. Sholat 2 rakaat di Maqam Ibrahim

Durasi: 40-60 menit"""

        elif "sai" in query or "safa" in query or "marwa" in query:
            response = """TATA CARA SAI

Sai adalah berjalan antara Safa dan Marwa 7 kali.

Langkah:
1. Mulai dari Safa
2. Berjalan ke Marwa (1x)
3. Kembali ke Safa (2x)
4. Total 7x, berakhir di Marwa
5. Laki-laki lari kecil di area lampu hijau

Boleh istirahat. Dzikir sepanjang jalan.

Durasi: 45-90 menit"""

        elif "tahalul" in query or "potong rambut" in query:
            response = """TAHALUL

Tahalul adalah memotong atau mencukur rambut.

Pilihan:
1. Halaq: Mencukur gundul (laki-laki, lebih utama)
2. Taqshir: Memotong rambat pendek (boleh laki-laki & wanita)

Perempuan: Potong ujung rambat 1-2 cm
Laki-laki: Gundul atau potong rata

Setelah tahalul: Umrah selesai!"""

        elif "doa" in query or "dzikir" in query:
            response = """DOA & DZIKIR UMRAH

Talbiyah (saat ihram):
Labbaika Allahumma labbaik

Doa Thawaf:
Rabbana atina fid dunya hasanah wa fil akhirati hasanah

Doa Multazam:
Berdoa apa saja dengan khusyuk

Doa Minum Zamzam:
Allahumma inni asaluka ilman nafia

Boleh berdoa dengan bahasa sendiri!"""

        elif "rukun" in query or "wajib" in query:
            response = """RUKUN & WAJIB UMRAH

RUKUN (tidak bisa diganti):
1. Ihram
2. Thawaf 7 putaran
3. Sai 7 kali
4. Tahalul

WAJIB (jika ditinggal bayar dam):
1. Ihram dari miqat
2. Tertib (urutan rukun)

SUNNAH:
1. Mandi sebelum ihram
2. Sholat 2 rakaat
3. Ramal
4. Istilam Hajar Aswad"""

        else:
            response = f"""Terima kasih atas pertanyaan: {request.message}

Topik yang bisa saya bantu:
- Ihram & Miqat
- Tata cara Thawaf
- Tata cara Sai
- Tahalul
- Doa & Dzikir
- Rukun & Wajib

Contoh: Jelaskan cara thawaf"""
        
        return ChatResponse(
            response=response,
            agent="Keyword Assistant",
            query=request.message
        )
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "chat"}
