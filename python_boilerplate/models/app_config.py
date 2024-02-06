from pydantic import BaseModel

from python_boilerplate.config.config import config


class AppConfig(BaseModel):
    """
    Model containing default values for all application configuration.
    The intention of this model is to avoid accessing the dynaconf configuration directly anywhere outside of this file,
    preferring to retrieve values from this model instead. This allows easy overriding of configuration values for unit
    testing & maintains inversion of control.
    """

    app_log_level: str = config["app.log_level"]
    app_host: str = config["app.host"]
    app_port: int = config["app.port"]

    my_class_value: int = config["my_class.value"]
