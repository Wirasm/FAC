"""
SQLAlchemy models for the item module.

These models define the database structure for items.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DECIMAL, Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Item(Base):
    """Database model for items."""
    
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    image_url = Column(String, nullable=True)
    category = Column(String(100), nullable=True)
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self) -> str:
        """String representation of the item."""
        return f"<Item(id={self.id}, name={self.name}, price={self.price})>"