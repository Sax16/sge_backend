from app.core.enums import LevelAcademicType
from pydantic import BaseModel, ConfigDict, Field


class LevelBase(BaseModel):
    name: str = Field(..., description="Full name of the educational level")
    modular_code: str | None = Field(None, description="Modular code for the level", alias="modularCode")
    tag: str = Field(..., description="Short tag/abbreviation for the level")
    type: LevelAcademicType = Field(..., description="Type or modality of the level")

    model_config = ConfigDict(populate_by_name=True)


class LevelCreate(LevelBase):
    pass


class LevelRead(LevelBase):
    id: int = Field(..., description="Level ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class LevelUpdate(LevelBase):
    name: str | None = Field(None, description="Full name of the educational level")
    modular_code: str | None = Field(None, description="Modular code for the level", alias="modularCode")
    tag: str | None = Field(None, description="Short tag/abbreviation for the level")

    model_config = ConfigDict(populate_by_name=True)