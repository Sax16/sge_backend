from enum import Enum


class Gender(str, Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


class EmployeePosition(str, Enum):
    DOCENTE = "Docente"
    AUXILIAR = "Auxiliar"
    SECRETARIA = "Secretaria"
    DIRECTOR = "Director"
    SUBDIRECTOR = "Subdirector"
    PSICOLOGO = "Psicologo"
    PROMOTOR = "Promotor"
    ADMINISTRATIVO = "Administrativo"
    OTRO = "Otro"


class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"


class LevelAcademicType(str, Enum):
    REGULAR = "Regular"
    EXTRAORDINARIO = "Extraordinario"


class AcademicPeriodType(str, Enum):
    REGULAR = "Regular"
    COMPLEMENTARIO = "Complementario"
    OTRO = "Otro"


class StudentStatus(str, Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    RETIRADO = "Retirado"
    EGRESADO = "Egresado"


class ExpenseType(str, Enum):
    ADMINISTRATIVO = "Administrativo"
    ACADEMICO = "Académico"
    SERVICIOS = "Servicios"
    OTRO = "Otro"


class ManagementType(str, Enum):
    PRIVADO = "Privada"
    PUBLICO = "Pública"
    OTRO = "Otro"


class Ugel(str, Enum):
    SATIPO = "Satipo"
    RIO_TAMBO = "Rio Tambo"
    RIO_NEGRO = "Rio Negro"
    LA_MERCED = "La Merced"
    CONCEPCION = "Concepcion"
    JAUJA = "Jauja"
    PICHANAKI = "Pichanaki"
    MAZAMARI = "Mazamari"
    HUANCAYO = "Huancayo"
    PANGOA = "Pangoa"
    OTRO = "Otro"

class RelationshipType(str, Enum):
    PADRE = "Padre"
    MADRE = "Madre"
    TIO = "Tio"
    TIA = "Tia"
    ABUELO = "Abuelo"
    ABUELA = "Abuela"
    HERMANO = "Hermano"
    HERMANA = "Hermana"
    TUTOR = "Tutor"
    APODERADO = "Apoderado"
    OTRO = "Otro"

class EnrollmentStatus(str, Enum):
    ACTIVO = "Activo"
    PENDIENTE = "Pendiente"
    RESERVADO = "Reservado"
    FINALIZADO = "Finalizado"
    RETIRADO = "Retirado"

class ChargeStatus(str, Enum):
    PENDIENTE = "Pendiente"
    PAGADO = "Pagado"
    VENCIDO = "Vencido"
    ANULADO = "Anulado"
    PARCIAL = "Parcial"

class ReceiptType(str, Enum):
    BOLETA = "Boleta"
    FACTURA = "Factura"
    OTRO = "Otro"

class PaymentMethod(str, Enum):
    EFECTIVO = "Efectivo"
    TARJETA = "Tarjeta"
    TRANSFERENCIA = "Transferencia"
    OTRO = "Otro"

    