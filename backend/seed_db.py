"""
Database seeding script.

This script populates the database with initial items for testing and development.
"""

import asyncio
import random
from decimal import Decimal
from typing import List, Dict, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.core.logging import setup_logger
from app.item.model import Base, Item

# Set up logger
logger = setup_logger("db_seeder")

# Convert standard PostgreSQL URL to asyncpg format if needed
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create the SQLAlchemy engine and session factory
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Sample item data
SAMPLE_ITEMS: List[Dict[str, Any]] = [
    {
        "name": "Ergonomic Desk Chair",
        "description": "A comfortable chair designed for long working hours with lumbar support and adjustable height.",
        "price": Decimal("189.99"),
        "image_url": "https://images.unsplash.com/photo-1596079890744-c1a0462d0975",
        "category": "furniture",
        "in_stock": True
    },
    {
        "name": "Mechanical Keyboard",
        "description": "A high-quality mechanical keyboard with customizable RGB lighting and tactile switches.",
        "price": Decimal("129.95"),
        "image_url": "https://images.unsplash.com/photo-1595044426077-d36d9236d35a",
        "category": "electronics",
        "in_stock": True
    },
    {
        "name": "Wireless Mouse",
        "description": "Precision wireless mouse with long battery life and ergonomic design.",
        "price": Decimal("49.99"),
        "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7",
        "category": "electronics",
        "in_stock": True
    },
    {
        "name": "Laptop Stand",
        "description": "Adjustable aluminum laptop stand that improves posture and keeps your device cool.",
        "price": Decimal("42.50"),
        "image_url": "https://images.unsplash.com/photo-1619948543338-d8eb37de6e5d",
        "category": "accessories",
        "in_stock": True
    },
    {
        "name": "Noise-Cancelling Headphones",
        "description": "Premium over-ear headphones with active noise cancellation for immersive audio experience.",
        "price": Decimal("249.99"),
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b",
        "category": "electronics",
        "in_stock": True
    },
    {
        "name": "Standing Desk",
        "description": "Electric height-adjustable desk with memory settings for sitting and standing positions.",
        "price": Decimal("399.00"),
        "image_url": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e",
        "category": "furniture",
        "in_stock": True
    },
    {
        "name": "External Monitor",
        "description": "27-inch 4K monitor with wide color gamut and multiple input ports.",
        "price": Decimal("349.95"),
        "image_url": "https://images.unsplash.com/photo-1629429407756-28d4a4982810",
        "category": "electronics",
        "in_stock": False
    },
    {
        "name": "Desk Lamp",
        "description": "LED desk lamp with adjustable brightness and color temperature settings.",
        "price": Decimal("39.99"),
        "image_url": "https://images.unsplash.com/photo-1534381548970-8317a57621b1",
        "category": "accessories",
        "in_stock": True
    },
    {
        "name": "Cable Management Kit",
        "description": "Complete cable organizer set to keep your workspace neat and tidy.",
        "price": Decimal("24.95"),
        "image_url": "https://images.unsplash.com/photo-1555589228-d215f4a635ab",
        "category": "accessories",
        "in_stock": True
    },
    {
        "name": "Portable SSD",
        "description": "1TB USB-C portable solid-state drive with fast transfer speeds.",
        "price": Decimal("179.99"),
        "image_url": "https://images.unsplash.com/photo-1618657246580-65b6bbba973a",
        "category": "electronics",
        "in_stock": True
    }
]


async def create_tables():
    """Create all tables in the database."""
    async with engine.begin() as conn:
        # Drop tables if they exist
        await conn.run_sync(Base.metadata.drop_all)
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")


async def seed_items():
    """Seed the database with sample items."""
    async with AsyncSessionFactory() as session:
        for item_data in SAMPLE_ITEMS:
            item = Item(**item_data)
            session.add(item)
        
        await session.commit()
    logger.info(f"Added {len(SAMPLE_ITEMS)} sample items to the database")


async def verify_connection():
    """Verify connection to the database."""
    async with AsyncSessionFactory() as session:
        result = await session.execute(text("SELECT 1"))
        if result.scalar() == 1:
            logger.info("Database connection verified")
        else:
            logger.error("Database connection test failed")


async def main():
    """Main entry point for the seeding script."""
    logger.info("Starting database seeding...")
    
    # First, verify we can connect to the database
    try:
        await verify_connection()
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        return
    
    # Create tables
    try:
        await create_tables()
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        return
    
    # Seed items
    try:
        await seed_items()
    except Exception as e:
        logger.error(f"Failed to seed items: {e}")
        return
    
    logger.info("Database seeding completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())