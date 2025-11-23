# -*- coding: utf-8 -*-
"""
Prayer Time Agent with Real-time Data
"""
from app.agents.base_agent import BaseAgent
from typing import Dict, Any
from datetime import datetime
import pytz
import requests
import logging

logger = logging.getLogger(__name__)

class PrayerTimeAgent(BaseAgent):
    """Agent for prayer times with real-time data"""
    
    def __init__(self):
        super().__init__(
            name="Prayer Time Agent",
            description="Provides accurate prayer times based on location"
        )
        self.api_url = "https://api.aladhan.com/v1/timings"
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get prayer times for location"""
        try:
            location = input_data.get("location", "Makkah")
            date = input_data.get("date", datetime.now())
            
            # Get coordinates
            coords = self._get_coordinates(location)
            
            # Fetch prayer times
            prayer_times = await self._fetch_prayer_times(
                coords["latitude"],
                coords["longitude"],
                date
            )
            
            # Format response
            response = self._format_prayer_times(prayer_times, location)
            
            return {
                "agent": self.name,
                "response": response,
                "data": prayer_times,
                "location": location
            }
            
        except Exception as e:
            logger.error(f"Error in PrayerTimeAgent: {e}")
            return {
                "agent": self.name,
                "response": "Maaf, tidak dapat mengambil jadwal sholat.",
                "error": str(e)
            }
    
    def _get_coordinates(self, location: str) -> Dict[str, float]:
        """Get coordinates for location"""
        # Predefined major locations
        locations = {
            "makkah": {"latitude": 21.4225, "longitude": 39.8262},
            "madinah": {"latitude": 24.5247, "longitude": 39.5692},
            "jeddah": {"latitude": 21.5433, "longitude": 39.1728},
        }
        
        return locations.get(location.lower(), locations["makkah"])
    
    async def _fetch_prayer_times(
        self,
        lat: float,
        lon: float,
        date: datetime
    ) -> Dict[str, str]:
        """Fetch prayer times from API"""
        try:
            timestamp = int(date.timestamp())
            url = f"{self.api_url}/{timestamp}"
            
            params = {
                "latitude": lat,
                "longitude": lon,
                "method": 4  # Umm Al-Qura University, Makkah
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data["code"] == 200:
                return data["data"]["timings"]
            else:
                raise Exception("API returned error")
                
        except Exception as e:
            logger.error(f"Error fetching prayer times: {e}")
            # Return default Makkah times as fallback
            return {
                "Fajr": "05:00",
                "Sunrise": "06:20",
                "Dhuhr": "12:30",
                "Asr": "15:45",
                "Maghrib": "18:15",
                "Isha": "19:45"
            }
    
    def _format_prayer_times(
        self,
        times: Dict[str, str],
        location: str
    ) -> str:
        """Format prayer times for display"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        response = f"🕌 *Jadwal Sholat - {location}*\n"
        response += f"📅 {now.strftime('%A, %d %B %Y')}\n\n"
        
        prayers = [
            ("Subuh", times.get("Fajr", "05:00")),
            ("Terbit", times.get("Sunrise", "06:20")),
            ("Dzuhur", times.get("Dhuhr", "12:30")),
            ("Ashar", times.get("Asr", "15:45")),
            ("Maghrib", times.get("Maghrib", "18:15")),
            ("Isya", times.get("Isha", "19:45"))
        ]
        
        for name, time in prayers:
            # Mark current/upcoming prayer
            marker = "⏰" if time > current_time else "✅"
            response += f"{marker} {name}: {time}\n"
        
        # Find next prayer
        next_prayer = self._find_next_prayer(current_time, prayers)
        if next_prayer:
            response += f"\n⏭️ Sholat berikutnya: *{next_prayer[0]}* ({next_prayer[1]})"
        
        return response
    
    def _find_next_prayer(
        self,
        current: str,
        prayers: list
    ) -> tuple:
        """Find next upcoming prayer"""
        for name, time in prayers:
            if time > current:
                return (name, time)
        return prayers[0]  # Next day Fajr