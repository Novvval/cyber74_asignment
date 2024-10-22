from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class BaseModel:
    pass

@dataclass
class Product(BaseModel):
    id: Optional[int] = None
    link: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None

@dataclass
class Price(BaseModel):
    id: Optional[int] = None
    value: Optional[int] = None
    date: Optional[datetime] = None
    product: Optional[Product] = None
    product_id: Optional[int] = None


@dataclass
class ProductInfoSchema(BaseModel):
    link: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    value: Optional[int] = None