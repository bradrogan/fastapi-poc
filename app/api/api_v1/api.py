from fastapi import APIRouter


from .handler import recipe_router, user_router

api_router = APIRouter()
api_router.include_router(recipe_router, prefix="/recipes", tags=["recipes"])
api_router.include_router(user_router, prefix="/users", tags=["recipes"])
