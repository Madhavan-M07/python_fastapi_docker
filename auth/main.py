from fastapi import FastAPI , Depends , HTTPException , status
from sqlalchemy.orm import Session
import models ,schemas ,utlis  
from auth_database import get_db
from jose import jwt
from datetime import datetime , timedelta
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import JWTError


SECRET_KEY = "XXOZNhjEUWL1t0IZfr6g35D6IEdVndEJunhRe39Tqjg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# HELPER FUNCTION THAT TAKES USER DATA
def create_access_token(data: dict):
    to_encode = data.copy()
    # Here we can add an expiration time to the token if needed
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"exp": expire})
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


app = FastAPI()

@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(models.User).filter(models.User.userName == user.userName).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

#Has the password
    hashed_password = utlis.get_password_hash(user.password)

    # Create a new user instance
    new_user = models.User(
        userName=user.userName,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'id': new_user.id, 'userName': new_user.userName, 'email': new_user.email, 'role': new_user.role}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userName == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not utlis.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password haha :)")

    token_data = {"sub": user.userName, "role": user.role}
    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return{"username": username, "role": role}
  

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['username']}! You have accessed a protected route.", "role": current_user['role']}
  
def required_role(required_role: list):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in required_role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user
    return role_checker


@app.get("/profile")
def profile_route(current_user: dict = Depends(required_role(["user", "admin"]))):
    return {"message": f"Hello {current_user['username']}! You have accessed your profile.", "role": current_user['role']}


@app.get("/user/dashboard")
def user_dashboard(current_user: dict = Depends(required_role(["user"]))):
    return {"message": f"Welcome to the user dashboard, {current_user['username']}!", "role": current_user['role']}


@app.get("/admin/dashboard")
def admin_dashboard(current_user: dict = Depends(required_role(["admin"]))):
    return {"message": f"Welcome to the admin dashboard, {current_user['username']}!", "role": current_user['role']}