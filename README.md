# Python Boilerplate

This project is a somewhat opinionated scaffolding & configuration for a Python application managed with poetry.

## Installation

This project requires python>=3.11, though it can be modified to use previous versions.

This project additionally requires that `poetry` is installed.

**Install project & dependencies**

```bash
poetry install
```

**Activate Virtual Environment**

```bash
source .venv/bin/activate # MacOS/Linux

.venv/Scripts/activate.bat # Windows
```

*Note: Poetry allows you to activate the virtual environment via `poetry shell`, but you can only enter the venv like this in one console at a time. Activating via virtual environment bypasses this restriction.*

**Install Pre-Commit Hook**

```bash
pre-commit install
```

## Dependencies

Dev/Test dependencies are discussed in the appropriate sections.
The only hard dependencies for this project are `poetry`, `dynaconf`, and `pydantic`. Pydantic is a library for building data models, and it can be swapped with dataclasses or another 3rd party library if desired. Dynaconf is used for configuration management and is discussed later.

## Files

- poetry.toml
    - Contains poetry settings. Some people prefer this to be not committed in repo, but I like having it here to standardize creation of virtualenvs within the project directory. It can be removed if desired.
- pyproject.toml
    - Contains package information including dependencies & some configuration.
    Dependencies are specified using less precise version restrictions.
- poetry.lock
    - Auto generated file specifying exact dependencies (like a pip freeze). Best practice is to keep this in source control so that deploying the app deploys the exact dependencies used during testing. This file should *not* be edited manually. It will automatically update when changing dependencies or when running `poetry lock`.
- .pre-commit-config.yaml
    - Configuration for pre-commit hooks
- Dockerfile
    - Dockerfile for deployment
- Dockerfile.test
    - Dockerfile for testing in CI/CD pipelines
- docker-compose.yaml

## Package Structure

This project installs your python application as a package, which allows absolute imports like `from python_boilerplate.models import ...`. This is a standard practice.

The directory structure of the package is up to you, but there are two submodules included at present. `config` contains .toml configuration files + the dynaconf configuration. `models` contains Pydantic data models.

### Configuration

Configuration in this project is implemented with [Dynaconf](https://www.dynaconf.com/), a modern configuration library for Python. This project uses .toml files as configuration to follow modern Python conventions and for the typed nature of the configuration (saving you from needing to manually parse or type cast).

Dynaconf allows for environment variable overrides of configuration. See the [Dynaconf docs](https://www.dynaconf.com/#on-env-vars) for more information.

The dynaconf configuration object is located in `python_boilerplate/config/config.py`

Dynaconf is set up to build the config from 3 files (co-located with the config.py), `default.toml`, `.secrets.toml` (not in source control), and an environment specific toml file (defaulting to `local.toml`). The environment is determined by the `ENV` environment variable and is intended to allow differing configs for different deployment environments (dev, stage, prod etc.).

Crucially, application code should *not* utilize the dynaconf object directly. The preferred pattern is to use the `python_boilerplate.models.app_config` Pydantic model to access configs. When you add a config, you should add an associated new property to that data model. Using the AppConfig pattern makes unit testing much easier as you can easily override configurations by passing in a non-default AppConfig object.


## Tests

This project is set up to use `pytest` for unit testing. Unit tests are located in the `tests` directory. That directory structure should mirror the package's structure, with test files named `test_<module name>.py`.

### Writing Testable Code

Unit tests can be made much easier or more difficult depending on design decisions of the code to be tested. One of the single best ways to improve testability is to use inversion of control. Python does not have any prominent dependency injection frameworks, but you can implement classes to do a "psuedo" DI pattern as so:

```python

class MyTestableClass:

    def __init__(
        self,
        app_config: AppConfig | None = None,
        some_client: SomeClient | None = None,
        ...
    ) -> None:
        self.app_config = app_config or AppConfig()
        self.some_client = some_client or SomeClient()
```

Making all complex dependencies optional means that you can still instantiate `MyTestableClass` by simply calling `MyTestableClass()`, but you can also override those dependencies with a mock or some specific value used for testing.

## Code Quality Tooling

There are a variety of tools that we can use to improve code quality and maintainability of a project like this such as linters, type checkers, auto formatting, etc.

This project proposes splitting those tools into two groups based on how strict & intrusive they are.

### Pre-Commit Hooks (Permissive Checks)

Pre-commit hooks run before every commit. If any checks fail, the commit is blocked. This is a great place for auto formatting (which reduces PR size by standardizing formatting) and more permissively configured linting. Pre-commit hooks should not be so onerous as to discourage frequent commits, so strict tests like type checking & unit test runs should not go in pre-commit hooks. Pre-commit hooks should run very fast (in ~10s or less) to avoid slowing down development.

This project is configured with pre-commit hooks such as poetry lock checks, import sorting, `black` autoformatting, and pylint. Pylint can be oversensitive, so if you find that a warning type is not helpful you can disable it globally in the `pyproject.toml` under `tool.pylint."messages control"`. Avoid adding too many disabled alerts here unless it is agreed upon by your team, or pylint can lose its ability to maintain code quality. You can bypass pylint warnings at the line level or file level with [inline comments](https://pylint.pycqa.org/en/latest/user_guide/messages/message_control.html).

Pre-commit hooks can be bypassed or disabled by developers if needed, though you should avoid this unless there is good reason.

Testing code is excluded from pylint checks.

### Pre-Merge Checks (Strict Checks)

Stricter checks can be configured to run as a pre-merge check in your version control remote platform (i.e. GitHub). This is a good place for more disruptive & slow running checks. Checks that belong here include unit tests, integration tests, stricter linting (if desired), and static type checking (`mypy`). The idea is that a commit can represent a working or in-progress state which may not have every case covered or full documentation, but a PR up for review should be production ready and of consistently high quality. PR gates can typically be bypassed by leadership, but this should happen only in exceptional circumstances. Even when hotfixing, if your fix breaks tests and you bypass that, you might just be making a situation worse.

You can also add conditions that check for the level of code coverage to avoid merging PRs that do not sufficiently test new added code. Writing tests as you develop is easier and leads to better tests, so you want to avoid needing to go back in and retrofit unit tests.

Stricter linting such as requiring docstrings can go here as well.

Static type checking with MyPy also belongs in the pre-merge checks. Python's dynamic typing makes it expressive, but can be the cause of many bugs. Writing thoroughly type annotated Python and using MyPy can have a massive impact on code quality and reliability.

MyPy's type inference is quite good, but if it needs some help you can add assert statements to your code. Crucially, an assert should never be used for control flow (and you should never expect it could fail)--when running the Python interpreter with certain optimization settings enabled, asserts are entirely bypassed so relying on them for control flow can result in unexpected behavior. Here is an example of using an assert to make MyPy happy:

```python
def my_func(value: int | None):
    if value:
        value += 1 # MyPy will recognize that value must be not None because of the if check
    # But if MyPy didn't for some reason (can happen with some complicated design patterns or with specific business logic), you can assert like so. Adding the reason in a comment is good practice.
    assert isinstance(value, int)  # For MyPy
```
