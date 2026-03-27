from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes.texts import router as texts_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Библиотека текстов")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(texts_router)


@app.get("/")
def root():
    return {"message": "API библиотеки текстов работает"}
