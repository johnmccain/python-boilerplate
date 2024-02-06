import logging

from fastapi.routing import APIRouter

from python_boilerplate.models.app_config import AppConfig
from server.resources import my_class

logging = logging.getLogger(__name__)

app_config = AppConfig()
router = APIRouter()


@router.get("/hello")
def hello():
    logging.info("Hello, world!")
    return {"hello": "world", "value": my_class.my_method()}
