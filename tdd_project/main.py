from fastapi import FastAPI

from tdd_project.core.config import settings
from tdd_project.routers import api_router


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            version="0.0.1",
            title=settings.PROJECT_NAME,
            # root_path=settings.ROOT_PATH
        )


app = App()
app.include_router(api_router)


# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

# @app.get("/docs")
# def read_docs():
#     return {"message": "Docs Page"}
