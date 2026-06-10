from fastapi import FastAPI

from api.v1.health.router import router as health_router
from api.v1.stocks.router import router as stocks_router
from api.v1.news.router import router as news_router
from api.v1.risk.router import router as risk_router
from api.v1.recommendations.router import router as recommendations_router
from api.v1.copilot.router import router as copilot_router
from logger.logger import setup_logger
from exceptions.handlers import generic_exception_handler
from middleware.request_logger import RequestLoggerMiddleware
from middleware.security_headers import SecurityHeadersMiddleware
from api.v1.stocks.market_data_router import router as market_data_router
from scheduler.market_data_scheduler import (
    start_scheduler,
    stop_scheduler,
)


app = FastAPI(
    title="FinVerse AI",
    version="1.0.0"
)

app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

app.add_exception_handler(Exception, generic_exception_handler) 

logger = setup_logger()
logger.info("FinVerse AI started successfully")

app.include_router(
    health_router,
    prefix="/api/v1/health",
    tags=["Health"]
)

app.include_router(
    stocks_router,
    prefix="/api/v1/stocks",
    tags=["Stocks"]
)

app.include_router(
    news_router,
    prefix="/api/v1/news",
    tags=["News"]
)

app.include_router(
    risk_router,
    prefix="/api/v1/risk",
    tags=["Risk"]
)

app.include_router(
    recommendations_router,
    prefix="/api/v1/recommendations",
    tags=["Recommendations"]
)

app.include_router(
    copilot_router,
    prefix="/api/v1/copilot",
    tags=["Copilot"]
)

app.include_router(
    market_data_router,
    prefix="/api/v1",
    tags=["Market Data"]
)

@app.on_event("startup")
async def startup_event():

    start_scheduler()


@app.on_event("shutdown")
async def shutdown_event():

    stop_scheduler()