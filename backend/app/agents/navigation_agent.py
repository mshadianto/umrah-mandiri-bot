from app.services.free_maps import free_maps

# In the execute method, use free_maps instead of Google Maps
async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    query = input_data.get("query", "").lower()
    user_location = input_data.get("user_location")
    
    # Use free maps service
    if "hotel" in query and user_location:
        lat = user_location.get("lat")
        lon = user_location.get("lon")
        
        nearby = free_maps.get_nearby_important_locations(lat, lon)
        # ... format response