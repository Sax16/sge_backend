from fastapi import APIRouter

from app.api.v1.endpoints import employees, users


router = APIRouter()

router.include_router(employees.router, prefix="/employees", tags=["Employees"])
router.include_router(users.router, prefix="/users", tags=["Users"])
