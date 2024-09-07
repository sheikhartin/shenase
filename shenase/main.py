import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from shenase.database import Base, engine
from shenase.routers import auth, users
from shenase.middlewares import CookieAuthMiddleware
from shenase.config import AVATAR_UPLOAD_FOLDER, AVATAR_STORAGE_PATH


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    os.makedirs(AVATAR_STORAGE_PATH, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title='Shenase',
    summary='System for managing user access and permissions.',
    version='v1',
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(CookieAuthMiddleware)

static_files_path = f'/{AVATAR_UPLOAD_FOLDER}'
static_files_directory = os.path.dirname(AVATAR_UPLOAD_FOLDER)
app.mount(
    static_files_path,
    StaticFiles(directory=AVATAR_STORAGE_PATH),
    name=static_files_directory,
)

app.include_router(auth.router, tags=['Authentication'])
app.include_router(users.router, tags=['Users'])
