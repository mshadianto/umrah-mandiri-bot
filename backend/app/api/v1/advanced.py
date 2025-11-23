# -*- coding: utf-8 -*-
"""Advanced Features API"""
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
        now = datetime.now()
        
        response_text = f"""Jadwal Sholat - {request.location.title()}
Tanggal: {now.strftime('%A, %d %B %Y')}

Waktu Sholat:
- Subuh: 05:00
- Terbit: 06:20
- Dzuhur: 12:30
- Ashar: 15:45
- Maghrib: 18:15
- Isya: 19:45

Lokasi: {request.location.title()}
Metode: Umm Al-Qura, Makkah

Tips:
- Sholat 15 menit setelah adzan
- Cek jadwal di hotel untuk waktu akurat

Waktu approximate untuk Makkah"""
        
        return {
            "agent": "Prayer Times",
            "response": response_text
        }
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/navigation")
async def navigation(request: dict):
    """Navigation endpoint"""
    try:
        query = request.get("query", "").lower()
        
        if "hotel" in query:
            response = """Hotel Dekat Masjidil Haram

Walking Distance (<5 min):
- Fairmont Makkah Clock Royal Tower
- Swissotel Makkah
- Pullman ZamZam Makkah

Medium Range:
- Hilton Suites Makkah
- Anjum Hotel Makkah
- Elaf Kinda Hotel

Tips Memilih:
- Semakin dekat = semakin mahal
- Cek view Kabah
- Baca review jamaah Indonesia"""
        
        elif "makan" in query:
            response = """Tempat Makan Dekat Haram

Restoran:
- Al Baik (Fast food lokal, murah!)
- Hardees, KFC, Pizza Hut
- Kudu (Saudi cuisine)

Food Court:
- Abraj Al Bait Mall
- Makkah Mall

Supermarket (hemat):
- Al Othaim
- Carrefour
- Panda

Budget:
- Meal murah: 15-25 SAR
- Meal sedang: 30-50 SAR"""
        
        else:
            response = """Navigasi Makkah

Lokasi Penting:
- Masjidil Haram (Kabah)
- Jabal Rahmah (Arafah) - 20km
- Gua Hira - 4km
- Mina - 7km

Jarak dalam Haram:
- Safa ke Marwa: 450m
- 1x thawaf: 450m
- 7x thawaf: 3.1km

Tanya: hotel terdekat atau tempat makan"""
        
        return {
            "agent": "Navigation",
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/emergency")
async def emergency(request: dict):
    """Emergency endpoint"""
    try:
        emerg_type = request.get("type", "general")
        
        if emerg_type == "medical":
            response = """DARURAT MEDIS

HUBUNGI:
1. Ambulans: 997
2. Hotel reception

RUMAH SAKIT:
- Ajyad Hospital: +966 12 549 8000
- King Abdullah Medical City: +966 12 549 5555

APOTEK 24 JAM:
- Nahdi Pharmacy (Abraj Al Bait)

KJRI Jeddah:
- Normal: +966 12 667 0080
- Emergency: +966 50 521 5066"""
        
        else:
            response = """KONTAK DARURAT

EMERGENCY:
- Polisi: 911
- Ambulans: 997
- Pemadam: 998

KJRI Jeddah:
- Telpon: +966 12 667 0080
- Emergency: +966 50 521 5066

Ketik: darurat medis untuk info kesehatan"""
        
        return {
            "agent": "Emergency",
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tips/{category}")
async def tips(category: str):
    """Tips endpoint"""
    tips_db = {
        "thawaf": [
            "Waktu terbaik: 1-3 pagi",
            "Gunakan lantai atas jika ramai",
            "Bawa air minum",
            "Fokus ibadah"
        ],
        "sai": [
            "Area lari: antara lampu hijau",
            "Perempuan jalan biasa",
            "Boleh istirahat",
            "Minum zamzam setelah sai"
        ],
        "budget": [
            "Supermarket lebih hemat",
            "Al Baik: murah & enak",
            "Bawa tumbler",
            "Naik bus hotel gratis"
        ]
    }
    
    return {
        "category": category,
        "tips": tips_db.get(category, ["Tips tidak ditemukan"])
    }

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "advanced"}
