from fastapi import APIRouter, FastAPI

from app import recipe_handlers


app: FastAPI = FastAPI(title="Recipe API", openapi_url="/openapi.json")

router: APIRouter = APIRouter()


app.include_router(recipe_handlers.router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="debug", reload=True)
