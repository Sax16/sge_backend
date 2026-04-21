from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import EnrollmentStatus
from app.models.base import Base


class Enrollment(Base):
    """
    Enrollment model representing a student's enrollment in a specific period, section, and payment scheme.
    """
    __tablename__ = "enrollment"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Enrollment ID")
    payment_scheme_id = Column(Integer, ForeignKey("payment_scheme.id", ondelete="RESTRICT"), nullable=False, index=True, comment="Payment Scheme ID")
    academic_period_id = Column(Integer, ForeignKey("academic_period.id", ondelete="RESTRICT"), nullable=False, index=True, comment="Academic Period ID")
    date = Column(Date, nullable=False, comment="Date of enrollment")
    section_id = Column(String(6), ForeignKey("section.id", ondelete="RESTRICT"), nullable=False, index=True, comment="Section ID")
    student_id = Column(Integer, ForeignKey("student.id", ondelete="RESTRICT"), nullable=False, index=True, comment="Student ID")
    user_id = Column(SmallInteger, ForeignKey("user.id", ondelete="RESTRICT"), nullable=False, index=True, comment="User ID who registered enrollment")
    status = Column(Enum(EnrollmentStatus), nullable=False, default=EnrollmentStatus.ACTIVO, comment="Status of the enrollment")
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now(), comment="Record creation timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Last update timestamp")

    payment_scheme = relationship("PaymentScheme", back_populates="enrollments")
    academic_period = relationship("AcademicPeriod", back_populates="enrollments")
    section = relationship("Section", back_populates="enrollments")
    student = relationship("Student", back_populates="enrollments")
    user = relationship("User", back_populates="enrollments")
