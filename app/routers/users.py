import httpx
from fastapi import APIRouter, Depends
from app.schemas import UserRead, UserUpdate
from app.users import current_active_user, fastapi_users
from app.db import User

router = APIRouter()


# This function extracts and returns more info from github about the current user
# Assumes the current user is authenticated into the DTT service
# returns a JSON with lots of user info - And augmented with a "emails" sub-dictionary which contains the user's 
# registered emails in github. 
# See: https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-the-authenticated-user 
# and https://docs.github.com/en/rest/users/emails?apiVersion=2022-11-28#list-email-addresses-for-the-authenticated-user
# for more details about the returned JSON structure

@router.get("/github-user",   tags=["Users"], summary="Users:User info from github")
async def get_github_user_info(user: User = Depends(current_active_user)):

    # Get the user's github access token from our database
    oauth_accounts = user.oauth_accounts
    github_token=oauth_accounts[0].access_token

    # Call github directly to get more user information
    async with httpx.AsyncClient() as client:

        headers = {'Accept':'application/json'}
        headers.update ({'Authorization': f'Bearer {github_token}'})

        try:
            response = await client.get('https://api.github.com/user', headers=headers)
            github_basic_userinfo = response.json()
        except:
            return {"error":"Unable to call github/user"}   ## TBD: Return proper error code

        # Now get the primary email address
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get('https://api.github.com/user/emails', headers=headers)
                github_basic_userinfo['emails'] = response.json()
        except:
            return {"error":"Unable to call github/email"}   ## TBD: Return proper error code

    return github_basic_userinfo

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["Users"]
)
