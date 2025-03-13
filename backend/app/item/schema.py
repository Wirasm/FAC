"""
Pydantic schemas for the item module.

These schemas define the structure for request and response data related to items.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base schema for item data that's common to all operations."""
    
    name: str = Field(..., description="The name of the item")
    description: Optional[str] = Field(None, description="Detailed description of the item")
    price: Decimal = Field(..., description="The price of the item", gt=0)
    image_url: Optional[str] = Field(None, description="URL to the item's image")
    category: Optional[str] = Field(None, description="Category the item belongs to")
    in_stock: bool = Field(True, description="Whether the item is currently in stock")


class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an existing item."""
    
    name: Optional[str] = Field(None, description="The name of the item")
    description: Optional[str] = Field(None, description="Detailed description of the item")
    price: Optional[Decimal] = Field(None, description="The price of the item", gt=0)
    image_url: Optional[str] = Field(None, description="URL to the item's image")
    category: Optional[str] = Field(None, description="Category the item belongs to")
    in_stock: Optional[bool] = Field(None, description="Whether the item is currently in stock")


class ItemResponse(ItemBase):
    """Schema for item responses that includes database fields."""
    
    id: int = Field(..., description="The unique identifier for the item")
    created_at: datetime = Field(..., description="When the item was created")
    updated_at: datetime = Field(..., description="When the item was last updated")
    
    class Config:
        """Pydantic config."""
        
        from_attributes = True