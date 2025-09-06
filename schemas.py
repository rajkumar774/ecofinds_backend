from typing import Optional, List
from pydantic import BaseModel, EmailStr

# Auth
class SignUpIn(BaseModel):
    email: EmailStr
    password: str

class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# User
class UserOut(BaseModel):
    id: str
    email: EmailStr

# Product
class ProductIn(BaseModel):
    title: str
    description: Optional[str] = ""
    category: str
    price: float
    image: Optional[str] = "placeholder.jpg"

class ProductOut(BaseModel):
    id: str
    title: str
    description: str
    category: str
    price: float
    image: str
    owner_email: str

# Cart
class CartAddIn(BaseModel):
    product_id: str

class CartItemOut(BaseModel):
    id: str
    product: ProductOut

# Purchases
class PurchaseOut(BaseModel):
    id: str
    product: ProductOut
    purchased_at: str
