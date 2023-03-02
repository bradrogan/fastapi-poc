from fastapi import FastAPI
from app.api.api_v1.api import api_router as api_router_v1
from app.core.config import settings


app: FastAPI = FastAPI(title="Recipe API", openapi_url="/openapi.json")


app.include_router(api_router_v1, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(  # type: ignore
        "main:app",
        host="0.0.0.0",
        port=8001,
        log_level="debug",
        reload=True,
    )
