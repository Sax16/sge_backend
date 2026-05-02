from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import LevelAcademicType


class LevelBase(BaseModel):
    name: str = Field(..., min_length=4, max_length=15, description="Full name of the educational level")
    modular_code: str | None = Field(None, min_length=5, max_length=20, pattern=r"^[a-zA-Z0-9]+$", description="Modular code for the level", alias="modularCode")
    tag: str = Field(..., min_length=2, max_length=10, description="Short tag/abbreviation for the level")
    type: LevelAcademicType = Field(..., description="Type or modality of the level")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("name", "tag", mode="before")
    @classmethod
    def strip_and_format_strings(cls, v, info):
        if isinstance(v, str):
            v = v.strip()
            if info.field_name == "tag":
                v = v.upper()
        return v

    @field_validator("modular_code", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return None
        return v


class LevelCreate(LevelBase):
    pass

class LevelRead(LevelBase):
    id: int = Field(..., description="Level ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class LevelUpdate(BaseModel):
    name: str | None = Field(None, min_length=4, max_length=15, description="Full name of the educational level")
    modular_code: str | None = Field(None, min_length=5, max_length=20, pattern=r"^[a-zA-Z0-9]+$", description="Modular code for the level", alias="modularCode")
    tag: str | None = Field(None, min_length=2, max_length=10, description="Short tag/abbreviation for the level")

    model_config = ConfigDict(populate_by_name=True)