from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.settings import config

app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_VERSION,
    version=config.APP_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.__main__:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=config.SERVER_RELOAD,
        workers=config.SERVER_WORKERS,
    )
