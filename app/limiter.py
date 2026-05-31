# app/limiter.py
import os
from slowapi import Limiter
from slowapi.util import get_remote_address

# Check if the code is currently running inside a pytest session
is_testing = os.getenv("PYTEST_CURRENT_TEST") is not None

limiter = Limiter(
    key_func=get_remote_address,
    enabled=not is_testing  # Disables rate limiting automatically during testing!
)