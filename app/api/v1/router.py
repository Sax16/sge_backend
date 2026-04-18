from fastapi import APIRouter

from app.api.v1.endpoints import employees, users, auth, expenses, school


router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(employees.router, prefix="/employees", tags=["Employees"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
router.include_router(school.router, prefix="/school", tags=["School"])
