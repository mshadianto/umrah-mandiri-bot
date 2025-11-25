# -*- coding: utf-8 -*-
"""
Budget Optimizer Agent - IMPROVED VERSION
Uses RAG to find optimal umrah packages with better error handling
"""
from typing import Dict, List, Optional
from groq import AsyncGroq
import os
import asyncio
import logging
import json

logger = logging.getLogger(__name__)

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key or groq_api_key == "your-groq-key-here":
    logger.warning("⚠️ GROQ_API_KEY not configured! Budget agent will use fallback mode.")
    groq_client = None
else:
    groq_client = AsyncGroq(api_key=groq_api_key)
    logger.info("✅ Groq client initialized successfully")

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

# TIPS HEMAT

1. Book 3-4 bulan sebelum keberangkatan untuk harga terbaik
2. Pilih hotel 5-10 menit jalan kaki dari Haram (lebih murah, exercise bagus)
3. Makan di warung lokal (Al Baik, Kudu, local restaurants)
4. Gunakan taxi sharing atau bus untuk transportasi antar kota
5. Hindari musim ramai (harga naik 30-50%)
6. Group booking (4+ orang) dapat diskon hotel 10-15%
"""

class BudgetAgent:
    """AI Agent for Budget Optimization with improved error handling"""
    
    def __init__(self):
        self.model = "llama-3.3-70b-versatile"
        self.timeout = 25.0  # 25 seconds timeout
    
    async def analyze_and_recommend(
        self, 
        jamaah: int, 
        duration: int, 
        budget_max: Optional[int] = None,
        preferences: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze requirements and generate 3 package recommendations
        WITH IMPROVED ERROR HANDLING
        
        Args:
            jamaah: Jumlah jamaah (1-50)
            duration: Durasi perjalanan dalam hari (5-30)
            budget_max: Budget maksimum (optional)
            preferences: User preferences (optional)
            
        Returns:
            Dict with packages and general_tips
        """
        
        # Validate inputs
        if jamaah < 1 or jamaah > 50:
            logger.error(f"Invalid jamaah count: {jamaah}")
            return {
                "error": "invalid_input",
                "packages": [],
                "general_tips": ["Jumlah jamaah harus antara 1-50 orang"]
            }
        
        if duration < 5 or duration > 30:
            logger.error(f"Invalid duration: {duration}")
            return {
                "error": "invalid_input", 
                "packages": [],
                "general_tips": ["Durasi harus antara 5-30 hari"]
            }
        
        # Check if Groq client is available
        if groq_client is None:
            logger.warning("Groq client not available, using fallback")
            return self._fallback_recommendations(jamaah, duration)
        
        # Build prompt with context
        prompt = f"""Anda adalah AI Budget Optimizer untuk umrah mandiri. Gunakan knowledge base untuk memberikan 3 rekomendasi paket umrah yang OPTIMAL.

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
- Split Makkah 60%, Madinah 40% dari total malam
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
        "madinah": {{
          "name": "...",
          "stars": 3,
          "distance": "8 min walk",
          "price_per_night": 500000,
          "nights": ...,
          "subtotal": ...
        }}
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
    }},
    {{
      "name": "Paket Standar",
      "category": "standar",
      ...
    }},
    {{
      "name": "Paket Premium", 
      "category": "premium",
      ...
    }}
  ],
  "general_tips": ["...", "...", "..."]
}}

Berikan HANYA JSON yang valid, tanpa markdown atau teks tambahan."""

        try:
            logger.info(f"Calling Groq API for {jamaah} jamaah, {duration} days...")
            
            # Call Groq API with timeout
            response = await asyncio.wait_for(
                groq_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert Umrah travel budget optimizer. You analyze prices and provide optimal recommendations based on knowledge base. Always return valid JSON only."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=4000,
                    response_format={"type": "json_object"}  # Ensure JSON response
                ),
                timeout=self.timeout
            )
            
            result = response.choices[0].message.content
            logger.info(f"Got response from Groq: {len(result)} chars")
            
            # Parse JSON response
            # Clean response if needed
            result = result.strip()
            if result.startswith("```json"):
                result = result.split("```json")[1].split("```")[0].strip()
            elif result.startswith("```"):
                result = result.split("```")[1].split("```")[0].strip()
            
            recommendations = json.loads(result)
            
            # Validate response structure
            if "packages" not in recommendations:
                logger.error("Invalid response structure: missing 'packages' key")
                return self._fallback_recommendations(jamaah, duration)
            
            if len(recommendations["packages"]) < 3:
                logger.warning(f"Expected 3 packages, got {len(recommendations['packages'])}")
            
            logger.info(f"✅ Successfully generated {len(recommendations['packages'])} packages")
            return recommendations
            
        except asyncio.TimeoutError:
            logger.error(f"Groq API timeout after {self.timeout}s")
            return self._fallback_recommendations(jamaah, duration)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            logger.error(f"Raw response (first 200 chars): {result[:200] if 'result' in locals() else 'N/A'}")
            return self._fallback_recommendations(jamaah, duration)
            
        except Exception as e:
            logger.error(f"Error in budget agent: {e}", exc_info=True)
            return self._fallback_recommendations(jamaah, duration)
    
    def _fallback_recommendations(self, jamaah: int, duration: int) -> Dict:
        """
        Fallback static recommendations if AI fails
        Provides reasonable estimates based on simple calculations
        """
        logger.info("Using fallback recommendations")
        
        makkah_nights = int(duration * 0.6)
        madinah_nights = duration - 1 - makkah_nights  # -1 for travel day
        
        # Simple package calculations
        packages = []
        
        # Ekonomis
        hotel_makkah_ekonomis = 600000 * makkah_nights
        hotel_madinah_ekonomis = 500000 * madinah_nights
        flight_ekonomis = 8500000 * jamaah
        other_costs_ekonomis = (2500000 + 500000 + 800000 + (200000 * duration)) * jamaah
        total_ekonomis = hotel_makkah_ekonomis + hotel_madinah_ekonomis + flight_ekonomis + other_costs_ekonomis
        
        packages.append({
            "name": "Paket Ekonomis",
            "category": "ekonomis",
            "hotels": {
                "makkah": {
                    "name": "Elaf Al Mashaer",
                    "stars": 3,
                    "distance": "5 min walk",
                    "price_per_night": 600000,
                    "nights": makkah_nights,
                    "subtotal": hotel_makkah_ekonomis
                },
                "madinah": {
                    "name": "Elaf Taiba",
                    "stars": 3,
                    "distance": "8 min walk",
                    "price_per_night": 500000,
                    "nights": madinah_nights,
                    "subtotal": hotel_madinah_ekonomis
                }
            },
            "flight": {
                "airline": "Emirates (via Dubai)",
                "type": "transit",
                "price_per_person": 8500000,
                "subtotal": flight_ekonomis
            },
            "costs": {
                "visa": 2500000 * jamaah,
                "insurance": 500000 * jamaah,
                "transport": 800000 * jamaah,
                "meals": 200000 * duration * jamaah,
                "misc": 500000 * jamaah
            },
            "total": total_ekonomis,
            "per_person": total_ekonomis // jamaah,
            "highlights": [
                "Hemat budget tapi tetap nyaman",
                "Walking distance ke Haram",
                "Hotel bersih & fasilitas standar"
            ],
            "reasoning": "Paket ini dipilih untuk meminimalkan biaya dengan tetap menjaga kenyamanan. Hotel bintang 3 dengan jarak walkable, penerbangan transit untuk harga lebih murah.",
            "tips": [
                "Book 3-4 bulan sebelum untuk harga terbaik",
                "Makan di warung lokal seperti Al Baik",
                "Gunakan bus hotel gratis untuk transport"
            ]
        })
        
        # Standar
        hotel_makkah_standar = 1100000 * makkah_nights
        hotel_madinah_standar = 900000 * madinah_nights
        flight_standar = 9500000 * jamaah
        other_costs_standar = (2500000 + 500000 + 800000 + (250000 * duration)) * jamaah
        total_standar = hotel_makkah_standar + hotel_madinah_standar + flight_standar + other_costs_standar
        
        packages.append({
            "name": "Paket Standar",
            "category": "standar",
            "hotels": {
                "makkah": {
                    "name": "Makkah Towers",
                    "stars": 4,
                    "distance": "Clock Tower view",
                    "price_per_night": 1100000,
                    "nights": makkah_nights,
                    "subtotal": hotel_makkah_standar
                },
                "madinah": {
                    "name": "Shaza Al Madina",
                    "stars": 4,
                    "distance": "5 min walk",
                    "price_per_night": 900000,
                    "nights": madinah_nights,
                    "subtotal": hotel_madinah_standar
                }
            },
            "flight": {
                "airline": "Saudia Airlines",
                "type": "direct",
                "price_per_person": 9500000,
                "subtotal": flight_standar
            },
            "costs": {
                "visa": 2500000 * jamaah,
                "insurance": 500000 * jamaah,
                "transport": 800000 * jamaah,
                "meals": 250000 * duration * jamaah,
                "misc": 1000000 * jamaah
            },
            "total": total_standar,
            "per_person": total_standar // jamaah,
            "highlights": [
                "Balance harga & fasilitas",
                "Hotel bintang 4 nyaman",
                "Penerbangan direct lebih cepat"
            ],
            "reasoning": "Paket ini memberikan balance terbaik antara harga dan kenyamanan. Hotel bintang 4 dengan fasilitas lebih baik, penerbangan direct menghemat waktu.",
            "tips": [
                "Hotel bintang 4 lebih nyaman untuk istirahat",
                "Direct flight menghemat 3-4 jam perjalanan",
                "Suitable untuk semua umur"
            ]
        })
        
        # Premium
        hotel_makkah_premium = 2200000 * makkah_nights
        hotel_madinah_premium = 1600000 * madinah_nights
        flight_premium = 10500000 * jamaah
        other_costs_premium = (2500000 + 500000 + 800000 + (300000 * duration)) * jamaah
        total_premium = hotel_makkah_premium + hotel_madinah_premium + flight_premium + other_costs_premium
        
        packages.append({
            "name": "Paket Premium",
            "category": "premium",
            "hotels": {
                "makkah": {
                    "name": "Raffles Makkah",
                    "stars": 5,
                    "distance": "2 min walk",
                    "price_per_night": 2200000,
                    "nights": makkah_nights,
                    "subtotal": hotel_makkah_premium
                },
                "madinah": {
                    "name": "Dar Al Iman InterContinental",
                    "stars": 5,
                    "distance": "Direct view",
                    "price_per_night": 1600000,
                    "nights": madinah_nights,
                    "subtotal": hotel_madinah_premium
                }
            },
            "flight": {
                "airline": "Garuda Indonesia",
                "type": "direct",
                "price_per_person": 10500000,
                "subtotal": flight_premium
            },
            "costs": {
                "visa": 2500000 * jamaah,
                "insurance": 500000 * jamaah,
                "transport": 800000 * jamaah,
                "meals": 300000 * duration * jamaah,
                "misc": 2000000 * jamaah
            },
            "total": total_premium,
            "per_person": total_premium // jamaah,
            "highlights": [
                "Luxury experience",
                "Hotel bintang 5 sangat dekat Haram",
                "Service excellence & fasilitas premium"
            ],
            "reasoning": "Paket ini memberikan pengalaman umrah terbaik dengan hotel mewah sangat dekat ke Haram, penerbangan premium dengan service terbaik.",
            "tips": [
                "View Kabah dari kamar (request saat booking)",
                "Buffet breakfast premium disediakan",
                "Concierge service 24/7"
            ]
        })
        
        return {
            "packages": packages,
            "general_tips": [
                "Book 3-4 bulan sebelum keberangkatan untuk harga terbaik",
                "Pilih musim reguler untuk harga lebih murah (hindari Ramadan & liburan)",
                "Group booking 4+ orang dapat diskon hotel 10-15%",
                "Bawa tumbler & snack untuk hemat biaya makan",
                "Gunakan aplikasi Uber/Careem untuk transport lebih murah"
            ],
            "note": "Ini adalah estimasi fallback. Aktifkan Groq API untuk rekomendasi AI yang lebih akurat."
        }

# Export agent instance
budget_agent = BudgetAgent()
