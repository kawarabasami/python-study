# Python Project Instructions

## Context
This is a modern Python project developed by a team using a cutting-edge stack. The developer asking you questions has a strong background in TypeScript (Next.js, Apollo, Jest) but is re-learning Python after a 10-year gap. Explain concepts by drawing analogies to the TypeScript/Node.js ecosystem when helpful.

## Tech Stack
- **Package & Environment Manager**: `uv` (Use `uv add`, `uv run` instead of `pip` or `poetry`)
- **Linter & Formatter**: `ruff` (Do not suggest `flake8`, `black`, or `isort`)
- **Web API Framework**: `FastAPI`
- **CLI Framework**: `Typer`
- **Database / ORM**: `PostgreSQL` + `SQLAlchemy 2.0` (Async mode)
- **Validation**: `Pydantic v2`
- **Testing**: `pytest`

## Coding Rules & Guidelines
1. **Always use Type Hints**: Every function parameter and return value must have type annotations.
2. **Asynchronous by Default**: For database operations and FastAPI endpoints, use `async`/`await` and `sqlalchemy.ext.asyncio`.
3. **Pydantic v2 Syntax**: Use `model_dump()` instead of `dict()`, and `model_validate()` instead of `parse_obj()`.
4. **No Legacy Python**: Do not use `os.path` (use `pathlib`), avoid old string formatting (use f-strings).
5. **Clear Separation**: Maintain separation between Pydantic models (Schemas) and SQLAlchemy models (Entities).


