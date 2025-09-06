from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from app.schemas import ProductIn, ProductOut
from app.database import products
from app.auth import get_current_user_email
from app.utils import oid, serialize_id

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductOut)
def create_product(payload: ProductIn, email: str = Depends(get_current_user_email)):
    doc = payload.model_dump()
    doc["owner_email"] = email
    res = products.insert_one(doc)
    created = products.find_one({"_id": res.inserted_id})
    created = serialize_id(created)
    return {
        "id": created["id"],
        "title": created["title"],
        "description": created.get("description",""),
        "category": created["category"],
        "price": float(created["price"]),
        "image": created.get("image", "placeholder.jpg"),
        "owner_email": created["owner_email"],
    }

@router.get("/", response_model=List[ProductOut])
def list_products(category: Optional[str] = None, search: Optional[str] = None):
    q = {}
    if category: q["category"] = category
    if search: q["title"] = {"$regex": search, "$options": "i"}
    data = []
    for d in products.find(q).sort("_id", -1):
        d = serialize_id(d)
        data.append({
            "id": d["id"],
            "title": d["title"],
            "description": d.get("description",""),
            "category": d["category"],
            "price": float(d["price"]),
            "image": d.get("image", "placeholder.jpg"),
            "owner_email": d["owner_email"],
        })
    return data

@router.get("/{product_id}", response_model=ProductOut)
def product_detail(product_id: str):
    doc = products.find_one({"_id": oid(product_id)})
    if not doc: raise HTTPException(status_code=404, detail="Not found")
    d = serialize_id(doc)
    return {
        "id": d["id"],
        "title": d["title"],
        "description": d.get("description",""),
        "category": d["category"],
        "price": float(d["price"]),
        "image": d.get("image", "placeholder.jpg"),
        "owner_email": d["owner_email"],
    }

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: str, payload: ProductIn, email: str = Depends(get_current_user_email)):
    doc = products.find_one({"_id": oid(product_id)})
    if not doc: raise HTTPException(status_code=404, detail="Not found")
    if doc["owner_email"] != email:
        raise HTTPException(status_code=403, detail="Not your product")
    products.update_one({"_id": doc["_id"]}, {"$set": payload.model_dump()})
    updated = serialize_id(products.find_one({"_id": doc["_id"]}))
    return {
        "id": updated["id"],
        "title": updated["title"],
        "description": updated.get("description",""),
        "category": updated["category"],
        "price": float(updated["price"]),
        "image": updated.get("image", "placeholder.jpg"),
        "owner_email": updated["owner_email"],
    }

@router.delete("/{product_id}")
def delete_product(product_id: str, email: str = Depends(get_current_user_email)):
    doc = products.find_one({"_id": oid(product_id)})
    if not doc: raise HTTPException(status_code=404, detail="Not found")
    if doc["owner_email"] != email:
        raise HTTPException(status_code=403, detail="Not your product")
    products.delete_one({"_id": doc["_id"]})
    return {"message": "Deleted"}
