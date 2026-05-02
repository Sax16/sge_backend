from pydantic import BaseModel, ConfigDict, Field, field_validator



class SectionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=15, description="Full name of the section")
    tag: str = Field(..., min_length=1, max_length=10, description="Short tag/abbreviation for the section")
    grade_id: int = Field(..., description="ID of the associated grade", alias="gradeId")

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().title()
        return v

    @field_validator("tag", mode="before")
    @classmethod
    def validate_tag(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip().upper()
        return v

    model_config = ConfigDict(populate_by_name=True)


class SectionCreate(SectionBase):
    pass


class SectionRead(SectionBase):
    id: str = Field(..., max_length=6, description="Section code (e.g., 'SR-001', 'SE-001')")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SectionUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=15, description="Full name of the section")
    tag: str | None = Field(None, min_length=1, max_length=10, description="Short tag/abbreviation for the section")

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            return v.strip().title()
        return v

    @field_validator("tag", mode="before")
    @classmethod
    def validate_tag(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            return v.strip().upper()
        return v

    model_config = ConfigDict(populate_by_name=True)