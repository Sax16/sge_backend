import os
import sys
from datetime import date

# Añadir el directorio raíz al path para poder importar los módulos de app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.employee import Employee
from app.models.user import User
from app.core.enums import Gender, EmployeePosition, UserRole

def seed_database():
    db = SessionLocal()
    try:
        # Verificar si ya existe al menos un usuario (para evitar duplicados al ejecutar varias veces)
        existing_user = db.query(User).first()
        if existing_user:
            print("La base de datos ya contiene usuarios. No se requiere inicialización.")
            return

        print("Iniciando el seeding de la base de datos...")
        
        # 1. Crear el Empleado inicial (Requisito para crear un Usuario por la Foreign Key)
        new_employee = Employee(
            first_name="Admin",
            last_name="Super",
            dni="00000000", # Cambiar por el DNI real si es necesario
            gender=Gender.MASCULINO,
            birth_date=date(1990, 1, 1),
            phone_number="999888777",
            email="admin@elohimsge.com",
            position=EmployeePosition.ADMINISTRATIVO
        )
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        print(f"✅ Empleado creado exitosamente con ID: {new_employee.id}")

        # 2. Crear el Usuario asociado (Super Admin) encriptando la contraseña
        new_user = User(
            username="admin",
            password=get_password_hash("admin123"), # Aquí se encripta la contraseña
            role=UserRole.SUPER_ADMIN,
            employee_id=new_employee.id
        )
        db.add(new_user)
        db.commit()
        print(f"✅ Usuario ({new_user.username}) creado exitosamente.")

        print("🎉 Seeding completado con éxito.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error al inicializar la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
