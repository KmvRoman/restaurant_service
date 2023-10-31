from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.infrastructure.database.exceptions.product import DatabaseException
from src.presentation.web.exceptions.application.basket import WebApplicationError


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


async def database_exception(_: Request, exc: DatabaseException) -> JSONResponse:
    return JSONResponse({"errors": [exc.message]}, status_code=412)


async def application_error(_: Request, exc: WebApplicationError) -> JSONResponse:
    return JSONResponse({"errors": [exc.message]}, status_code=400)
