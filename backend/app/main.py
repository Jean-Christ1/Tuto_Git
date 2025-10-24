"""
Natural Language to SQL - Main Application.

This is the main FastAPI application entry point for the Natural Language
to SQL accelerator platform.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import time
from loguru import logger

from app.config import get_settings
from app.database import test_connection, close_db_connection
from app.routers import query_router, schema_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events for the application.

    Parameters
    ----------
    app : FastAPI
        FastAPI application instance.

    Yields
    ------
    None

    Examples
    --------
    This function is automatically called by FastAPI during application lifecycle.
    """
    # Startup
    logger.info("Starting Natural Language to SQL API")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"LLM Provider: {settings.llm_provider}")

    # Test database connection
    if test_connection():
        logger.info("Database connection successful")
    else:
        logger.error("Database connection failed")

    yield

    # Shutdown
    logger.info("Shutting down Natural Language to SQL API")
    close_db_connection()


# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="""
    Natural Language to SQL Accelerator API

    This API enables users to query databases using natural language and receive
    results with intelligent visualizations.

    ## Features

    * **Natural Language Queries**: Convert plain English to SQL
    * **Query Execution**: Safe SQL execution with validation
    * **Schema Analysis**: Explore database structure and relationships
    * **Export Options**: Download results as CSV or JSON
    * **Query Suggestions**: Get intelligent query recommendations

    ## Authentication

    Currently, this API does not require authentication. In production,
    implement proper authentication and authorization.

    ## Rate Limiting

    Rate limits:
    - 60 requests per minute
    - 1000 requests per hour
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods.split(",")
    if isinstance(settings.cors_allow_methods, str)
    else settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers.split(",")
    if isinstance(settings.cors_allow_headers, str)
    else settings.cors_allow_headers,
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Add processing time to response headers.

    Parameters
    ----------
    request : Request
        FastAPI request object.
    call_next : Callable
        Next middleware or route handler.

    Returns
    -------
    Response
        Response with X-Process-Time header.

    Examples
    --------
    This middleware is automatically applied to all requests.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
    return response


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """
    Handle ValueError exceptions.

    Parameters
    ----------
    request : Request
        FastAPI request object.
    exc : ValueError
        ValueError exception.

    Returns
    -------
    JSONResponse
        Error response with 400 status code.

    Examples
    --------
    Automatically handles ValueError exceptions from route handlers.
    """
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": str(exc), "type": "ValueError"},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions.

    Parameters
    ----------
    request : Request
        FastAPI request object.
    exc : Exception
        Exception instance.

    Returns
    -------
    JSONResponse
        Error response with 500 status code.

    Examples
    --------
    Automatically handles unhandled exceptions from route handlers.
    """
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "type": type(exc).__name__,
        },
    )


# Include routers
app.include_router(query_router)
app.include_router(schema_router)


@app.get("/")
async def root():
    """
    Root endpoint.

    Returns basic API information and available endpoints.

    Returns
    -------
    dict
        API information and links.

    Examples
    --------
    GET /

    Response:
    {
        "message": "Natural Language to SQL API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
    """
    return {
        "message": "Natural Language to SQL API",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "endpoints": {
            "query": "/api/query/nl",
            "schema": "/api/schema",
            "suggestions": "/api/schema/suggestions",
        },
    }


@app.get("/health")
async def health():
    """
    Health check endpoint.

    Returns application health status and version information.

    Returns
    -------
    dict
        Health status information.

    Examples
    --------
    GET /health

    Response:
    {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected",
        "llm_provider": "openai"
    }
    """
    db_status = "connected" if test_connection() else "disconnected"

    return {
        "status": "healthy",
        "version": settings.api_version,
        "database": db_status,
        "llm_provider": settings.llm_provider,
        "debug": settings.debug,
    }


@app.get("/info")
async def info():
    """
    Get API configuration information.

    Returns non-sensitive configuration details.

    Returns
    -------
    dict
        API configuration information.

    Examples
    --------
    GET /info

    Response:
    {
        "api_version": "1.0.0",
        "llm_provider": "openai",
        "max_query_results": 1000,
        "query_timeout": 30
    }
    """
    return {
        "api_version": settings.api_version,
        "llm_provider": settings.llm_provider,
        "max_query_results": settings.max_query_results,
        "query_timeout": settings.query_timeout,
        "enable_query_caching": settings.enable_query_caching,
        "rate_limit_per_minute": settings.rate_limit_per_minute,
    }


def custom_openapi():
    """
    Customize OpenAPI schema.

    Returns
    -------
    dict
        Custom OpenAPI schema.

    Examples
    --------
    This function is called automatically by FastAPI to generate API documentation.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.api_title,
        version=settings.api_version,
        description="Natural Language to SQL Accelerator API",
        routes=app.routes,
    )

    # Add custom schema elements
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
