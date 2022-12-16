import uvicorn as uvicorn
from fastapi import FastAPI

from routers import router


app = FastAPI()
app.include_router(router.r)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)