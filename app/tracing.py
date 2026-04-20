from __future__ import annotations

from contextvars import ContextVar
from dataclasses import asdict, is_dataclass
import os
from functools import wraps
from typing import Any

try:
    from langfuse import Langfuse
except Exception:  # pragma: no cover
    Langfuse = None  # type: ignore[assignment]

    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

    langfuse_context = _DummyContext()
    _current_span: ContextVar[Any | None] = ContextVar("langfuse_current_span", default=None)
else:
    _current_span: ContextVar[Any | None] = ContextVar("langfuse_current_span", default=None)


def _make_client() -> Any | None:
    if not (os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")):
        return None

    host = os.getenv("LANGFUSE_HOST") or os.getenv("LANGFUSE_BASE_URL")
    return Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=host,
        tracing_enabled=True,
        environment=os.getenv("APP_ENV", "dev"),
        release=os.getenv("APP_NAME", "day13-observability-lab"),
    )


LANGFUSE_CLIENT = _make_client()


def _serialize(value: Any) -> Any:
    if value is None:
        return None
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_serialize(item) for item in value]
    return repr(value)


def observe(*args: Any, **kwargs: Any):
    def decorator(func):
        @wraps(func)
        def wrapper(*func_args: Any, **func_kwargs: Any):
            if LANGFUSE_CLIENT is None:
                return func(*func_args, **func_kwargs)

            token = _current_span.set(None)
            try:
                if hasattr(LANGFUSE_CLIENT, "start_as_current_span"):
                    with LANGFUSE_CLIENT.start_as_current_span(name=func.__name__) as span:
                        token = _current_span.set(span)
                        try:
                            result = func(*func_args, **func_kwargs)
                            span.update(output=_serialize(result))
                            return result
                        except Exception as exc:
                            span.update(metadata={"error_type": type(exc).__name__}, status_message=str(exc))
                            raise
                        finally:
                            _current_span.reset(token)
                elif hasattr(LANGFUSE_CLIENT, "start_span"):
                    span = LANGFUSE_CLIENT.start_span(name=func.__name__)
                    token = _current_span.set(span)
                    try:
                        result = func(*func_args, **func_kwargs)
                        span.update(output=_serialize(result))
                        return result
                    except Exception as exc:
                        span.update(metadata={"error_type": type(exc).__name__}, status_message=str(exc))
                        raise
                    finally:
                        _current_span.reset(token)
                        if hasattr(span, "end"):
                            span.end()
                else:
                    return func(*func_args, **func_kwargs)
            finally:
                if hasattr(LANGFUSE_CLIENT, "flush"):
                    LANGFUSE_CLIENT.flush()

        return wrapper

    if args and callable(args[0]) and not kwargs:
        return decorator(args[0])

    return decorator


class _LangfuseContext:
    def update_current_trace(self, **kwargs: Any) -> None:
        if LANGFUSE_CLIENT is None:
            return None
        if hasattr(LANGFUSE_CLIENT, "update_current_trace"):
            LANGFUSE_CLIENT.update_current_trace(**kwargs)
            return None

        span = _current_span.get()
        if span is not None and hasattr(span, "update_trace"):
            span.update_trace(**kwargs)

    def update_current_observation(self, **kwargs: Any) -> None:
        span = _current_span.get()
        if span is None:
            return None

        safe_kwargs = dict(kwargs)
        if "usage_details" in safe_kwargs:
            usage = safe_kwargs.pop("usage_details")
            metadata = safe_kwargs.get("metadata")
            if not isinstance(metadata, dict):
                metadata = {}
            metadata["usage_details"] = usage
            safe_kwargs["metadata"] = metadata

        try:
            span.update(**safe_kwargs)
        except TypeError:
            # Older SDKs support a narrower update signature.
            if "metadata" in safe_kwargs:
                span.update(metadata=safe_kwargs["metadata"])

    def flush(self) -> None:
        if LANGFUSE_CLIENT is None:
            return None
        LANGFUSE_CLIENT.flush()


langfuse_context = _LangfuseContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
