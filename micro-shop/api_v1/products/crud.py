from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Product
from sqlalchemy.engine import Result
from sqlalchemy import select

from .schemas import ProductCreate
async def get_products(session: AsyncSession)-> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result:Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)
async def get_product(session: AsyncSession, product_id: int)-> Product|None:
    return await session.get(Product, product_id)

async def create_product(session: AsyncSession, product: ProductCreate)-> Product|None:
    Product()
