import logging
import sys

import uvicorn
from fastapi import FastAPI

from python_boilerplate.models.app_config import AppConfig
from server.routes import hello

app_config = AppConfig()

logging.basicConfig(
    level=app_config.app_log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.router.include_router(hello.router)

if __name__ == "__main__":
    logger.info(
        "Starting development server on %s:%s", app_config.app_host, app_config.app_port
    )
    uvicorn.run(app, host=app_config.app_host, port=app_config.app_port)
