from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ChargeCatalogAmountBase(BaseModel):
    charge_catalog_id: int = Field(..., description="Charge Catalog ID", alias="chargeCatalogId")
    economic_level_id: int | None = Field(None, description="Economic Level ID", alias="economicLevelId")
    amount: Decimal = Field(..., description="Amount")

    model_config = ConfigDict(populate_by_name=True)


class ChargeCatalogAmountCreate(ChargeCatalogAmountBase):
    pass


class ChargeCatalogAmountRead(ChargeCatalogAmountBase):
    id: int = Field(..., description="Charge Catalog Amount ID")
    created_at: datetime = Field(..., description="Record creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ChargeCatalogAmountUpdate(ChargeCatalogAmountBase):
    charge_catalog_id: int | None = Field(None, description="Charge Catalog ID", alias="chargeCatalogId")
    economic_level_id: int | None = Field(None, description="Economic Level ID", alias="economicLevelId")
    amount: Decimal | None = Field(None, description="Amount")

    model_config = ConfigDict(populate_by_name=True)