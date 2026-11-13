# List recipes.
default:
    @just --list

# Run the test suite.
test *args:
    uv run -m pytest {{ args }}

# Run tests against every supported Python/Django pair, like CI.
tox:
    uvx --with tox-uv tox

# Check types.
typecheck:
    uv run mypy src

# Check code style without changing files.
lint:
    uv run ruff check src tests example
    uv run ruff format --check src tests example
    uv run djlint --check src tests example

# Format code.
fmt:
    uv run ruff check --fix src tests example
    uv run ruff format src tests example
    uv run djlint --reformat src tests example

# Run every check, as before a commit.
check: lint typecheck test

# Build the wheel and sdist into dist/.
build:
    uv build

# Remove build artifacts and caches.
clean:
    rm -rf dist .pytest_cache .mypy_cache .ruff_cache .tox
    find . -name __pycache__ -type d -prune -exec rm -rf {} +
