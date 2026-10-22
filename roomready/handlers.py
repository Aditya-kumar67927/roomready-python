
"""Convert domain and validation errors into problem+json responses."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from roomready.errors import DomainError, FILTER


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(
        request: Request, exc: DomainError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status,
            media_type="application/problem+json",
            content={
                "type": exc.type,
                "title": exc.title,
                "status": exc.status,
                "detail": exc.detail,
                **exc.extra,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        status, problem_type, title = FILTER
        return JSONResponse(
            status_code=status,
            media_type="application/problem+json",
            content={
                "type": problem_type,
                "title": title,
                "status": status,
                "detail": "One or more query or path parameters are invalid.",
            },
        )
