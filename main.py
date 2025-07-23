from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from src.routes import items
from src.database import engine
from src import models
from src.utils.rate_limiter import limiter

app = FastAPI()

# DB Tables
models.Base.metadata.create_all(engine)

# Middleware
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
        headers=exc.headers
    )

# Routes
app.include_router(items.router)
