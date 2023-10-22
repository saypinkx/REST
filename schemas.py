from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: str = None
    password: str = None
    firstname: str = None
    lastname: str = None

    class Config:
        orm_mode = True

class ProductResponse(BaseModel):
    id: int
    name: str
    owner_id: int
class ProductCreate(BaseModel):
    name: str
    owner_id: int

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    name: str = None
    owner_id: int = None

    class Config:
        orm_mode = True


class LessonCreate(BaseModel):
    name: str
    link: str
    duration: int
    product_id: int


class LessonResponse(BaseModel):
    id: int
    name: str
    link: str
    duration: int
    product_id: int
