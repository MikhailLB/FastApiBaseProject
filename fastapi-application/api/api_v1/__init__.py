from fastapi import APIRouter
from .users import router as users_router
from .notes import router as notes_router
router = APIRouter()
router.include_router(users_router)
router.include_router(notes_router)