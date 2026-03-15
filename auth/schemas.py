from pydantic import BaseModel, EmailStr


#Schema for user creation
class UserCreate(BaseModel):
    userName: str
    email: EmailStr
    password: str
    role: str

#Schema for user login
class UserLogin(BaseModel):
   userName: str
   password: str