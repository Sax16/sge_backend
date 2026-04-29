from pydantic import BaseModel, ConfigDict, Field


class GradeBase(BaseModel):
    name: str = Field(..., max_length=25, description="Full name of the academic grade")
    tag: str = Field(..., max_length=10, description="Short tag/abbreviation for the grade")
    level_id: int = Field(..., description="ID of the associated educational level", alias="levelId")

    model_config = ConfigDict(populate_by_name=True)


class GradeCreate(GradeBase):
    pass


class GradeRead(GradeBase):
    id: int = Field(..., description="Grade ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class GradeUpdate(GradeBase):
    name: str | None = Field(None, max_length=25, description="Full name of the academic grade")
    tag: str | None = Field(None, max_length=10, description="Short tag/abbreviation for the grade")
    level_id: int | None = Field(None, description="ID of the associated educational level", alias="levelId")

    model_config = ConfigDict(populate_by_name=True)