from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Float, func, Text
from sqlalchemy.orm import relationship, registry

from .models import Product, Price

mapper_registry = registry()

product = Table(
    'product',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('link', String, nullable=False, unique=True),
    Column('title', String),
    Column('description', Text),
    Column('rating', Float),
)

price = Table(
    'price',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', Integer, nullable=False),
    Column('date', DateTime, default=func.now(), nullable=False),
    Column('product_id', ForeignKey('product.id', ondelete='CASCADE'), nullable=False),
)

def init_mappers() -> None:
    mapper_registry.map_imperatively(
        Product,
        product,
        properties={
            'prices': relationship(Price, back_populates='product', cascade='all, delete-orphan')
        }
    )
    mapper_registry.map_imperatively(
        Price,
        price,
        properties={
            'product': relationship(Product, back_populates='prices')
        }
    )

async def create_tables(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
