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
    