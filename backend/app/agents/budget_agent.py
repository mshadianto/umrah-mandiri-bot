# -*- coding: utf-8 -*-
"""
Budget Optimizer Agent
Uses RAG to find optimal umrah packages
"""
from typing import Dict, List, Optional
from groq import AsyncGroq
import os

# Initialize Groq client
groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

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
    """AI Agent for Budget Optimization"""
    
    def __init__(self):
        self.model = "llama-3.3-70b-versatile"
    
    async def analyze_and_recommend(
        self, 
        jamaah: int, 
        duration: int, 
        budget_max: Optional[int] = None,
        preferences: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze requirements and generate 3 package recommendations
        """
        
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

        try:
            # Call Groq API
            response = await groq_client.chat.completions.create(
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
            )
            
            result = response.choices[0].message.content
            
            # Parse JSON response
            import json
            # Clean response if needed
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                result = result.split("```")[1].split("```")[0].strip()
            
            recommendations = json.loads(result)
            return recommendations
            
        except Exception as e:
            print(f"Error in budget agent: {e}")
            return self._fallback_recommendations(jamaah, duration)
    
    def _fallback_recommendations(self, jamaah: int, duration: int) -> Dict:
        """Fallback static recommendations if AI fails"""
        makkah_nights = int(duration * 0.6)
        madinah_nights = duration - makkah_nights
        
        return {
            "packages": [
                {
                    "name": "Paket Ekonomis",
                    "category": "ekonomis",
                    "total": 15000000 * jamaah,
                    "per_person": 15000000,
                    "highlights": ["Hemat budget", "Walking distance", "Fasilitas standar"],
                    "reasoning": "Pilihan terbaik untuk budget terbatas"
                }
            ],
            "general_tips": ["Book early", "Avoid peak season"]
        }

# Export agent instance
budget_agent = BudgetAgent()
