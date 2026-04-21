from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import UserRole


class UserBase(BaseModel):
    username: str = Field(..., description="Username of the user")
    is_active: bool = Field(..., description="Active status of the user", alias="isActive")
    role: UserRole = Field(..., description="Role of the user")

    model_config = ConfigDict(populate_by_name=True)


class UserCreate(UserBase):
    password: str = Field(..., description="Password of the user")
    employee_id: int = Field(..., description="ID of the associated employee", alias="employeeId")


class UserRead(UserBase):
    id: int = Field(..., description="ID of the user")
    employee_id: int = Field(..., description="ID of the associated employee", alias="employeeId")
    created_at: datetime = Field(..., description="Creation timestamp of the user", alias="createdAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserUpdate(UserBase):
    username: str | None = Field(None, description="Username of the user")
    is_active: bool | None = Field(None, description="Active status of the user", alias="isActive")
    role: UserRole | None = Field(None, description="Role of the user")
    password: str | None = Field(None, description="Password of the user")
