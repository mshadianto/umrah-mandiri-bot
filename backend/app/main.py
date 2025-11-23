# -*- coding: utf-8 -*-
"""
Umrah Assistant API
Main application entry point - Enhanced Version
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('api.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Umrah Assistant API",
    description="""
    ## AI-Powered Umrah Guide
    
    Advanced features:
    - 🤖 RAG-based AI Chat
    - 🕌 Real-time Prayer Times
    - 🗺️ Navigation & Location Services
    - 🆘 Emergency Assistance
    - 📊 Progress Tracking
    - 💡 Smart Tips & Recommendations
    
    Powered by Multi-Agent AI System with Islamic Knowledge Base
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "Umrah Assistant API v2.0",
        "status": "running",
        "features": [
            "AI Chat with RAG",
            "Real-time Prayer Times",
            "Navigation Services",
            "Emergency Assistance",
            "Progress Tracking",
            "Multilingual Support"
        ],
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "health_check": "/health"
    }

@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "umrah-assistant-api",
        "version": "2.0.0",
        "components": {
            "api": "operational",
            "agents": "operational",
            "database": "pending",  # Will be "operational" when DB is connected
            "rag": "pending"  # Will be "operational" when RAG is ready
        }
    }

@app.get("/features")
async def features():
    """
    List all available features
    """
    return {
        "core_features": {
            "chat": {
                "endpoint": "/api/v1/chat/message",
                "description": "AI-powered chat with RAG",
                "status": "available"
            },
            "users": {
                "endpoint": "/api/v1/users",
                "description": "User management",
                "status": "available"
            },
            "umrah_guide": {
                "endpoint": "/api/v1/umrah",
                "description": "Umrah manasik information",
                "status": "available"
            }
        },
        "advanced_features": {
            "prayer_times": {
                "endpoint": "/api/v1/advanced/prayer-times",
                "description": "Real-time prayer times by location",
                "status": "available"
            },
            "navigation": {
                "endpoint": "/api/v1/advanced/navigation",
                "description": "Location & navigation services",
                "status": "available"
            },
            "emergency": {
                "endpoint": "/api/v1/advanced/emergency",
                "description": "Emergency assistance",
                "status": "available"
            },
            "progress": {
                "endpoint": "/api/v1/advanced/progress",
                "description": "Track umrah progress",
                "status": "available"
            },
            "tips": {
                "endpoint": "/api/v1/advanced/tips",
                "description": "Quick tips & recommendations",
                "status": "available"
            }
        }
    }

# ============================================================================
# ROUTER IMPORTS & REGISTRATION
# ============================================================================

# Track loaded routers
loaded_routers = []
failed_routers = []

# Import and register routers
try:
    logger.info("Loading API routers...")
    
    # Core routers
    try:
        from app.api.v1 import users
        app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
        loaded_routers.append("users")
        logger.info("✓ Users router loaded")
    except ImportError as e:
        failed_routers.append(("users", str(e)))
        logger.warning(f"✗ Users router not available: {e}")
    
    try:
        from app.api.v1 import umrah
        app.include_router(umrah.router, prefix="/api/v1/umrah", tags=["Umrah Guide"])
        loaded_routers.append("umrah")
        logger.info("✓ Umrah router loaded")
    except ImportError as e:
        failed_routers.append(("umrah", str(e)))
        logger.warning(f"✗ Umrah router not available: {e}")
    
    try:
        from app.api.v1 import chat
        app.include_router(chat.router, prefix="/api/v1/chat", tags=["AI Chat"])
        loaded_routers.append("chat")
        logger.info("✓ Chat router loaded")
    except ImportError as e:
        failed_routers.append(("chat", str(e)))
        logger.warning(f"✗ Chat router not available: {e}")
    
    # Advanced routers
    try:
        from app.api.v1 import advanced
        app.include_router(advanced.router, prefix="/api/v1/advanced", tags=["Advanced Features"])
        loaded_routers.append("advanced")
        logger.info("✓ Advanced router loaded")
    except ImportError as e:
        failed_routers.append(("advanced", str(e)))
        logger.warning(f"✗ Advanced router not available: {e}")
    
    # Summary
    if loaded_routers:
        logger.info(f"Successfully loaded {len(loaded_routers)} routers: {', '.join(loaded_routers)}")
    
    if failed_routers:
        logger.warning(f"Failed to load {len(failed_routers)} routers")
        for router_name, error in failed_routers:
            logger.warning(f"  - {router_name}: {error}")
        logger.info("API will run with limited functionality")
    else:
        logger.info("All routers loaded successfully!")
    
except Exception as e:
    logger.error(f"Critical error loading routers: {e}", exc_info=True)

# ============================================================================
# LIFECYCLE EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Run on startup
    """
    logger.info("=" * 80)
    logger.info("🕌 UMRAH ASSISTANT API v2.0 - STARTING")
    logger.info("=" * 80)
    logger.info("")
    logger.info("📊 System Status:")
    logger.info(f"  ✓ FastAPI: Running")
    logger.info(f"  ✓ CORS: Enabled")
    logger.info(f"  ✓ Routers: {len(loaded_routers)} loaded")
    logger.info("")
    logger.info("🔗 Endpoints:")
    logger.info("  • API Root: http://localhost:8000/")
    logger.info("  • API Docs: http://localhost:8000/docs")
    logger.info("  • ReDoc: http://localhost:8000/redoc")
    logger.info("  • Health Check: http://localhost:8000/health")
    logger.info("  • Features List: http://localhost:8000/features")
    logger.info("")
    logger.info("🤖 Available Features:")
    for router in loaded_routers:
        logger.info(f"  ✓ {router.capitalize()}")
    logger.info("")
    
    if failed_routers:
        logger.info("⚠️  Unavailable Features:")
        for router_name, _ in failed_routers:
            logger.info(f"  ✗ {router_name.capitalize()}")
        logger.info("")
    
    logger.info("=" * 80)
    logger.info("✅ API is ready to accept requests!")
    logger.info("=" * 80)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on shutdown
    """
    logger.info("=" * 80)
    logger.info("👋 Umrah Assistant API Shutting down...")
    logger.info("=" * 80)
    
    # Cleanup tasks here (close DB connections, etc.)
    logger.info("Performing cleanup tasks...")
    
    logger.info("✅ Shutdown complete")

# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    logger.error(f"Request: {request.method} {request.url}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "detail": str(exc) if app.debug else None
        }
    )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Handle 404 errors
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "message": f"The endpoint {request.url.path} does not exist",
            "available_endpoints": {
                "docs": "/docs",
                "health": "/health",
                "features": "/features"
            }
        }
    )

# ============================================================================
# MIDDLEWARE (Optional - for logging requests)
# ============================================================================

@app.middleware("http")
async def log_requests(request, call_next):
    """
    Log all incoming requests
    """
    import time
    
    start_time = time.time()
    
    # Log request
    logger.info(f"→ {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log response
    logger.info(f"← {response.status_code} - {request.method} {request.url.path} - {duration:.2f}s")
    
    return response

# ============================================================================
# APPLICATION INFO
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 80)
    print("🕌 UMRAH ASSISTANT API")
    print("=" * 80)
    print("Starting development server...")
    print("API will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("=" * 80 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )