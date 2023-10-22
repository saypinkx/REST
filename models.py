from database import Base
from sqlalchemy import ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

Product_User = Table('Product_User',
                     Base.metadata,
                     Column('id', Integer, autoincrement=True, primary_key=True),
                     Column('product_id', Integer, ForeignKey('Product.id')),
                     Column('user_id', Integer, ForeignKey('User.id'))
                     )


class User(Base):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    products = relationship("Product", back_populates='owner', uselist=True, foreign_keys='Product.owner_id')
    # allowed_products = relationship('User', back_populates='allowed_users', uselist=True)


class Product(Base):
    __tablename__ = "Product"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column()
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    owner = relationship("User", back_populates='products', foreign_keys=owner_id)
    # allowed_users_id: Mapped[list[int]] = mapped_column(ForeignKey(User.id), nullable=True)
    allowed_users = relationship('User', uselist=True, secondary=Product_User)
    lessons = relationship("Lesson", uselist=True, back_populates='product', cascade='all, delete-orphan')


class Lesson(Base):
    __tablename__ = 'Lesson'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column()
    link: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()
    product_id = mapped_column(ForeignKey(Product.id))
    product = relationship('Product', uselist=False, back_populates='lessons', foreign_keys=product_id)
