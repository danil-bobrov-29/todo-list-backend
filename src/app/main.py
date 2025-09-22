import uvicorn

from src.app.adapters.api.fastapi_app import create_app
from src.app.core.config import settings

app = create_app()


# Для разработки из-под виртуального окружения.
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=True,
    )
