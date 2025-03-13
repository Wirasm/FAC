"""
API routes for the item module.

These routes handle CRUD operations for items.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional

from auth.clerk_deps import get_current_user
from core.logging import app_logger
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from item.model import Item
from item.schema import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(
    prefix="/api/items",
    tags=["items"],
)


@router.get("/", response_model=List[ItemResponse])
async def get_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of items to return"),
    category: Optional[str] = Query(None, description="Filter items by category"),
    in_stock: Optional[bool] = Query(None, description="Filter by in_stock status"),
    db: AsyncSession = Depends(get_db),
) -> List[ItemResponse]:
    """
    Get a list of items with optional filtering.

    This is a public endpoint accessible without authentication.
    """
    try:
        # Start with a base query
        query = select(Item)

        # Apply filters if provided
        if category:
            query = query.where(Item.category == category)
        if in_stock is not None:
            query = query.where(Item.in_stock == in_stock)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute the query
        result = await db.execute(query)
        items = result.scalars().all()

        app_logger.info(f"Retrieved {len(items)} items")
        return items
    except SQLAlchemyError as e:
        app_logger.error(f"Database error while retrieving items: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving items from the database",
        )


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int = Path(..., ge=1, description="The ID of the item to get"),
    db: AsyncSession = Depends(get_db),
) -> ItemResponse:
    """
    Get a specific item by ID.

    This is a public endpoint accessible without authentication.
    """
    try:
        # Query for the specific item
        result = await db.execute(select(Item).where(Item.id == item_id))
        item = result.scalars().first()

        if not item:
            app_logger.warning(f"Item with ID {item_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found",
            )

        app_logger.info(f"Retrieved item with ID {item_id}")
        return item
    except SQLAlchemyError as e:
        app_logger.error(f"Database error while retrieving item {item_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving item from the database",
        )


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
) -> ItemResponse:
    """
    Create a new item.

    This endpoint requires authentication.
    """
    try:
        # Create a new item instance
        db_item = Item(
            name=item.name,
            description=item.description,
            price=item.price,
            image_url=item.image_url,
            category=item.category,
            in_stock=item.in_stock,
        )

        # Add to the session and commit
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)

        user_id = user.get("sub")
        app_logger.info(f"User {user_id} created new item with ID {db_item.id}")

        return db_item
    except SQLAlchemyError as e:
        await db.rollback()
        app_logger.error(f"Database error while creating item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating the item in the database",
        )


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int = Path(..., ge=1, description="The ID of the item to update"),
    item_update: ItemUpdate = ...,
    db: AsyncSession = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
) -> ItemResponse:
    """
    Update an existing item.

    This endpoint requires authentication.
    """
    try:
        # Query for the specific item
        result = await db.execute(select(Item).where(Item.id == item_id))
        db_item = result.scalars().first()

        if not db_item:
            app_logger.warning(f"Item with ID {item_id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found",
            )

        # Update the item attributes if provided in the update
        if item_update.name is not None:
            db_item.name = item_update.name
        if item_update.description is not None:
            db_item.description = item_update.description
        if item_update.price is not None:
            db_item.price = item_update.price
        if item_update.image_url is not None:
            db_item.image_url = item_update.image_url
        if item_update.category is not None:
            db_item.category = item_update.category
        if item_update.in_stock is not None:
            db_item.in_stock = item_update.in_stock

        # Commit the changes
        await db.commit()
        await db.refresh(db_item)

        user_id = user.get("sub")
        app_logger.info(f"User {user_id} updated item with ID {item_id}")

        return db_item
    except SQLAlchemyError as e:
        await db.rollback()
        app_logger.error(f"Database error while updating item {item_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating the item in the database",
        )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int = Path(..., ge=1, description="The ID of the item to delete"),
    db: AsyncSession = Depends(get_db),
    user: Dict[str, Any] = Depends(get_current_user),
) -> None:
    """
    Delete an item.

    This endpoint requires authentication.
    """
    try:
        # Query for the specific item
        result = await db.execute(select(Item).where(Item.id == item_id))
        db_item = result.scalars().first()

        if not db_item:
            app_logger.warning(f"Item with ID {item_id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found",
            )

        # Delete the item
        await db.delete(db_item)
        await db.commit()

        user_id = user.get("sub")
        app_logger.info(f"User {user_id} deleted item with ID {item_id}")
    except SQLAlchemyError as e:
        await db.rollback()
        app_logger.error(f"Database error while deleting item {item_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting the item from the database",
        )
