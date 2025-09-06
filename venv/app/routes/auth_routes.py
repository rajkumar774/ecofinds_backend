from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import SignUpIn, LoginOut, UserOut
from app.database import users
from app.auth import hash_password, verify_password, make_token
from app.utils import serialize_id

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(payload: SignUpIn):
    if users.find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    doc = {"email": payload.email, "password": hash_password(payload.password)}
    res = users.insert_one(doc)
    user = users.find_one({"_id": res.inserted_id})
    return {"message": "User created", "user": serialize_id(user)}

@router.post("/login", response_model=LoginOut)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users.find_one({"email": form.username})
    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": make_token(user["email"]), "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(token: str):
    # Allow quick “token check” without OAuth2 flow in Swagger
    import jose
    from jose import jwt
    from app.auth import JWT_SECRET, ALGO
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
        email = payload.get("sub")
        user = users.find_one({"email": email})
        if not user: raise Exception()
        user = serialize_id(user)
        return {"id": user["id"], "email": user["email"]}
    except jose.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
