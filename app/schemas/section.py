from pydantic import BaseModel, ConfigDict, Field



class SectionBase(BaseModel):
    id: str = Field(..., description="Section code (e.g., '1A', '2B')")
    name: str = Field(..., description="Full name of the section")
    tag: str = Field(..., description="Short tag/abbreviation for the section")
    grade_id: int = Field(..., description="ID of the associated grade", alias="gradeId")

    model_config = ConfigDict(populate_by_name=True)


class SectionCreate(SectionBase):
    pass


class SectionRead(SectionBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SectionUpdate(SectionBase):
    id: str | None = Field(None, description="Section code (e.g., '1A', '2B')")
    name: str | None = Field(None, description="Full name of the section")
    tag: str | None = Field(None, description="Short tag/abbreviation for the section")
    grade_id: int | None = Field(None, description="ID of the associated grade", alias="gradeId")

    model_config = ConfigDict(populate_by_name=True)