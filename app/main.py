from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import models
from .database.database import engine
from .routers import campaigns

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(campaigns.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}