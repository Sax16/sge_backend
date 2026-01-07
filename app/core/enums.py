from enum import Enum

# Enum for gender
class GenderEnum(str, Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


class PositionEnum(str, Enum):
    DOCENTE = "Docente"
    AUXILIAR = "Auxiliar"
    SECRETARIA = "Secretaria"
    DIRECTOR = "Director"
    SUBDIRECTOR = "Subdirector"
    PSICOLOGO = "Psicologo"
    PROMOTOR = "Promotor"
    ADMINISTRATIVO = "Administrativo"
    OTRO = "Otro"
