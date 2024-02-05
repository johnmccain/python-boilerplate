from pydantic import BaseModel

from python_boilerplate.config.config import config


class AppConfig(BaseModel):
    """
    Model containing default values for all application configuration.
    The intention of this model is to avoid accessing the dynaconf configuration directly anywhere outside of this file,
    preferring to retrieve values from this model instead. This allows easy overriding of configuration values for unit
    testing & maintains inversion of control.
    """

    my_class_value: int = config["my_class.value"]
