from typing import Optional
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models import Product


async def create_product(db: AsyncSession, data: dict):
    """
    Создать новый товар в базе данных.
    
    Args:
        db: Асинхронная сессия базы данных
        data: Словарь с данными товара
        
    Returns:
        Product: Созданный товар или None в случае ошибки
    """
    new_product = Product(**data)
    try:
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product
    except SQLAlchemyError:
        return None
    

async def get_products(db: AsyncSession):
    """
    Получить все товары из базы данных.
    
    Args:
        db: Асинхронная сессия базы данных
        
    Returns:
        List[Product]: Список всех товаров
    """
    result = await db.execute(select(Product))
    return result.scalars().all()


async def search_products(
    db: AsyncSession, 
    name: Optional[str] = None, 
    category: Optional[str] = None
):
    """
    Поиск товаров по названию и/или категории.
    
    Args:
        db: Асинхронная сессия базы данных
        name: Название товара (частичное совпадение, без учета регистра)
        category: Категория товара (частичное совпадение, без учета регистра)
        
    Returns:
        List[Product]: Список товаров, соответствующих критериям поиска
    """
    query = select(Product)
    
    conditions = []
    if name:
        conditions.append(Product.name.ilike(f"%{name}%"))
    if category:
        conditions.append(Product.category.ilike(f"%{category}%"))
    if conditions:
        query = query.where(or_(*conditions))
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_product(id: int, db: AsyncSession):
    """
    Получить товар по ID.
    
    Args:
        id: ID товара
        db: Асинхронная сессия базы данных
        
    Returns:
        Product: Найденный товар или None если не найден
    """
    result = await db.execute(select(Product).where(Product.id == id))
    return result.scalar_one_or_none()


async def delete_product_by_id(id: int, db: AsyncSession):
    """
    Удалить товар по ID.
    
    Args:
        id: ID товара для удаления
        db: Асинхронная сессия базы данных
        
    Returns:
        bool: True если товар удален, None если товар не найден
    """
    product = await get_product(id=id, db=db)
    if not product:
        return None
    await db.delete(product)
    await db.commit()
    return True