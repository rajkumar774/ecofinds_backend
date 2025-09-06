import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, products_routes, cart_routes, purchase_routes

app = FastAPI(title="EcoFinds Backend", version="1.0.0")

# CORS
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(products_routes.router)
app.include_router(cart_routes.router)
app.include_router(purchase_routes.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "EcoFinds Backend"}
