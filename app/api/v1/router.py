from fastapi import APIRouter

from app.api.v1.endpoints import (
    employees, users, auth, expenses, school, academic_periods, charges,
    charge_catalogs, charge_catalog_amounts, charge_discounts, discounts,
    economic_levels, enrollments, grades, guardians, guardian_students,
    levels, payment_employees, payment_schedules, payment_schemes,
    receipts, receipt_lines, sections, students
)

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(employees.router, prefix="/employees", tags=["Employees"])
router.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
router.include_router(school.router, prefix="/school", tags=["School"])
router.include_router(academic_periods.router, prefix="/academic-periods", tags=["Academic Periods"])
router.include_router(charges.router, prefix="/charges", tags=["Charges"])
router.include_router(charge_catalogs.router, prefix="/charge-catalogs", tags=["Charge Catalogs"])
router.include_router(charge_catalog_amounts.router, prefix="/charge-catalog-amounts", tags=["Charge Catalog Amounts"])
router.include_router(charge_discounts.router, prefix="/charge-discounts", tags=["Charge Discounts"])
router.include_router(discounts.router, prefix="/discounts", tags=["Discounts"])
router.include_router(economic_levels.router, prefix="/economic-levels", tags=["Economic Levels"])
router.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])
router.include_router(grades.router, prefix="/grades", tags=["Grades"])
router.include_router(guardians.router, prefix="/guardians", tags=["Guardians"])
router.include_router(guardian_students.router, prefix="/guardian-students", tags=["Guardian Students"])
router.include_router(levels.router, prefix="/levels", tags=["Levels"])
router.include_router(payment_employees.router, prefix="/payment-employees", tags=["Payment Employees"])
router.include_router(payment_schedules.router, prefix="/payment-schedules", tags=["Payment Schedules"])
router.include_router(payment_schemes.router, prefix="/payment-schemes", tags=["Payment Schemes"])
router.include_router(receipts.router, prefix="/receipts", tags=["Receipts"])
router.include_router(receipt_lines.router, prefix="/receipt-lines", tags=["Receipt Lines"])
router.include_router(sections.router, prefix="/sections", tags=["Sections"])
router.include_router(students.router, prefix="/students", tags=["Students"])
