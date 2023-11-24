from typing import Any, Optional, Dict, no_type_check

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.openapi.utils import get_openapi

from src.infrastructure.cache.redis_cache import RedisConnect, RedisCacheSystem
from src.infrastructure.config.config import Config, make_fastapi_instance_kwargs
from src.infrastructure.database.exceptions.product import DatabaseException
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.ioc.ioc import IoC
from src.presentation.web.api import routers
from src.presentation.web.api.v1.dependencies.dependencies import IocDependencyMarker, UserRepositoryDependencyMarker
from src.presentation.web.error_handlers.http422 import http422_error_handler
from src.presentation.web.error_handlers.http_error import http_error_handler, database_exception, application_error
from src.presentation.web.exceptions.application.basket import WebApplicationError
from src.presentation.web.middlewares.process_time_middleware import add_process_time_header

ALLOWED_METHODS = ["POST", "PUT", "DELETE", "GET"]


class DevelopmentApplicationBuilder:
    """Class, that provides the installation of FastAPI application"""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.app: FastAPI = FastAPI(**make_fastapi_instance_kwargs(self.config.server))
        self.app.config = self.config  # type: ignore
        self._openapi_schema: Optional[Dict[str, Any]] = None

    @no_type_check
    def setup_middlewares(self):
        self.app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)

    def configure_openapi_schema(self) -> None:
        self._openapi_schema = get_openapi(
            title="Cube API",
            version="0.0.1",
            description="This is a very custom OpenAPI schema",
            routes=self.app.routes,
        )
        self._openapi_schema["info"]["x-logo"] = {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
        }
        self.app.openapi_schema = self._openapi_schema

    @no_type_check
    def configure_routes(self):
        [self.app.include_router(router) for router in routers]

    def configure_exception_handlers(self) -> None:
        self.app.add_exception_handler(RequestValidationError, http422_error_handler)
        self.app.add_exception_handler(HTTPException, http_error_handler)
        self.app.add_exception_handler(DatabaseException, database_exception)
        self.app.add_exception_handler(WebApplicationError, application_error)

    def configure_application_state(self) -> None:
        engine = create_async_engine(url=self.config.database.connection_uri)
        session_make = sessionmaker(  # NOQA
            engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
        )
        user_repo = UserRepository(session_or_pool=session_make)

        redis_connect = RedisConnect(
            host=self.config.redis.host, port=self.config.redis.port,
            password=self.config.redis.password, db=self.config.redis.db,
        )
        redis = RedisCacheSystem(redis=redis_connect())

        ioc = IoC(db_gateway=user_repo, redis_cache=redis, config=self.config)

        self.app.dependency_overrides.update(
            {
                IocDependencyMarker: lambda: ioc,
                UserRepositoryDependencyMarker: lambda: user_repo,
            }
        )


class Director:
    def __init__(self, builder: DevelopmentApplicationBuilder) -> None:
        if not isinstance(builder, DevelopmentApplicationBuilder):
            raise TypeError("You passed on invalid builder")
        self._builder = builder

    @property
    def builder(self) -> DevelopmentApplicationBuilder:
        return self._builder

    @builder.setter
    def builder(self, new_builder: DevelopmentApplicationBuilder):
        self._builder = new_builder

    def build_app(self) -> FastAPI:
        self.builder.configure_routes()
        self.builder.setup_middlewares()
        self.builder.configure_application_state()
        self.builder.configure_exception_handlers()
        return self.builder.app
