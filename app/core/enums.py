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


class SectionType(str, Enum):
    REGULAR = "Regular"
    EXTRAORDINARIO = "Extraordinario"
    OTRO = "Otro"


class AcademicPeriodType(str, Enum):
    REGULAR = "Regular"
    COMPLEMENTARIO = "Complementario"
    OTRO = "Otro"


class EconomicLevel(str, Enum):
    PRIMERO = "Nivel I"
    SEGUNDO = "Nivel II"
    TERCERO = "Nivel III"
    CUARTO = "Nivel IV"
    QUINTO = "Nivel V"


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