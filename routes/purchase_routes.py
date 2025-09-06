from fastapi import APIRouter, Depends
from typing import List
from datetime import datetime
from app.schemas import PurchaseOut
from app.database import carts, products, purchases
from app.auth import get_current_user_email
from app.utils import serialize_id

router = APIRouter(prefix="/purchases", tags=["Purchases"])

@router.post("/checkout")
def checkout(email: str = Depends(get_current_user_email)):
    items = list(carts.find({"user_email": email}))
    for it in items:
        prod = products.find_one({"_id": it["product_id"]})
        if not prod: continue
        purchases.insert_one({
            "user_email": email,
            "product": prod,  # snapshot
            "purchased_at": datetime.utcnow().isoformat()
        })
        carts.delete_one({"_id": it["_id"]})
    return {"message": "Checkout complete"}

@router.get("/", response_model=List[PurchaseOut])
def history(email: str = Depends(get_current_user_email)):
    res = []
    for p in purchases.find({"user_email": email}).sort("_id", -1):
        prod = serialize_id(p["product"])
        res.append({
            "id": str(p["_id"]),
            "product": {
                "id": prod["id"],
                "title": prod["title"],
                "description": prod.get("description",""),
                "category": prod["category"],
                "price": float(prod["price"]),
                "image": prod.get("image","placeholder.jpg"),
                "owner_email": prod["owner_email"]
            },
            "purchased_at": p["purchased_at"]
        })
    return res
