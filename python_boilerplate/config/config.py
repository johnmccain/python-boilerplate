import os
import pathlib

from dynaconf import Dynaconf

current_dir = pathlib.Path(__file__).parent

# Load the environment from the `ENV` environment variable, defaulting to `local`.
env = os.environ.get("ENV", "local")

config = Dynaconf(
    envvar_prefix="DYNACONF",  # `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
    settings_files=[
        current_dir / f"{env}.toml",
        current_dir / "default.toml",
        current_dir / ".secrets.toml",
    ],
)
