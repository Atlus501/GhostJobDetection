# app/api/middleware/security.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from monitoring.custom_metrics import LATENCY, REQUESTS_NUMBER, FAILED_REQUESTS
import time

"""
Middlware class for adding secure response headers
"""
class SecureResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow the request to travel down to the router endpoint
        response = await call_next(request)
        
        # Inject your strict security headers onto the outgoing response
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'none'"

        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        url = request.url.path
        ignored_endpoints = {"/metrics", "/", "/health"}

        if url in ignored_endpoints:
            return await call_next(request)

        try:
            start_time = time.perf_counter()
            response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            status_code = 500
            FAILED_REQUESTS.labels(endpoint=url, status_code=status_code, error = type(e).__name__).inc()
            raise
        finally:
            LATENCY.labels(endpoint=url, status_code=status_code).observe(time.perf_counter()-start_time)
            REQUESTS_NUMBER.labels(endpoint=url, status_code=status_code).inc()

        return response