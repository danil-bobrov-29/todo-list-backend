from fastapi import APIRouter

from src.app.adapters.api.v1.views.auth import router as auth_router
from src.app.adapters.api.v1.views.todo import router as todo_router

router = APIRouter(prefix="/v1/api")

router.include_router(auth_router)
router.include_router(todo_router)
