from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from .database import Base

class ServiceConfig(Base):
    __tablename__ = "service_configs"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100), unique=True, index=True, nullable=False)
    service_type = Column(String(50), nullable=False)  # browser, document, communication, media, bot_builder
    
    # Service configuration
    base_url = Column(String(255))
    api_key = Column(String(255))  # Encrypted API key
    config_data = Column(JSON)  # Service-specific configuration
    
    # Service status
    is_active = Column(Boolean, default=True)
    is_healthy = Column(Boolean, default=True)
    last_health_check = Column(DateTime(timezone=True))
    
    # Endpoints
    endpoints = Column(JSON)  # Available endpoints for this service
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<ServiceConfig(id={self.id}, service_name='{self.service_name}', is_active={self.is_active})>"