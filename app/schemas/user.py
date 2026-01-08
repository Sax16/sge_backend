from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field



class UserBase(BaseModel):
    user_name: str = Field(..., description="Username of the user")
    is_active: bool = Field(..., description="Active status of the user")
    employee_id: int = Field(..., description="ID of the associated employee")


class UserCreate(UserBase):
    password: str = Field(..., description="Password of the user")
    created_at: datetime = Field(default_factory=datetime.now)


class UserRead(UserBase):
    id: int = Field(..., description="ID of the user")
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)
