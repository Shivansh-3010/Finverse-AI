from logger.logger import setup_logger

from starlette.middleware.base import BaseHTTPMiddleware

logger = setup_logger()

class RequestLoggerMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request,
        call_next
    ):
        logger.info(
    f"Request: {request.method} {request.url.path}"
)

        response = await call_next(request)

        return response