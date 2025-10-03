from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.schemas.product import ProductCreate, ProductFull, ProductList

from app.crud.product import create_product, get_products, get_product, search_products, delete_product_by_id


product_router = APIRouter(prefix="/api/v1", tags=["products"])


@product_router.post("/products", status_code=201, response_model=ProductFull)
async def add_product(
    product_data: ProductCreate, db: AsyncSession = Depends(get_db)
):
    """
    Создать новый товар.
    
    - product_data: Данные для создания товара (название, описание, цена, категория)
    - Возвращает: Созданный товар с присвоенным ID
    """
    new_product = await create_product(data=product_data.model_dump(), db=db)
    return new_product


@product_router.get(
        "/products",
        response_model=List[ProductList],
        responses={404: {"description": "Products not found"}}
)
async def get_all_products(
    category: Optional[str] = Query(None, description="Search by category"),
    name: Optional[str] = Query(None, description="Search by product name"),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список товаров с возможностью поиска.
    
    - category: Поиск по категории (частичное совпадение, без учета регистра)
    - name: Поиск по названию товара (частичное совпадение, без учета регистра)
    - Возвращает: Список товаров, соответствующих критериям поиска или полный список, если условия не заданы
    - Вызывает 404: Если товары не найдены
    """
    if category or name:
        products = await search_products(category=category, name=name, db=db)
    else:
        products = await get_products(db=db)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Products not found.")
    return products


@product_router.get(
        "/products/{id}",
        response_model=ProductFull,
        responses={404: {"description": "Product not found"}}
)
async def product_info(
    id: int, db: AsyncSession = Depends(get_db)
):
    """
    Получить детальную информацию о конкретном товаре.
    
    - id: ID товара
    - Возвращает: Полную информацию о товаре
    - Вызывает 404: Если товар с указанным ID не найден
    """
    product = await get_product(id=id, db=db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found.")
    return product


@product_router.delete(
        "/products/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
        204: {"description": "Product successfully deleted"},
        404: {"description": "Product not found"}
    }
)
async def delete_product(
    id: int, db: AsyncSession = Depends(get_db)
):
    """
    Удалить товар по ID.
    
    - id: ID товара для удаления
    - Возвращает: Пустой ответ со статусом 204
    - Вызывает 404: Если товар с указанным ID не найден
    """
    product = await delete_product_by_id(id=id, db=db)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found.")
    return None