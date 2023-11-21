from fastapi import APIRouter
from config import settings
from app.models import *
from httpx_oauth.clients.github import GitHubOAuth2
from app.users import auth_backend, fastapi_users

router = APIRouter()

""" GitHub Login """
def get_oauth_router():
    # Inclusion of 2 routers for github login (under /auth)
    # GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET and DTT_FRONTEND_URL are loaded from the environment (.env)
    # as they will change depending on the environment (local, DEV, TEST, PROD)
    github_oauth_client = GitHubOAuth2(settings.OAUTH_GITHUB_CLIENT_ID, settings.OAUTH_GITHUB_CLIENT_SECRET)
    # Set scope to be only READ access
    github_oauth_client.base_scopes=["user:email"]
    return fastapi_users.get_oauth_router(
        github_oauth_client,
        auth_backend,
        settings.SECRET_KEY,
        associate_by_email=False,
        redirect_url=f"{settings.DTT_FRONTEND_URL}/auth/github-callback"
    )

router.include_router(get_oauth_router(), prefix="/github", tags=["Authentication"])

# --- Other piotential Routers for FASTAPI Users
# NOTE: 2023-09-19:MB: These routes commented out because unused for the moment.
# But left in code as they will become needed if we do more extensive authentication schemes

"""
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
"""