from pydantic import BaseModel, ConfigDict, Field


class GradeBase(BaseModel):
    name: str = Field(..., description="Full name of the academic grade")
    tag: str = Field(..., description="Short tag/abbreviation for the grade")
    level_id: int = Field(..., description="ID of the associated educational level", alias="levelId")

    model_config = ConfigDict(populate_by_name=True)


class GradeCreate(GradeBase):
    pass


class GradeRead(GradeBase):
    id: int = Field(..., description="Grade ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class GradeUpdate(GradeBase):
    name: str | None = Field(None, description="Full name of the academic grade")
    tag: str | None = Field(None, description="Short tag/abbreviation for the grade")
    level_id: int | None = Field(None, description="ID of the associated educational level", alias="levelId")

    model_config = ConfigDict(populate_by_name=True)