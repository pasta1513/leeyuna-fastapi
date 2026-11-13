from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from connection import Base, engine
from routes.user_route import user_router
from routes.file_route import file_router
import models.user_model
import models.file_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix='/users')
app.include_router(file_router, prefix='/files')

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)