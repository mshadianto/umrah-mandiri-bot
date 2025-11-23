# -*- coding: utf-8 -*-
"""
Free Prayer Times Service
Uses: api.aladhan.com (FREE, no API key!)
"""
import httpx
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FreePrayerTimesService:
    """
    Free prayer times using Aladhan API
    NO API KEY NEEDED!
    """
    
    def __init__(self):
        self.base_url = "https://api.aladhan.com/v1"
    
    async def get_prayer_times(
        self,
        latitude: float,
        longitude: float,
        date: datetime = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get prayer times for location
        FREE API - no key needed!
        """
        if not date:
            date = datetime.now()
        
        timestamp = int(date.timestamp())
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/timings/{timestamp}",
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "method": 4  # Umm Al-Qura (Makkah)
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("code") == 200:
                        timings = data["data"]["timings"]
                        
                        return {
                            "date": data["data"]["date"]["readable"],
                            "hijri": data["data"]["date"]["hijri"],
                            "fajr": timings.get("Fajr"),
                            "sunrise": timings.get("Sunrise"),
                            "dhuhr": timings.get("Dhuhr"),
                            "asr": timings.get("Asr"),
                            "maghrib": timings.get("Maghrib"),
                            "isha": timings.get("Isha"),
                            "method": "Umm Al-Qura University, Makkah"
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching prayer times: {e}")
            return self._fallback_times()
    
    def _fallback_times(self) -> Dict[str, Any]:
        """Fallback prayer times for Makkah"""
        return {
            "date": datetime.now().strftime("%d %b %Y"),
            "fajr": "05:00",
            "sunrise": "06:20",
            "dhuhr": "12:30",
            "asr": "15:45",
            "maghrib": "18:15",
            "isha": "19:45",
            "method": "Approximate times for Makkah",
            "note": "Times may vary, please check local mosque"
        }

# Global instance
prayer_times_service = FreePrayerTimesService()