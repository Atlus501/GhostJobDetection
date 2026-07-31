from fastapi import FastAPI

from middlewares.cors import setup_corsmiddleware
from middlewares.secure_headers import SecureResponseMiddleware

def setup_middlewares(app : FastAPI):
    setup_corsmiddleware(app)
    app.add_middleware(SecureResponseMiddleware)