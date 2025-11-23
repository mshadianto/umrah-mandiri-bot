# -*- coding: utf-8 -*-
"""
User Models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
    # Profile
    language = Column(String, default="id")  # id, en, ar
    timezone = Column(String, default="Asia/Jakarta")
    
    # Umrah Info
    umrah_date = Column(DateTime, nullable=True)
    hotel_name = Column(String, nullable=True)
    hotel_location = Column(String, nullable=True)
    
    # Preferences
    preferences = Column(JSON, default={})
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class UmrahProgress(Base):
    __tablename__ = "umrah_progress"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    
    # Progress tracking
    ihram_completed = Column(Boolean, default=False)
    ihram_completed_at = Column(DateTime, nullable=True)
    
    thawaf_completed = Column(Boolean, default=False)
    thawaf_count = Column(Integer, default=0)
    thawaf_completed_at = Column(DateTime, nullable=True)
    
    sai_completed = Column(Boolean, default=False)
    sai_count = Column(Integer, default=0)
    sai_completed_at = Column(DateTime, nullable=True)
    
    tahalul_completed = Column(Boolean, default=False)
    tahalul_completed_at = Column(DateTime, nullable=True)
    
    # Additional activities
    visited_locations = Column(JSON, default=[])
    duas_read = Column(JSON, default=[])
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    
    message = Column(String)
    response = Column(String)
    agent = Column(String)
    
    # Context
    context = Column(JSON, default={})
    sources = Column(JSON, default=[])
    
    # Ratings
    helpful = Column(Boolean, nullable=True)
    rating = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)