import logging

from fastapi import FastAPI

from app.api import health
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title="CodeLens", version="0.1.0")
app.include_router(health.router)

logger.info("CodeLens backend started (env=%s)", settings.app_env)
