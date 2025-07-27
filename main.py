from fastapi import   FastAPI;
from fastapi.middleware.cors import CORSMiddleware
from database import  engine
from models import models
from routers import auth,todos; 


# app = FastAPI()
app = FastAPI(
    title="Todo Application using FastAPI",
    description="api to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(todos.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
