from fastapi import FastAPI

from api.v1.health.router import router as health_router
from logger.logger import setup_logger
from exceptions.handlers import generic_exception_handler


app = FastAPI(
    title="FinVerse AI",
    version="1.0.0"
)

app.add_exception_handler(Exception, generic_exception_handler) 

logger = setup_logger()
logger.info("FinVerse AI started successfully")

app.include_router(
    health_router,
    prefix="/api/v1/health",
    tags=["Health"]
)