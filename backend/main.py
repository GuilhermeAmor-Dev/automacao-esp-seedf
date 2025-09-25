# backend/main.py
# Ponto de entrada da API: instancia FastAPI, aplica middlewares e registra routers.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .Controllers import auth_router, users_router
from .database import Base, engine

app = FastAPI(title="API - AutomaÃ§Ã£o ESP SEEDF")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/health", tags=["health"])
def healthcheck():
    return {"ok": True}

