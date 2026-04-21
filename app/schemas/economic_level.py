from pydantic import BaseModel, ConfigDict, Field


class EconomicLevelBase(BaseModel):
    name: str = Field(..., description="Level name")
    description: str | None = Field(None, description="Detailed description")

    model_config = ConfigDict(populate_by_name=True)


class EconomicLevelCreate(EconomicLevelBase):
    pass


class EconomicLevelRead(EconomicLevelBase):
    id: int = Field(..., description="Economic Level ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class EconomicLevelUpdate(EconomicLevelBase):
    name: str | None = Field(None, description="Level name")
    description: str | None = Field(None, description="Detailed description")

    model_config = ConfigDict(populate_by_name=True)