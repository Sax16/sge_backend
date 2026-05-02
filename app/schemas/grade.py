from pydantic import BaseModel, ConfigDict, Field


class GradeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=15, strip_whitespace=True, description="Full name of the academic grade")
    tag: str = Field(..., min_length=2, max_length=10, strip_whitespace=True, description="Short tag/abbreviation for the grade")
    level_id: int = Field(..., gt=0, description="ID of the associated educational level", alias="levelId")

    model_config = ConfigDict(populate_by_name=True)


class GradeCreate(GradeBase):
    pass


class GradeRead(GradeBase):
    id: int = Field(..., description="Grade ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class GradeUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=15, strip_whitespace=True, description="Full name of the academic grade")
    tag: str | None = Field(None, min_length=2, max_length=10, strip_whitespace=True, description="Short tag/abbreviation for the grade")

    model_config = ConfigDict(populate_by_name=True)