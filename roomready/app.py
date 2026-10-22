
"""The RoomReady application: configure the database, seed data, mount routes,
and install error handlers."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from roomready.settings import Settings
from roomready.db import init_db, make_engine, make_sessionmaker
from roomready.services.seed import seed
from roomready.routers.rooms import router as rooms_router
from roomready.handlers import install_error_handlers


def create_app(clock=None) -> FastAPI:
    settings = Settings()
    engine = make_engine(settings.database_url)
    session_factory = make_sessionmaker(engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_db(engine)

        with session_factory() as session:
            seed(session, settings.seed_dir)

        yield

        engine.dispose()

    app = FastAPI(
        title="RoomReady",
        lifespan=lifespan,
    )

    app.state.sessionmaker = session_factory

    app.include_router(rooms_router)
    install_error_handlers(app)

    return app
