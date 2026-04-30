import re
from datetime import date, datetime
from app.core.enums import Gender, EmployeePosition

from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator


class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50, description="First name of the employee", alias="firstName")
    last_name: str = Field(..., min_length=2, max_length=50, description="Last name of the employee", alias="lastName")
    dni: str = Field(..., min_length=8, max_length=15, pattern=r'^\d{8,15}$', description="DNI of the employee")
    ruc: str | None = Field(None, min_length=11, max_length=11, pattern=r'^\d{11}$', description="RUC of the employee")
    gender: Gender = Field(..., description="Gender of the employee")
    birth_date: date | None = Field(None, description="Birth date of the employee", alias="birthDate")
    address: str | None = Field(None, min_length=2, max_length=75, description="Address of the employee")
    phone_number: str = Field(..., min_length=6, max_length=15, pattern=r'^\+?\d{6,14}$', description="Phone number of the employee", alias="phoneNumber")
    email: EmailStr | None = Field(None, max_length=50, description="Email of the employee")
    is_active: bool = Field(default=True, description="Active status of the employee", alias="isActive")
    position: EmployeePosition = Field(..., description="Position of the employee")

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    @field_validator('first_name', 'last_name')
    @classmethod
    def clean_names(cls, v: str) -> str:
        # Reemplazar múltiples espacios por uno solo y quitar espacios en los bordes
        v = " ".join(v.split())
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', v):
            raise ValueError("El texto solo puede contener letras y espacios")
        return v

    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v: date | None) -> date | None:
        if v is None:
            return v
        today = date.today()
        if v >= today:
            raise ValueError("La fecha de nacimiento debe estar en el pasado")
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError("El empleado debe ser mayor de 18 años")
        return v


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int = Field(..., description="ID of the employee")
    created_at: datetime = Field(..., description="Creation timestamp of the employee", alias="createdAt")
    updated_at: datetime = Field(..., description="Update timestamp of the employee", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class EmployeeUpdate(EmployeeBase):
    first_name: str | None = Field(None, min_length=2, max_length=50, description="First name of the employee", alias="firstName")
    last_name: str | None = Field(None, min_length=2, max_length=50, description="Last name of the employee", alias="lastName")
    dni: str | None = Field(None, min_length=8, max_length=15, pattern=r'^\d{8,15}$', description="DNI of the employee")
    ruc: str | None = Field(None, min_length=11, max_length=11, pattern=r'^\d{11}$', description="RUC of the employee")
    gender: Gender | None = Field(None, description="Gender of the employee")
    birth_date: date | None = Field(None, description="Birth date of the employee", alias="birthDate")
    address: str | None = Field(None, min_length=2, max_length=75, description="Address of the employee")
    phone_number: str | None = Field(None, min_length=6, max_length=15, pattern=r'^\+?\d{6,14}$', description="Phone number of the employee", alias="phoneNumber")
    email: EmailStr | None = Field(None, max_length=50, description="Email of the employee")
    is_active: bool | None = Field(None, description="Active status of the employee", alias="isActive")
    position: EmployeePosition | None = Field(None, description="Position of the employee")

    @field_validator('first_name', 'last_name')
    @classmethod
    def clean_names_update(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = " ".join(v.split())
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', v):
            raise ValueError("El texto solo puede contener letras y espacios")
        return v
