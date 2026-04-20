from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.enums import RelationshipType
from app.models.base import Base


class GuardianStudent(Base):
    """
    Association model representing the relationship between a Guardian and a Student.

    Attributes:
        id: Primary key, auto-incremented
        student_id: Foreign key to the student model
        guardian_id: Foreign key to the guardian model
        relationship_type: Type of relationship (e.g., PADRE, MADRE, TUTOR)
    """
    __tablename__ = "guardian_student"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Association ID")
    student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"), nullable=False, index=True, comment="Student ID")
    guardian_id = Column(Integer, ForeignKey("guardian.id", ondelete="CASCADE"), nullable=False, index=True, comment="Guardian ID")
    relationship_type = Column(Enum(RelationshipType), nullable=False, comment="Type of relationship")

    student = relationship("Student", back_populates="guardians")
    guardian = relationship("Guardian", back_populates="students")
