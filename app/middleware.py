from __future__ import annotations

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Reset context at request start to prevent cross-request leakage.
        clear_contextvars()

        # Reuse inbound request ID if present; otherwise generate one.
        inbound_request_id = request.headers.get("x-request-id", "").strip()
        correlation_id = inbound_request_id or f"req-{uuid.uuid4().hex[:8]}"
        
        # Bind correlation ID so every log line in this request carries it.
        bind_contextvars(correlation_id=correlation_id)
        
        request.state.correlation_id = correlation_id
        
        start = time.perf_counter()
        try:
            response = await call_next(request)
        finally:
            # Always clear request-scoped context even if handler errors.
            clear_contextvars()
        
        response.headers["x-request-id"] = correlation_id
        response.headers["x-response-time-ms"] = str(int((time.perf_counter() - start) * 1000))
        
        return response
