# -*- coding: utf-8 -*-
"""
Budget Optimizer Agent
Uses RAG to find optimal umrah packages
FIXED VERSION - No circular import
"""
from typing import Dict, List, Optional
import os
import asyncio
import json
import logging

# Import Groq at the top level
try:
    from groq import AsyncGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    AsyncGroq = None

logger = logging.getLogger(__name__)

# Knowledge base - In production, this would be from vector DB
KNOWLEDGE_BASE = """
# HARGA HOTEL MAKKAH (Per Malam, Per Kamar Double)

## Bintang 3 (Walking Distance)
- Elaf Al Mashaer: Rp 600.000 (5 min walk to Haram)
- Dar Al Eiman Royal: Rp 550.000 (10 min walk)
- Al Marwa Rayhaan: Rp 650.000 (7 min walk)

## Bintang 4 (Close to Haram)
- Swissotel Makkah: Rp 1.200.000 (3 min walk)
- Anjum Hotel: Rp 1.000.000 (5 min walk)
- Makkah Towers: Rp 1.100.000 (Clock Tower view)

## Bintang 5 (Premium)
- Fairmont Makkah: Rp 2.500.000 (Direct Haram view)
- Raffles Makkah: Rp 2.200.000 (Luxury, 2 min walk)
- Conrad Makkah: Rp 2.000.000 (Premium facilities)

# HARGA HOTEL MADINAH (Per Malam, Per Kamar Double)

## Bintang 3
- Elaf Taiba: Rp 500.000 (8 min walk to Masjid Nabawi)
- Al Aqeeq Hotel: Rp 450.000 (10 min walk)
- Dar Al Taqwa: Rp 550.000 (7 min walk)

## Bintang 4
- Shaza Al Madina: Rp 900.000 (5 min walk)
- Anjum Hotel Madinah: Rp 850.000 (Front view)
- Madinah Marriott: Rp 950.000 (Premium location)

## Bintang 5
- Oberoi Madinah: Rp 1.800.000 (Luxury, direct view)
- Dar Al Iman InterContinental: Rp 1.600.000
- Millennium Al Aqeeq: Rp 1.500.000

# HARGA TIKET PESAWAT JAKARTA-JEDDAH (PP)

## Musim Reguler (Februari-Juni, September-November)
- Saudia Airlines: Rp 9.500.000 (Direct, 11 jam)
- Garuda Indonesia: Rp 10.500.000 (Direct, premium service)
- Emirates (via Dubai): Rp 8.500.000 (1 transit)
- Qatar Airways (via Doha): Rp 9.000.000 (1 transit)

## Musim Ramai (Juli-Agustus, Desember-Januari, Ramadhan)
- Saudia Airlines: Rp 12.000.000
- Garuda Indonesia: Rp 13.000.000
- Emirates: Rp 11.000.000
- Qatar Airways: Rp 11.500.000

# BIAYA LAIN-LAIN

- Visa Umrah: Rp 2.500.000 per orang
- Asuransi Perjalanan: Rp 500.000 per orang
- Transportasi Lokal (Jeddah-Makkah-Madinah): Rp 800.000 per orang
- Makan per hari: Rp 150.000-300.000 tergantung tempat
- Ziarah & Tour Optional: Rp 500.000-1.000.000
"""


class BudgetAgent:
    """AI Agent for Budget Optimization"""
    
    def __init__(self):
        self.model = "llama-3.3-70b-versatile"
        self.timeout = 25.0  # 25 second timeout
        self.groq_client = None
        
        # Initialize Groq client
        self._init_groq_client()
    
    def _init_groq_client(self):
        """Initialize Groq client separately to avoid circular imports"""
        try:
            if not GROQ_AVAILABLE:
                logger.warning("⚠️ Groq library not available")
                return
            
            GROQ_API_KEY = os.getenv("GROQ_API_KEY")
            if GROQ_API_KEY and GROQ_API_KEY != "your-groq-key-here":
                self.groq_client = AsyncGroq(api_key=GROQ_API_KEY)
                logger.info("✅ Groq client initialized successfully")
            else:
                logger.warning("⚠️ GROQ_API_KEY not configured, will use fallback")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Groq client: {e}")
    
    async def analyze_and_recommend(
        self, 
        jamaah: int, 
        duration: int, 
        budget_max: Optional[int] = None,
        preferences: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze requirements and generate 3 package recommendations
        With timeout and fallback
        """
        
        # Input validation
        if not 1 <= jamaah <= 50:
            return {
                "error": "Jumlah jamaah harus antara 1-50 orang",
                "packages": []
            }
        
        if not 5 <= duration <= 30:
            return {
                "error": "Durasi harus antara 5-30 hari",
                "packages": []
            }
        
        # If Groq not configured, use fallback immediately
        if not self.groq_client:
            logger.warning("Groq not configured, using fallback")
            return self._fallback_recommendations(jamaah, duration)
        
        try:
            # Build prompt with context
            prompt = self._build_prompt(jamaah, duration, budget_max, preferences)
            
            # Call Groq API with timeout
            logger.info(f"Calling Groq API for {jamaah} jamaah, {duration} days")
            
            response = await asyncio.wait_for(
                self.groq_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert Umrah travel budget optimizer. You analyze prices and provide optimal recommendations based on knowledge base."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=4000
                ),
                timeout=self.timeout
            )
            
            result = response.choices[0].message.content
            logger.info("✅ Received response from Groq")
            
            # Parse JSON response
            recommendations = self._parse_response(result)
            
            # Validate structure
            if not self._validate_response(recommendations):
                logger.warning("Invalid response structure, using fallback")
                return self._fallback_recommendations(jamaah, duration)
            
            return recommendations
            
        except asyncio.TimeoutError:
            logger.error(f"⏱️ Groq API timeout after {self.timeout}s")
            return self._fallback_recommendations(jamaah, duration)
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parse error: {e}")
            return self._fallback_recommendations(jamaah, duration)
            
        except Exception as e:
            logger.error(f"❌ Error in budget agent: {e}", exc_info=True)
            return self._fallback_recommendations(jamaah, duration)
    
    def _build_prompt(self, jamaah: int, duration: int, budget_max: Optional[int], preferences: Optional[Dict]) -> str:
        """Build prompt for Groq"""
        return f"""Anda adalah AI Budget Optimizer untuk umrah mandiri. Gunakan knowledge base untuk memberikan 3 rekomendasi paket umrah yang OPTIMAL.

# KNOWLEDGE BASE:
{KNOWLEDGE_BASE}

# REQUEST USER:
- Jumlah Jamaah: {jamaah} orang
- Durasi: {duration} hari (split 60% Makkah, 40% Madinah)
- Budget Maximum: {f'Rp {budget_max:,.0f}' if budget_max else 'Flexible'}
- Preferences: {preferences if preferences else 'Standard'}

# TUGAS:
Berikan 3 rekomendasi paket:
1. EKONOMIS (Paling hemat tapi tetap nyaman)
2. STANDAR (Balance antara harga & fasilitas)
3. PREMIUM (Fasilitas terbaik)

Untuk SETIAP paket, berikan:
- Nama paket & kategori
- Hotel Makkah (nama, bintang, jarak ke Haram, harga per malam)
- Hotel Madinah (nama, bintang, jarak ke Masjid Nabawi, harga per malam)
- Airlines (nama, tipe, harga)
- Total biaya detail (breakdown)
- Keunggulan paket
- Tips khusus untuk paket ini

IMPORTANT: 
- Hitung AKURAT berdasarkan jumlah jamaah & durasi
- Malam hotel = durasi - 1
- Split Makkah 60%, Madinah 40%
- Pastikan paket EKONOMIS benar-benar paling murah
- Berikan REASONING mengapa pilih hotel/airline tersebut

FORMAT OUTPUT sebagai JSON:
{{
  "packages": [
    {{
      "name": "Paket Ekonomis",
      "category": "ekonomis",
      "hotels": {{
        "makkah": {{
          "name": "...",
          "stars": 3,
          "distance": "5 min walk",
          "price_per_night": 600000,
          "nights": ...,
          "subtotal": ...
        }},
        "madinah": {{...}}
      }},
      "flight": {{
        "airline": "...",
        "type": "transit/direct",
        "price_per_person": ...,
        "subtotal": ...
      }},
      "costs": {{
        "visa": ...,
        "insurance": ...,
        "transport": ...,
        "meals": ...,
        "misc": ...
      }},
      "total": ...,
      "per_person": ...,
      "highlights": ["...", "..."],
      "reasoning": "Mengapa pilih paket ini...",
      "tips": ["...", "..."]
    }}
  ],
  "general_tips": ["...", "..."]
}}

Berikan HANYA JSON, tanpa teks tambahan."""
    
    def _parse_response(self, result: str) -> Dict:
        """Parse Groq response to JSON"""
        # Clean response if needed
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        elif "```" in result:
            result = result.split("```")[1].split("```")[0].strip()
        
        return json.loads(result)
    
    def _validate_response(self, data: Dict) -> bool:
        """Validate response structure"""
        if not isinstance(data, dict):
            return False
        
        if "packages" not in data:
            return False
        
        if not isinstance(data["packages"], list):
            return False
        
        if len(data["packages"]) < 1:
            return False
        
        # Check first package has required fields
        pkg = data["packages"][0]
        required_fields = ["name", "total", "per_person"]
        
        return all(field in pkg for field in required_fields)
    
    def _fallback_recommendations(self, jamaah: int, duration: int) -> Dict:
        """
        Fallback static recommendations if AI fails
        Calculate based on knowledge base prices
        """
        logger.info("Using fallback recommendations")
        
        makkah_nights = int(duration * 0.6)
        madinah_nights = duration - makkah_nights - 1  # -1 for travel day
        
        # Calculate costs
        visa_cost = 2500000 * jamaah
        insurance_cost = 500000 * jamaah
        transport_cost = 800000 * jamaah
        misc_cost = 500000 * jamaah
        
        packages = []
        
        # PAKET EKONOMIS
        makkah_hotel_ekonomis = 550000 * makkah_nights
        madinah_hotel_ekonomis = 450000 * madinah_nights
        flight_ekonomis = 8500000 * jamaah
        meals_ekonomis = 150000 * duration * jamaah
        
        total_ekonomis = (
            makkah_hotel_ekonomis +
            madinah_hotel_ekonomis +
            flight_ekonomis +
            visa_cost +
            insurance_cost +
            transport_cost +
            meals_ekonomis +
            misc_cost
        )
        
        packages.append({
            "name": "Paket Ekonomis",
            "category": "ekonomis",
            "hotels": {
                "makkah": {
                    "name": "Dar Al Eiman Royal",
                    "stars": 3,
                    "distance": "10 min walk",
                    "price_per_night": 550000,
                    "nights": makkah_nights,
                    "subtotal": makkah_hotel_ekonomis
                },
                "madinah": {
                    "name": "Al Aqeeq Hotel",
                    "stars": 3,
                    "distance": "10 min walk",
                    "price_per_night": 450000,
                    "nights": madinah_nights,
                    "subtotal": madinah_hotel_ekonomis
                }
            },
            "flight": {
                "airline": "Emirates via Dubai",
                "type": "1 transit",
                "price_per_person": 8500000,
                "subtotal": flight_ekonomis
            },
            "costs": {
                "visa": visa_cost,
                "insurance": insurance_cost,
                "transport": transport_cost,
                "meals": meals_ekonomis,
                "misc": misc_cost
            },
            "total": int(total_ekonomis),
            "per_person": int(total_ekonomis / jamaah),
            "highlights": [
                "Hemat budget hingga 30%",
                "Hotel walking distance dari Haram",
                "Fasilitas standar tapi nyaman"
            ],
            "reasoning": "Pilihan terbaik untuk jamaah dengan budget terbatas. Hotel bintang 3 dengan jarak walking distance, penerbangan transit untuk harga lebih ekonomis.",
            "tips": [
                "Book 3-4 bulan sebelumnya untuk harga terbaik",
                "Jalan kaki ke Haram sebagai exercise",
                "Makan di warung lokal seperti Al Baik"
            ]
        })
        
        # PAKET STANDAR
        makkah_hotel_standar = 1000000 * makkah_nights
        madinah_hotel_standar = 850000 * madinah_nights
        flight_standar = 9500000 * jamaah
        meals_standar = 200000 * duration * jamaah
        
        total_standar = (
            makkah_hotel_standar +
            madinah_hotel_standar +
            flight_standar +
            visa_cost +
            insurance_cost +
            transport_cost +
            meals_standar +
            misc_cost
        )
        
        packages.append({
            "name": "Paket Standar",
            "category": "standar",
            "hotels": {
                "makkah": {
                    "name": "Anjum Hotel Makkah",
                    "stars": 4,
                    "distance": "5 min walk",
                    "price_per_night": 1000000,
                    "nights": makkah_nights,
                    "subtotal": makkah_hotel_standar
                },
                "madinah": {
                    "name": "Anjum Hotel Madinah",
                    "stars": 4,
                    "distance": "5 min walk",
                    "price_per_night": 850000,
                    "nights": madinah_nights,
                    "subtotal": madinah_hotel_standar
                }
            },
            "flight": {
                "airline": "Saudia Airlines Direct",
                "type": "direct",
                "price_per_person": 9500000,
                "subtotal": flight_standar
            },
            "costs": {
                "visa": visa_cost,
                "insurance": insurance_cost,
                "transport": transport_cost,
                "meals": meals_standar,
                "misc": misc_cost
            },
            "total": int(total_standar),
            "per_person": int(total_standar / jamaah),
            "highlights": [
                "Balance sempurna harga & kualitas",
                "Hotel bintang 4 dekat Haram",
                "Penerbangan direct lebih nyaman"
            ],
            "reasoning": "Pilihan paling populer dengan balance optimal antara kenyamanan dan harga. Hotel bintang 4 dengan lokasi strategis, direct flight untuk kenyamanan perjalanan.",
            "tips": [
                "Pilih kamar dengan view Ka'bah",
                "Manfaatkan fasilitas hotel",
                "Kombinasi makan di hotel dan restoran lokal"
            ]
        })
        
        # PAKET PREMIUM
        makkah_hotel_premium = 2200000 * makkah_nights
        madinah_hotel_premium = 1600000 * madinah_nights
        flight_premium = 10500000 * jamaah
        meals_premium = 300000 * duration * jamaah
        
        total_premium = (
            makkah_hotel_premium +
            madinah_hotel_premium +
            flight_premium +
            visa_cost +
            insurance_cost +
            transport_cost +
            meals_premium +
            misc_cost
        )
        
        packages.append({
            "name": "Paket Premium",
            "category": "premium",
            "hotels": {
                "makkah": {
                    "name": "Raffles Makkah Palace",
                    "stars": 5,
                    "distance": "2 min walk",
                    "price_per_night": 2200000,
                    "nights": makkah_nights,
                    "subtotal": makkah_hotel_premium
                },
                "madinah": {
                    "name": "Dar Al Iman InterContinental",
                    "stars": 5,
                    "distance": "3 min walk",
                    "price_per_night": 1600000,
                    "nights": madinah_nights,
                    "subtotal": madinah_hotel_premium
                }
            },
            "flight": {
                "airline": "Garuda Indonesia Premium",
                "type": "direct",
                "price_per_person": 10500000,
                "subtotal": flight_premium
            },
            "costs": {
                "visa": visa_cost,
                "insurance": insurance_cost,
                "transport": transport_cost,
                "meals": meals_premium,
                "misc": misc_cost
            },
            "total": int(total_premium),
            "per_person": int(total_premium / jamaah),
            "highlights": [
                "Hotel bintang 5 luxury",
                "View langsung Ka'bah & Masjid Nabawi",
                "Fasilitas & service premium"
            ],
            "reasoning": "Pilihan terbaik untuk jamaah yang menginginkan kenyamanan maksimal. Hotel bintang 5 dengan view langsung, layanan premium, dan lokasi super strategis.",
            "tips": [
                "Nikmati semua fasilitas hotel",
                "Request early check-in",
                "Manfaatkan concierge service"
            ]
        })
        
        return {
            "packages": packages,
            "general_tips": [
                "Book hotel dan flight minimal 3 bulan sebelum keberangkatan",
                "Hindari musim ramai (Ramadhan, libur sekolah) untuk harga lebih murah",
                "Gunakan travel insurance untuk perlindungan maksimal",
                "Siapkan budget tambahan 10-15% untuk keperluan tak terduga"
            ],
            "note": "Fallback calculation - AI service temporarily unavailable"
        }


# Function to get agent instance (lazy initialization to avoid circular imports)
def get_budget_agent():
    """Get budget agent instance - Use this in budget_routes.py"""
    return BudgetAgent()
