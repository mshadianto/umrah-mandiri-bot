# -*- coding: utf-8 -*-
"""
Fixed API Client for Bot
"""
import httpx
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """API Client with correct endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.timeout = 30.0
    
    async def call(self, endpoint: str, method: str = "POST", data: Dict = None) -> Optional[Dict]:
        """Make API call with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if method == "POST":
                    response = await client.post(url, json=data or {})
                else:
                    response = await client.get(url, params=data)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    logger.warning(f"Endpoint not found: {endpoint}")
                    return None
                else:
                    logger.warning(f"API returned {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.warning(f"API timeout for {endpoint}")
            return None
        except Exception as e:
            logger.error(f"API error: {e}")
            return None
    
    async def chat(self, message: str, user_id: int) -> Optional[Dict]:
        """Send chat message - FIXED PATH"""
        return await self.call(
            "/api/v1/chat/message",  # Correct path
            "POST",
            {
                "message": message,
                "user_id": str(user_id)
            }
        )
    
    async def prayer_times(self, location: str = "Makkah") -> Optional[Dict]:
        """Get prayer times - FIXED PATH"""
        return await self.call(
            "/api/v1/advanced/prayer-times",  # Correct path
            "POST",
            {
                "location": location
            }
        )
    
    async def navigation(self, query: str) -> Optional[Dict]:
        """Get navigation - FIXED PATH"""
        return await self.call(
            "/api/v1/advanced/navigation",  # Correct path
            "POST",
            {
                "query": query
            }
        )
    
    async def emergency(self, query: str, emerg_type: str = "general") -> Optional[Dict]:
        """Get emergency info - FIXED PATH"""
        return await self.call(
            "/api/v1/advanced/emergency",  # Correct path
            "POST",
            {
                "query": query,
                "type": emerg_type
            }
        )
    
    async def tips(self, category: str) -> Optional[Dict]:
        """Get tips - FIXED PATH"""
        return await self.call(
            f"/api/v1/advanced/tips/{category}",  # Correct path
            "GET"
        )
    
    async def health_check(self) -> Optional[Dict]:
        """Check API health"""
        return await self.call("/health", "GET")
