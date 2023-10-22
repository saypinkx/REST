from fastapi import APIRouter, Depends, Body, Path, HTTPException, Query, status
from typing import Annotated
from database import SessionLocal
from schemas import UserLogin, UserResponse, UserUpdate, UserCreate, ProductCreate, ProductUpdate, LessonCreate, \
    LessonResponse, ProductResponse
from models import User, Product, Lesson
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(prefix='/api/v1')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/s')
def hello():
    return 'hello'


@router.post('/users/', response_model=UserResponse, status_code=201)
def create_user(user: Annotated[UserCreate, Body()], db: Session = Depends(get_db)):
    try:
        user_db = User(username=user.username, password=user.password, firstname=user.firstname, lastname=user.lastname)
        db.add(user_db)
        db.commit()
    except:
        raise HTTPException(status_code=400, detail='user with username already registered')
    return user_db


@router.get('/users/{username}', response_model=UserResponse)
def get_current_user(username: Annotated[str, Path()], db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == username).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='user with username not found')
    return user_db


@router.post('/user/login', response_model=UserResponse)
def login_user(user: Annotated[UserLogin, Body()], db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='user with username not found')
    if user_db.password != user.password:
        raise HTTPException(status_code=401, detail='invalid password')
    return user_db


@router.put('/users/{user_id}', status_code=200, response_model=UserResponse)
def update_user(user_id: Annotated[str, Path()], new_user: Annotated[UserUpdate, Body()],
                db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='user with username not found')

    new_user_dict = new_user.dict()
    for key in new_user_dict:
        if not new_user_dict[key]:
            new_user_dict[key] = user_db.__dict__[key]
    user_db.username, user_db.password, user_db.firstname, user_db.lastname = new_user_dict['username'], new_user_dict[
        'password'], new_user_dict['firstname'], new_user_dict['lastname']
    try:
        db.add(user_db)
        db.commit()
    except:
        raise HTTPException(status_code=400, detail='user with username already registered')

    return user_db


# @router.put('/users/{user_id}', status_code=200)
# def update_password(user_id: Annotated[int, Path()], password: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     user.password = password
#     db.add(user)
#     db.commit()
#     return 'yes'
@router.delete('/users/{user_id}', status_code=200)
def delete_user(user_id: Annotated[int, Path()], db: Session = Depends(get_db)):
    user_db = db.query(User).get(user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail='user not be found')
    db.delete(user_db)
    db.commit()
    return user_db


@router.get('/users/')
def get_all_users(firstname: Annotated[str | None, Query()] = None,
                  lastname: Annotated[str | None, Query()] = None, db: Session = Depends(get_db)) -> list[UserResponse]:
    select = db.query(User)
    if firstname:
        select = select.filter(User.firstname == firstname)
    if lastname:
        select = select.filter(User.lastname == lastname)
    users = select.all()
    return users


@router.post('/products/', status_code=201, response_model=ProductResponse)
def create_product(product: Annotated[ProductCreate, Body()], db: Session = Depends(get_db)):
    owner = db.query(User).get(product.owner_id)
    if not owner:
        raise HTTPException(detail='owner not found', status_code=404)
    product_db = Product(name=product.name, owner_id=product.owner_id, owner=owner)
    db.add(product_db)
    db.commit()
    return product_db


@router.put('/products/{product_id}', status_code=200, response_model=ProductUpdate)
def update_product(product_id: Annotated[int, Path()], new_product: Annotated[ProductUpdate, Body()],
                   db: Session = Depends(get_db), test: str = Body(default=None)):
    product_db = db.query(Product).get(product_id)
    if not product_db:
        raise HTTPException(status_code=404, detail='product not found')
    if new_product.name:
        product_db.name = new_product.name
    if new_product.owner_id:
        product_db.owner_id = new_product.owner_id
        owner = db.query(User).get(new_product.owner_id)
        if not owner:
            raise HTTPException(status_code=404, detail='owner not found')
        product_db.owner = owner
    db.add(product_db)
    db.commit()
    return product_db


@router.post('/products/{product_id}/allowed_users', status_code=201)
def add_allowed_user(product_id: Annotated[int, Path()], user_id: Annotated[int, Query()],
                     db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail='product not found')
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    product.allowed_users.append(user)
    db.add(product)
    db.commit()
    return product.allowed_users


@router.delete('/products/{product_id}/allowed_users', status_code=200)
def remove_allowed_user(product_id: Annotated[int, Path()], user_id: Annotated[int, Query()],
                        db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail='product not found')
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    product.allowed_users.remove(user)
    db.add(product)
    db.commit()
    return product.allowed_users


@router.get('/products/{product_id}/allowed_users', status_code=200, response_model=list[UserResponse])
def get_allowed_users(product_id: Annotated[int, Path()], db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail='product not found')
    return product.allowed_users


@router.get('/products/{product_id}', response_model=ProductResponse)
def get_product(product_id: Annotated[int, Path()], db: Session = Depends(get_db)):
    product_db = db.get(Product, product_id)
    if not product_db:
        raise HTTPException(status_code=404, detail='product not found')
    return product_db


@router.delete('/products/{product_id}', status_code=200, response_model=ProductCreate)
def delete_product(product_id: Annotated[int, Path()], db: Session = Depends(get_db)):
    product_db = db.get(Product, product_id)
    if not product_db:
        raise HTTPException(status_code=404, detail='product  not found')
    db.delete(product_db)
    db.commit()
    return product_db


@router.get('/users/{user_id}/allowed_products', response_model=list[ProductCreate])
def get_allowed_products(user_id: Annotated[int, Path()], db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    smtp = select(Product).where(Product.allowed_users.contains(user))
    products_db = db.scalars(smtp).all()
    return products_db


@router.post('/lessons/', status_code=201, response_model=LessonResponse)
def create_lesson(lesson: Annotated[LessonCreate, Body()], db: Session = Depends(get_db)):
    product_db = db.get(Product, lesson.product_id)
    if not product_db:
        raise HTTPException(status_code=404, detail='product not found')
    lesson_db = Lesson(name=lesson.name, link=lesson.link, duration=lesson.duration, product=product_db)
    db.add(lesson_db)
    db.commit()
    return lesson_db


@router.get('/products/', status_code=200, response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    smtp = select(Product)
    products_db = db.scalars(smtp).all()
    return products_db

@router.get('/lessons/', status_code=200, response_model=list[LessonResponse])
def get_lessons(db: Session = Depends(get_db)):
    smtp = select(Lesson)
    lessons_db = db.scalars(smtp).all()
    return lessons_db

# @router.get('/products/{product_id}/lessons')
# @router.get('/users/{user_id}/allowed_lessons')
# @router.get('/lessons/{lesson_id}') + delete + update + read
#  + сама тзшка

