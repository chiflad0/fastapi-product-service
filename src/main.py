from fastapi import FastAPI
from src.api import main_router


def create_application() -> FastAPI:
    application = FastAPI(
        title="Tasks",
        description="Tasks service",
        version="0.0.1"
    )
    app.include_router(main_router)
    return application


app = create_application()
