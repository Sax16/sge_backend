from pydantic import BaseModel, ConfigDict, Field


class ChargeCatalogBase(BaseModel):
    name: str = Field(..., description="Charge name")
    is_active: bool = Field(default=True, description="Is charge active", alias="isActive")

    model_config = ConfigDict(populate_by_name=True)


class ChargeCatalogCreate(ChargeCatalogBase):
    pass


class ChargeCatalogRead(ChargeCatalogBase):
    id: int = Field(..., description="Charge Catalog ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ChargeCatalogUpdate(ChargeCatalogBase):
    name: str | None = Field(None, description="Charge name")
    is_active: bool | None = Field(None, description="Is charge active", alias="isActive")

    model_config = ConfigDict(populate_by_name=True)