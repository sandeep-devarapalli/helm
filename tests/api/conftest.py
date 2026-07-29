import asyncio
import os
from collections.abc import AsyncIterator, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from helm.database import Base, get_session
from helm.domain.models import OperatingContext, Workspace
from helm.main import app
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool


@dataclass(frozen=True)
class ApiTestContext:
    client: TestClient
    session_factory: async_sessionmaker[AsyncSession]
    workspace_a: UUID
    workspace_b: UUID


def create_test_engine(tmp_path: Path) -> tuple[AsyncEngine, bool]:
    database_url = os.getenv("HELM_TEST_DATABASE_URL")
    if database_url is None:
        database_url = f"sqlite+aiosqlite:///{tmp_path / 'helm-test.db'}"
    engine = create_async_engine(database_url, poolclass=NullPool)
    is_sqlite = database_url.startswith("sqlite")
    if is_sqlite:

        @event.listens_for(engine.sync_engine, "connect")
        def enable_sqlite_foreign_keys(
            dbapi_connection: Any,
            connection_record: Any,
        ) -> None:
            del connection_record
            dbapi_connection.execute("PRAGMA foreign_keys=ON")

    return engine, is_sqlite


@pytest.fixture
def api_context(tmp_path: Path) -> Iterator[ApiTestContext]:
    engine, is_sqlite = create_test_engine(tmp_path)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    workspace_a = uuid4()
    workspace_b = uuid4()

    async def prepare() -> None:
        async with engine.begin() as connection:
            if is_sqlite:
                await connection.run_sync(Base.metadata.drop_all)
                await connection.run_sync(Base.metadata.create_all)
            else:
                await connection.execute(
                    text(
                        "TRUNCATE run_events, agent_runs, messages, conversations, "
                        "workspaces RESTART IDENTITY CASCADE"
                    )
                )
        async with session_factory() as session:
            session.add_all(
                [
                    Workspace(
                        id=workspace_a,
                        name="Individual workspace",
                        operating_context=OperatingContext.INDIVIDUAL_SELF_DIRECTED.value,
                    ),
                    Workspace(
                        id=workspace_b,
                        name="Institutional workspace",
                        operating_context=OperatingContext.INSTITUTIONAL_PROPRIETARY.value,
                    ),
                ]
            )
            await session.commit()

    async def override_session() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    asyncio.run(prepare())
    app.dependency_overrides[get_session] = override_session
    with TestClient(app) as client:
        yield ApiTestContext(client, session_factory, workspace_a, workspace_b)
    app.dependency_overrides.clear()

    async def cleanup() -> None:
        if is_sqlite:
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.drop_all)
        await engine.dispose()

    asyncio.run(cleanup())
