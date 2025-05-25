from pydantic import BaseModel

class ProductBase(BaseModel):
    __tablename__ = "products"

    name: str
    price: int
    description: str

class Product(ProductBase):
    id: int
