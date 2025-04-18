from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from database.custom_types import JSONText
from sqlalchemy.orm import relationship


class Product(Base):

    __tablename__ = "products"
     
    id = Column(BigInteger, primary_key=True, index=True)
    merchant_id = Column(BigInteger, default=0)
    category_id = Column(BigInteger, ForeignKey('categories.id'))
    currency_id = Column(BigInteger, ForeignKey('currencies.id'))
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    slug = Column(String, nullable=True)
    units = Column(Integer, default=0)
    weight = Column(Float, default=0)
    cost_price = Column(Float, default=0)
    price = Column(Float, default=0)
    discount_price = Column(Float, default=0)
    discount = Column(Float, default=0)
    discount_type = Column(Integer, default=0)
    special_note = Column(Text, nullable=True)
    unit_low_level = Column(Integer, default=0)
    files_meta_data = Column(JSONText)
    meta_data = Column(Text, nullable=True)
    notify_if_available = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

    category = relationship("Category")
    categories = relationship("Category", secondary="products_categories", back_populates="products")
    currency = relationship("Currency")
    tags = relationship("Tag", secondary="tags_products", back_populates="products")
    groups = relationship("Group", secondary="groups_products", back_populates="products")

def create_product(db: Session, merchant_id: int = 0, category_id: int = 0, currency_id: int = 0, name: str = None, description: str = None, slug: str = None, units: int = 0, weight: float = 0, cost_price: float = 0, price: float = 0, discount_price: float = 0, discount: float = 0, discount_type: int = 0, special_note: str = None, unit_low_level: int = 0, files_meta_data: Any=None, meta_data: str = None, notify_if_available: int = 0, status: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, commit: bool=False):
    product = Product(merchant_id=merchant_id, category_id=category_id, currency_id=currency_id, name=name, description=description, slug=slug, units=units, weight=weight, cost_price=cost_price, price=price, discount_price=discount_price, discount=discount, discount_type=discount_type, special_note=special_note, unit_low_level=unit_low_level, files_meta_data=files_meta_data, meta_data=meta_data, notify_if_available=notify_if_available, status=status, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(product)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(product)
    return product

def update_product(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Product).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_product(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Product).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_product(db: Session, id: int=0, commit: bool=False):
    db.query(Product).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_product_by_id(db: Session, id: int=0):
    return db.query(Product).options(joinedload(Product.category), joinedload(Product.categories), joinedload(Product.currency), joinedload(Product.tags)).filter_by(id = id).first()

def get_single_product_by_slug(db: Session, slug: str=None):
    return db.query(Product).options(joinedload(Product.category), joinedload(Product.categories), joinedload(Product.currency), joinedload(Product.tags)).filter_by(slug = slug).first()

def get_products(db: Session, filters: Dict={}):
    query = db.query(Product).options(joinedload(Product.category), joinedload(Product.categories), joinedload(Product.currency), joinedload(Product.tags))
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'category_id' in filters:
        query = query.filter_by(category_id = filters['category_id'])
    if 'currency_id' in filters:
        query = query.filter_by(currency_id = filters['currency_id'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    if 'name' in filters:
        query = query.filter(Product.name.like("%" + filters['name'] + "%"))
    if 'slug' in filters:
        query = query.filter(Product.slug.like('%' + filters['slug'] + '%'))
    return query.order_by(desc(Product.created_at))

