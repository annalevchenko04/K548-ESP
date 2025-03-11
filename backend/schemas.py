from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional


class UserCreate(BaseModel):
    username: str
    name: str
    surname: str
    age: int
    gender: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    role: str

    # Member-specific fields
    membership_status: Optional[str] = None


class Member(BaseModel):
    membership_status: Optional[str]


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    age: int
    gender: str
    email: EmailStr
    phone: Optional[str]
    role: str
    member_details: Optional[Member] = None

    class Config:
        from_attributes = True



class Question(BaseModel):
    id: str
    text: str
    unit: str
    type: str  # "range", "single_value", "dropdown", etc.
    options: Optional[List[str]] = None
    default_value: Optional[float] = None

class CarbonFootprintRequest(BaseModel):
    answers: Dict[str, str | float]