from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas import CartAddIn, CartItemOut, ProductOut
from app.database import carts, products
from app.auth import get_current_user_email
from app.utils import oid, serialize_id

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/")
def add_to_cart(payload: CartAddIn, email: str = Depends(get_current_user_email)):
    prod = products.find_one({"_id": oid(payload.product_id)})
    if not prod: raise HTTPException(status_code=404, detail="Product not found")
    carts.insert_one({"user_email": email, "product_id": prod["_id"]})
    return {"message": "Added to cart"}

@router.get("/", response_model=List[CartItemOut])
def view_cart(email: str = Depends(get_current_user_email)):
    out = []
    for c in carts.find({"user_email": email}):
        p = products.find_one({"_id": c["product_id"]})
        if not p: continue
        p = serialize_id(p)
        out.append({
            "id": str(c["_id"]),
            "product": {
                "id": p["id"],
                "title": p["title"],
                "description": p.get("description",""),
                "category": p["category"],
                "price": float(p["price"]),
                "image": p.get("image","placeholder.jpg"),
                "owner_email": p["owner_email"]
            }
        })
    return out

@router.delete("/{cart_item_id}")
def remove_from_cart(cart_item_id: str, email: str = Depends(get_current_user_email)):
    res = carts.delete_one({"_id": oid(cart_item_id), "user_email": email})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Removed"}
