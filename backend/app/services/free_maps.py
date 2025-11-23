# -*- coding: utf-8 -*-
"""
Free Maps Service using OpenStreetMap
NO API KEY NEEDED!
"""
from typing import Dict, Any, Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from app.config import settings
import logging
import time

logger = logging.getLogger(__name__)

class FreeMapsService:
    """
    Free maps service using OpenStreetMap/Nominatim
    NO API KEY REQUIRED!
    """
    
    def __init__(self):
        self.geolocator = Nominatim(
            user_agent=settings.NOMINATIM_USER_AGENT,
            timeout=10
        )
        
        # Important locations in Makkah & Madinah
        self.important_locations = {
            "masjidil_haram": {
                "name": "Masjidil Haram",
                "lat": 21.4225,
                "lon": 39.8262,
                "city": "Makkah"
            },
            "masjid_nabawi": {
                "name": "Masjid Nabawi",
                "lat": 24.4672,
                "lon": 39.6111,
                "city": "Madinah"
            },
            "jabal_rahmah": {
                "name": "Jabal Rahmah",
                "lat": 21.3551,
                "lon": 39.9831,
                "city": "Arafah"
            },
            "gua_hira": {
                "name": "Gua Hira",
                "lat": 21.4574,
                "lon": 39.8565,
                "city": "Makkah"
            },
            "mina": {
                "name": "Mina",
                "lat": 21.4204,
                "lon": 39.8890,
                "city": "Makkah"
            },
            "muzdalifah": {
                "name": "Muzdalifah",
                "lat": 21.4021,
                "lon": 39.9382,
                "city": "Makkah"
            }
        }
    
    async def geocode(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Convert address to coordinates
        FREE - uses OpenStreetMap
        """
        try:
            location = self.geolocator.geocode(address)
            
            if location:
                return {
                    "address": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "raw": location.raw
                }
            return None
            
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error(f"Geocoding error: {e}")
            return None
    
    async def reverse_geocode(
        self, 
        latitude: float, 
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """
        Convert coordinates to address
        FREE - uses OpenStreetMap
        """
        try:
            location = self.geolocator.reverse(f"{latitude}, {longitude}")
            
            if location:
                return {
                    "address": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "raw": location.raw
                }
            return None
            
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error(f"Reverse geocoding error: {e}")
            return None
    
    def calculate_distance(
        self,
        point1: Tuple[float, float],
        point2: Tuple[float, float]
    ) -> float:
        """
        Calculate distance between two points in kilometers
        FREE - no API needed!
        
        Args:
            point1: (latitude, longitude)
            point2: (latitude, longitude)
        
        Returns:
            Distance in kilometers
        """
        try:
            distance = geodesic(point1, point2).kilometers
            return round(distance, 2)
        except Exception as e:
            logger.error(f"Distance calculation error: {e}")
            return 0.0
    
    def get_nearby_important_locations(
        self,
        latitude: float,
        longitude: float,
        max_distance_km: float = 50
    ) -> List[Dict[str, Any]]:
        """
        Find important Islamic locations nearby
        """
        user_location = (latitude, longitude)
        nearby = []
        
        for loc_id, loc_data in self.important_locations.items():
            loc_coords = (loc_data["lat"], loc_data["lon"])
            distance = self.calculate_distance(user_location, loc_coords)
            
            if distance <= max_distance_km:
                nearby.append({
                    "id": loc_id,
                    "name": loc_data["name"],
                    "city": loc_data["city"],
                    "distance_km": distance,
                    "coordinates": {
                        "latitude": loc_data["lat"],
                        "longitude": loc_data["lon"]
                    }
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x["distance_km"])
        return nearby
    
    def get_location_info(self, location_name: str) -> Optional[Dict[str, Any]]:
        """Get info about important location"""
        for loc_id, loc_data in self.important_locations.items():
            if location_name.lower() in loc_data["name"].lower():
                return loc_data
        return None

# Global instance
free_maps = FreeMapsService()