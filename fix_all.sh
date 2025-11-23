#!/bin/bash
echo "í´§ FIXING ALL ENDPOINTS..."
echo ""

# ============================================================================
# STEP 1: CREATE MISSING ROUTER FILES
# ============================================================================

cd backend/app/api/v1

echo "í³ Creating chat.py..."
cat > chat.py << 'PYTHON_EOF'
# -*- coding: utf-8 -*-
"""Chat API - Working Version"""
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
    """Simple chat endpoint with keyword matching"""
    try:
        logger.info(f"Chat from {request.user_id}: {request.message[:30]}...")
        
        query = request.message.lower()
        
        # Keyword matching responses
        if any(word in query for word in ['ihram', 'miqat']):
            response = """**IHRAM & MIQAT**

**Ihram** adalah niat untuk melaksanakan umrah dengan memakai pakaian ihram.

**Langkah:**
1. Mandi (sunnah)
2. Pakai pakaian ihram (putih untuk laki-laki)
3. Sholat sunnah 2 rakaat
4. Niat: "Labbaika Allahumma 'umratan"
5. Ucapkan talbiyah: "Labbaika Allahumma labbaik..."

**Miqat** adalah batas tempat untuk niat ihram. Untuk jamaah dari Indonesia biasanya di **Bir Ali** (jalur udara).

í²¡ Larangan dalam ihram: memotong kuku, mencukur rambut, memakai wewangian, berburu."""

        elif any(word in query for word in ['thawaf', 'tawaf', 'thoaf']):
            response = """**TATA CARA THAWAF**

**Thawaf** adalah mengelilingi Ka'bah 7 putaran berlawanan arah jarum jam.

**Langkah:**
1. Mulai dari Hajar Aswad (istilam/cium/tunjuk)
2. Ka'bah berada di sebelah kiri
3. 7 putaran lengkap
4. 3 putaran pertama: **ramal** (laki-laki berjalan cepat)
5. Sentuh **Rukun Yamani** jika memungkinkan
6. Baca doa antara Rukun Yamani & Hajar Aswad:
   "Rabbana atina fid dunya hasanah wa fil akhirati hasanah wa qina 'adzaban nar"
7. Selesai 7 putaran, sholat 2 rakaat di **Maqam Ibrahim**

â±ï¸ Durasi: 40-60 menit (tergantung keramaian)"""

        elif any(word in query for word in ['sai', "sa'i", 'safa', 'marwa']):
            response = """**TATA CARA SA'I**

**Sa'i** adalah berjalan/berlari kecil antara bukit Safa dan Marwa sebanyak 7 kali.

**Langkah:**
1. Mulai dari **Safa** (naik sampai lihat Ka'bah)
2. Baca doa & berdzikir
3. Turun dan berjalan ke **Marwa** (ini 1x)
4. Di antara lampu hijau: **lari kecil** (laki-laki)
5. Sampai Marwa, naik dan hadap Ka'bah
6. Kembali ke Safa (ini 2x)
7. Ulangi sampai 7x, berakhir di **Marwa**

**Tips:**
- Boleh istirahat di tengah
- Perempuan jalan biasa (tidak lari)
- Dzikir & doa sepanjang jalan
- Minum zamzam setelah sa'i

â±ï¸ Durasi: 45-90 menit
í³ Jarak: ~450m x 7 = 3.1 km"""

        elif any(word in query for word in ['tahalul', 'tahallul', 'gundul', 'potong rambut']):
            response = """**TAHALUL (TAHALLUL)**

**Tahalul** adalah memotong atau mencukur rambut sebagai tanda selesainya umrah.

**Pilihan:**
1. **Halaq**: Mencukur gundul (laki-laki, lebih utama)
2. **Taqshir**: Memotong rambut pendek (boleh laki-laki & wanita)

**Ketentuan:**
- Laki-laki: Minimal gundul atau potong rata seluruh kepala
- Perempuan: Potong ujung rambut sepanjang ujung jari (Â±1-2 cm)
- Dilakukan setelah sa'i selesai
- Banyak tempat potong rambut di sekitar Haram

**Setelah tahalul:**
âœ… Umrah selesai!
âœ… Semua larangan ihram sudah terbuka
âœ… Boleh memakai wewangian, potong kuku, dll"""

        elif any(word in query for word in ['doa', 'dzikir', 'bacaan']):
            response = """**DOA & DZIKIR UMRAH**

**Talbiyah (saat ihram):**
"Labbaika Allahumma labbaik, labbaika la syarika laka labbaik. Innal hamda wan ni'mata laka wal mulk, la syarika lak"

**Doa Thawaf:**
Antara Rukun Yamani & Hajar Aswad:
"Rabbana atina fid dunya hasanah wa fil akhirati hasanah wa qina 'adzaban nar"

**Doa di Multazam:**
Tempat mustajab antara Hajar Aswad & pintu Ka'bah. Berdoa apa saja dengan khusyuk.

**Doa Minum Zamzam:**
"Allahumma inni as'aluka 'ilman nafi'an wa rizqan wasi'an wa syifa'an min kulli da'"

**Doa Sa'i:**
"Innash shafa wal marwata min sya'airillah"

í²¡ Boleh berdoa dengan bahasa sendiri, yang penting dari hati!"""

        elif any(word in query for word in ['rukun', 'wajib', 'sunnah']):
            response = """**RUKUN, WAJIB & SUNNAH UMRAH**

**RUKUN UMRAH (Wajib, tidak bisa diganti):**
1. âœ… Ihram (niat & pakaian ihram)
2. âœ… Thawaf 7 putaran
3. âœ… Sa'i 7 kali
4. âœ… Tahalul (gundul/potong rambut)

**WAJIB UMRAH (wajib, jika ditinggal bayar dam):**
1. Ihram dari miqat
2. Tertib (urutan rukun)

**SUNNAH UMRAH:**
1. Mandi sebelum ihram
2. Sholat 2 rakaat sebelum ihram
3. Ramal (3 putaran pertama thawaf)
4. Idhtiba' (membuka bahu kanan saat thawaf)
5. Istilam Hajar Aswad
6. Sentuh Rukun Yamani
7. Minum zamzam
8. Thawaf wada' (perpisahan)

**Jika tertinggal rukun:** Umrah tidak sah
**Jika tertinggal wajib:** Bayar dam (potong kambing)
**Jika tertinggal sunnah:** Tidak masalah, tapi kurang sempurna"""

        else:
            response = f"""Terima kasih atas pertanyaan Anda tentang: "{request.message}"

**Topik yang bisa saya bantu:**
- Ihram & Miqat
- Tata cara Thawaf
- Tata cara Sa'i
- Tahalul (potong rambut)
- Doa & Dzikir
- Rukun, Wajib, Sunnah

**Contoh pertanyaan:**
- "Jelaskan cara thawaf"
- "Apa saja rukun umrah?"
- "Doa ketika sa'i"

Silakan tanya dengan kata kunci di atas! íµ‹"""
        
        return ChatResponse(
            response=response,
            agent="Keyword Assistant",
            query=request.message
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "chat"}
PYTHON_EOF

echo "âœ… chat.py created!"

# ============================================================================
# CREATE ADVANCED.PY
# ============================================================================

echo "í³ Creating advanced.py..."
cat > advanced.py << 'PYTHON_EOF'
# -*- coding: utf-8 -*-
"""Advanced Features API - Working Version"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class PrayerTimeRequest(BaseModel):
    location: str = "Makkah"
    date: Optional[datetime] = None

@router.post("/prayer-times")
async def prayer_times(request: PrayerTimeRequest):
    """Prayer times endpoint"""
    try:
        logger.info(f"Prayer times request for {request.location}")
        
        # Simple static times for now
        response_text = f"""íµŒ **Jadwal Sholat - {request.location.title()}**
í³… {datetime.now().strftime('%A, %d %B %Y')}

â° **Waktu Sholat:**
- Subuh: 05:00 âœ¨
- Terbit: 06:20 í¼…
- Dzuhur: 12:30 â˜€ï¸
- Ashar: 15:45 í¼¤ï¸
- Maghrib: 18:15 í¼†
- Isya: 19:45 í¼™

í³ Lokasi: {request.location.title()}
í³Š Metode: Umm Al-Qura, Makkah

í²¡ **Tips:**
- Sholat 15 menit setelah adzan lebih afdhal
- Cek jadwal di hotel untuk waktu yang akurat
- Gunakan app Muslim Pro untuk alarm

_Waktu approximate untuk Makkah_"""
        
        return {
            "agent": "Prayer Times",
            "response": response_text
        }
        
    except Exception as e:
        logger.error(f"Prayer times error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/navigation")
async def navigation(request: dict):
    """Navigation endpoint"""
    try:
        query = request.get("query", "").lower()
        
        if "hotel" in query:
            response = """í¿¨ **Hotel Dekat Masjidil Haram**

**Walking Distance (<5 min):**
â­â­â­â­â­
- Fairmont Makkah Clock Royal Tower
- Swissotel Makkah  
- Pullman ZamZam Makkah

â­â­â­â­
- Hilton Suites Makkah
- Anjum Hotel Makkah
- Elaf Kinda Hotel

í²¡ **Tips Memilih:**
- Semakin dekat = semakin mahal
- Cek view Ka'bah
- Baca review jamaah Indonesia
- Pastikan ada lift (penting!)"""
        
        elif "makan" in query:
            response = """í½½ï¸ **Tempat Makan Dekat Haram**

**Restoran:**
- Al Baik (Fast food lokal, murah & enak!)
- Hardee's, KFC, Pizza Hut
- Kudu (Saudi cuisine)

**Food Court:**
- Abraj Al Bait Mall (basement)
- Makkah Mall

**Supermarket (paling hemat!):**
- Al Othaim, Carrefour, Panda

í²° **Budget:**
- Meal murah: 15-25 SAR
- Meal sedang: 30-50 SAR"""
        
        else:
            response = """í·ºï¸ **Navigasi Makkah**

**Lokasi Penting:**
- íµ‹ Masjidil Haram (Ka'bah)
- â›°ï¸ Jabal Rahmah (Arafah) - 20km
- í¿”ï¸ Gua Hira - 4km
- íµŒ Mina - 7km

**Jarak dalam Haram:**
- Safa ke Marwa: ~450m
- 1x thawaf: ~450m
- 7x thawaf: ~3.1km

Tanya spesifik: "hotel terdekat" atau "tempat makan""""
        
        return {
            "agent": "Navigation",
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Navigation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/emergency")
async def emergency(request: dict):
    """Emergency endpoint"""
    try:
        emerg_type = request.get("type", "general")
        
        if emerg_type == "medical":
            response = """íº¨ **DARURAT MEDIS**

**HUBUNGI:**
1. Ambulans: **997**
2. Hotel reception untuk bantuan

**RUMAH SAKIT:**
- Ajyad Hospital: +966 12 549 8000
- King Abdullah Medical City: +966 12 549 5555

**APOTEK 24 JAM:**
- Nahdi Pharmacy (Abraj Al Bait)

í·®í·© **KJRI Jeddah:**
- Normal: +966 12 667 0080
- Emergency: +966 50 521 5066"""
        
        else:
            response = """í¶˜ **KONTAK DARURAT**

**EMERGENCY:**
- Polisi: **911**
- Ambulans: **997**
- Pemadam: **998**

í·®í·© **KJRI Jeddah:**
- Telpon: +966 12 667 0080
- Emergency: +966 50 521 5066

Ketik "darurat medis" untuk info kesehatan"""
        
        return {
            "agent": "Emergency",
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Emergency error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tips/{category}")
async def tips(category: str):
    """Tips endpoint"""
    tips_db = {
        "thawaf": [
            "Waktu terbaik: 1-3 pagi (paling sepi)",
            "Gunakan lantai atas jika ramai",
            "Bawa air minum sendiri",
            "Fokus ibadah, kurangi foto"
        ],
        "sai": [
            "Area lari: antara lampu hijau",
            "Perempuan jalan biasa (tidak lari)",
            "Boleh istirahat di tengah",
            "Minum zamzam setelah sa'i"
        ],
        "budget": [
            "Supermarket lebih hemat",
            "Al Baik: fast food murah",
            "Bawa tumbler untuk zamzam",
            "Naik bus hotel (gratis)"
        ]
    }
    
    return {
        "category": category,
        "tips": tips_db.get(category, ["Tips tidak ditemukan"])
    }

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "advanced"}
PYTHON_EOF

echo "âœ… advanced.py created!"

# ============================================================================
# VERIFY FILES
# ============================================================================

echo ""
echo "í³‹ Verifying files..."
ls -lh chat.py advanced.py

echo ""
echo "âœ… ALL FILES CREATED!"
echo ""
echo "Next: Restart backend with: uvicorn app.main:app --reload"
