from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

TrimmedString25 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=25)]
TrimmedString10 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=10)]


class GradeBase(BaseModel):
    name: TrimmedString25 = Field(..., description="Full name of the academic grade")
    tag: TrimmedString10 = Field(..., description="Short tag/abbreviation for the grade")
    level_id: int = Field(..., gt=0, description="ID of the associated educational level", alias="levelId")

    model_config = ConfigDict(populate_by_name=True)


class GradeCreate(GradeBase):
    pass


class GradeRead(GradeBase):
    id: int = Field(..., description="Grade ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class GradeUpdate(BaseModel):
    name: TrimmedString25 | None = Field(None, description="Full name of the academic grade")
    tag: TrimmedString10 | None = Field(None, description="Short tag/abbreviation for the grade")

    model_config = ConfigDict(populate_by_name=True)