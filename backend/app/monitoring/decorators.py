import time
from functools import wraps
import inspect

from monitoring.custom_metrics import DEPENDENCY_LATENCY, DEPENDENCY_ERRORS

def track_dependency(service_name: str):
    def decorator(func):
        def _record(status, start_time, e):
            if e is not None:
                DEPENDENCY_ERRORS.labels(service=service_name, operation=func.__name__, error=type(e).__name__).inc()

            DEPENDENCY_LATENCY.labels(service=service_name, operation=func.__name__, status=status).observe(time.perf_counter() - start_time)

        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.perf_counter()

                try:
                    result = await func(*args, **kwargs)
                    status = "successful"
                    error = None
                except Exception as e:
                    status="failed"
                    error = e
                    raise
                finally:
                    _record(status, start_time, error)

                return result
            return async_wrapper

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()

            try:
                result = func(*args, **kwargs)
                status = "successful"
                error = None
            except Exception as e:
                status="failed"
                error = e
                raise
            finally:
                _record(status, start_time, error)

            return result

        return wrapper
    return decorator