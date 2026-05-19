from pydantic import BaseModel

class user_create(BaseModel):
    users: str
    products: str
    orders: str
    order_items: str
    payments: int   # "male" or "female"

class user_response(user_create): # ALR INHERITS THE FIELD FROM USER_CREATE
    id: int
    class Config:
        orm_mode = True # converts it into JSON


class EcommerceCreate(BaseModel):
    users: str
    products: str
    orders: str
    order_items: str
    payments: int

class EcommerceResponse(EcommerceCreate):
    id: int

    class Config:
        orm_mode = True
