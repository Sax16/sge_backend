from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field



class UserBase(BaseModel):
    user_name: str = Field(..., description="Username of the user", alias="userName")
    is_active: bool = Field(..., description="Active status of the user", alias="isActive")
    employee_id: int = Field(..., description="ID of the associated employee", alias="employeeId")
    password: str = Field(..., description="Password of the user")

    model_config = ConfigDict(populate_by_name=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int = Field(..., description="ID of the user")
    created_at: datetime = Field(..., description="Creation timestamp of the user", alias="createdAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserUpdate(UserBase):
    pass