from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import processing

app = FastAPI(
    title="Webtoon Processing Service",
    description="Image processing service for webtoon panel translation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(processing.router)


@app.get("/")
async def root():
    return {
        "service": "Webtoon Processing Service",
        "version": "1.0.0",
        "status": "running"
    }
