from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import yaml
import os
from database import init_db
from routes import router


# Load OpenAPI spec from YAML file
def load_openapi_spec():
    """Load the OpenAPI specification from the YAML file."""
    openapi_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "openapi.yaml")
    with open(openapi_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# Initialize database on startup
init_db()

# Load custom OpenAPI spec
custom_openapi_spec = load_openapi_spec()

# Create FastAPI app with custom OpenAPI configuration
app = FastAPI(
    title=custom_openapi_spec["info"]["title"],
    description=custom_openapi_spec["info"]["description"],
    version=custom_openapi_spec["info"]["version"],
    docs_url="/",  # Swagger UI at root endpoint
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware - allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes with /api prefix
app.include_router(router, prefix="/api")


# Custom OpenAPI schema generation
def custom_openapi():
    """Return the custom OpenAPI schema loaded from openapi.yaml."""
    if app.openapi_schema:
        return app.openapi_schema
    
    # Use the exact spec from openapi.yaml without modifications
    app.openapi_schema = custom_openapi_spec
    return app.openapi_schema


# Override the default OpenAPI schema
app.openapi = custom_openapi


# Root endpoint for health check
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
