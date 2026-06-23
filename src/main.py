from fastapi import FastAPI
from src.api import main_router


def create_application() -> FastAPI:
    application = FastAPI(
        title="Product Service API",
        # description="Product service",
        version="0.0.1"
    )
    application.include_router(main_router)
    return application


app = create_application()
