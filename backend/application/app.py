from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.routes import routers

app = FastAPI(title="ZipInfo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)
