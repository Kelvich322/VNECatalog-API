import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product


@pytest.mark.asyncio
async def test_get_products(client: AsyncClient, test_product: Product):
    """Тестирует получение списка товара"""
    resp = await client.get("/api/products")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()[0]["name"] == "Test"


@pytest.mark.asyncio
async def test_get_product_info(client: AsyncClient, test_product: Product):
    """Тестирует получение полной информации о товаре"""
    resp = await client.get("/api/products/1")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["name"] == "Test"
    assert resp.json()["sizes"] == "Test sizes"
    assert resp.json()["description"] == "Test description"
    
    resp = await client.get("/api/products/999")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_products_search(client: AsyncClient, test_product: Product):
    """Тестирует поиск продуктов по категории и имени"""
    resp = await client.get("/api/products?category=Untitled")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    resp = await client.get("/api/products?category=Test")
    assert resp.status_code == status.HTTP_200_OK

    resp = await client.get("/api/products?name=Untitled")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    resp = await client.get("/api/products?name=Test")
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient, db_session: AsyncSession, test_product: Product):
    """Тестирует создание нового продукта"""
    data = {
        "name": "Test",
        "description": "Test",
        "price": 500.00,
        "category": "Test",
        "sizes": "Test"
    }
    resp = await client.post("/api/products", json=data)
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()["name"] == data["name"]

    data.pop("name")
    resp = await client.post("/api/products", json=data)
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient, test_product: Product):
    """Тестирует удаление продукта"""
    resp = await client.delete("/api/products/1")
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    resp = await client.delete("/api/products/1")
    assert resp.status_code == status.HTTP_404_NOT_FOUND