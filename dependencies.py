import jwt.exceptions
import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.oauth2 import id_token
from google.auth.transport import requests

from clients.repositories.github_integration.github_repo import GitHubRepo
from config.config import settings
from config.queue import get_arq_pool
from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from config.database import async_session
from factories.storage_strategy_factory import StorageStrategyFactory
from clients.repositories import *
from services.data_store.strategy.data_store_strategy import DataStoreStrategy
from services.email_service import EmailService, email_service

logger = structlog.get_logger()

def get_email_dependancy() -> EmailService:
    return email_service


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide an asynchronous database session.

    Yields:
        AsyncSession: An async SQLAlchemy session for use in request handling.
    """
    async with async_session() as session:
        yield session


def get_organization_repo() -> OrganizationRepo:
    return OrganizationRepo()


def get_team_repo(
    email_service: EmailService = Depends(get_email_dependancy)
) -> TeamRepo:
    return TeamRepo(email_service)


def get_user_repo() -> UserRepo:
    return UserRepo()


def get_project_repo() -> ProjectRepo:
    return ProjectRepo()


def get_temp_story_repo() -> TempStoryRepo:
    return TempStoryRepo()

def get_storage_strategy() -> DataStoreStrategy:
    return StorageStrategyFactory.create()

def get_github_repo() -> GitHubRepo:
    return GitHubRepo()


security = HTTPBearer()


def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials
    try:
        if settings.test.e2e_enabled:
            return id_token.verify_token(
                token,
                requests.Request(),
                audience=settings.api.google_client_id,
                certs_url=settings.test.certs_url,
            )

        return id_token.verify_oauth2_token(
            token, requests.Request(), settings.api.google_client_id
        )
    except ValueError as e:
        logger.error(f"Invalid token {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid or expired token {e}"
        )
    except jwt.exceptions.PyJWKClientError as e:
        logger.error(f"Invalid token {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid or expired token {e}"
        )
