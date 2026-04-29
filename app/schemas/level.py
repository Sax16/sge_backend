from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import LevelAcademicType


class LevelBase(BaseModel):
    name: str = Field(..., max_length=25, description="Full name of the educational level")
    modular_code: str | None = Field(None, max_length=20, description="Modular code for the level", alias="modularCode")
    tag: str = Field(..., max_length=10, description="Short tag/abbreviation for the level")

    model_config = ConfigDict(populate_by_name=True)


class LevelCreate(LevelBase):
    type: LevelAcademicType = Field(..., description="Type or modality of the level")


class LevelRead(LevelBase):
    id: int = Field(..., description="Level ID")
    type: LevelAcademicType = Field(..., description="Type or modality of the level")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class LevelUpdate(LevelBase):
    name: str | None = Field(None, max_length=25, description="Full name of the educational level")
    modular_code: str | None = Field(None, max_length=20, description="Modular code for the level", alias="modularCode")
    tag: str | None = Field(None, max_length=10, description="Short tag/abbreviation for the level")

    model_config = ConfigDict(populate_by_name=True)