from pydantic import BaseModel, ConfigDict, Field


class EconomicLevelBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=15, description="Level name")
    description: str | None = Field(None, min_length=2, max_length=75, description="Detailed description")

    model_config = ConfigDict(populate_by_name=True)


class EconomicLevelCreate(EconomicLevelBase):
    pass


class EconomicLevelRead(EconomicLevelBase):
    id: int = Field(..., description="Economic Level ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class EconomicLevelUpdate(EconomicLevelBase):
    name: str | None = Field(None, min_length=2, max_length=15, description="Level name")
    description: str | None = Field(None, min_length=2, max_length=75, description="Detailed description")

    model_config = ConfigDict(populate_by_name=True)