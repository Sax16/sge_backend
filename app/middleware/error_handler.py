from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Manejador personalizado para errores de validación de Pydantic.
    Devuelve un JSON con un mensaje más amigable y estructurado.
    """
    errors = []
    for error in exc.errors():
        field = error.get("loc", ["unknown"])[-1]
        msg = error.get("msg", "Error de validación")
        type_ = error.get("type", "unknown")

        # Personalizar mensajes específicos
        loc = error.get("loc", [])
        
        # Verificar si el error es sobre el campo 'email'
        if type_ == "value_error.email" or "email" in type_ or ("email" in loc):
            msg = "El formato del correo electrónico no es válido."
        
        errors.append({
            "field": field,
            "message": msg,
            "type": type_
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación en los datos enviados.",
            "errors": errors
        },
    )
