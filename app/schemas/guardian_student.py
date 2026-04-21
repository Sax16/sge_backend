from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import RelationshipType


class GuardianStudentBase(BaseModel):
    student_id: int = Field(..., description="Student ID", alias="studentId")
    guardian_id: int = Field(..., description="Guardian ID", alias="guardianId")
    relationship_type: RelationshipType = Field(..., description="Type of relationship", alias="relationshipType")

    model_config = ConfigDict(populate_by_name=True)


class GuardianStudentCreate(GuardianStudentBase):
    pass


class GuardianStudentRead(GuardianStudentBase):
    id: int = Field(..., description="Association ID")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class GuardianStudentUpdate(GuardianStudentBase):
    student_id: int | None = Field(None, description="Student ID", alias="studentId")
    guardian_id: int | None = Field(None, description="Guardian ID", alias="guardianId")
    relationship_type: RelationshipType | None = Field(None, description="Type of relationship", alias="relationshipType")

    model_config = ConfigDict(populate_by_name=True)