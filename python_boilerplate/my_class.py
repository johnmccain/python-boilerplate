import logging

from python_boilerplate.models.app_config import AppConfig

logger = logging.getLogger(__name__)


class MyClass:
    def __init__(self, app_config: AppConfig | None = None):
        self.app_config = app_config or AppConfig()

    def my_method(self):
        return self.app_config.my_class_value
