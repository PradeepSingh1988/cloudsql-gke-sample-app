import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security.api_key import APIKey
from fastapi_versioning import version

from sample.api.schemas import User
from sample.common.auth import get_api_key
from sample.common.exceptions import SampleException, UserAlreadyExists, UserNotFound
from sample.db import api as db_api


LOG = logging.getLogger(__name__)
DEFAULT_PAGE_SIZE = 100

router = APIRouter(tags=["users"])



@router.get(
    "/users",
    response_model=List[User],
    summary="List Users",
)
@version(1)
def list_users(
    sort_key=Query(
        default="name",
        alias="sort_key",
        description="Sort Key",
    ),
    sort_dir=Query(
        default="asc",
        alias="sort_dir",
        description="Direction in which results should be sorted by sort_key, (asc, desc)",
    ),
    page_size=Query(
        default=DEFAULT_PAGE_SIZE,
        alias="limit",
        description="Limit number of items returned in response",
    ),
    name=Query(
        default=None,
        description="User Name for filtering",
        alias="name",
    ),
    phone=Query(
        default=None,
        description="User phone for filtering",
        alias="phone",
    ),
    email=Query(
        default=None,
        description="User email for filtering",
        alias="email",
    ),

    api_key: APIKey = Depends(get_api_key),
):

    LOG.debug("List all users")
    try:
        filter = {}
        if name:
            filter.update({"name": name})
        if phone:
            filter.update({"phone": phone})
        if email:
            filter.update({"email": email})
        
        return db_api.get_all_users(
            filters=filter,
            limit=page_size,
            sort_key=sort_key,
            sort_dir=sort_dir,
        )
    except (
        UserNotFound,
    ) as ex:
        LOG.warn(str(ex))
        return []

@router.post(
    "/users",
    response_model=User,
    summary="Create User",
)
@version(1)
def create_user(user: User, api_key: APIKey = Depends(get_api_key),):
    user_dict = user.dict()
    try:
        LOG.debug(user_dict)
        data = db_api.add_user(user_dict)
        return data
    except UserAlreadyExists:
        raise HTTPException(status_code=409, detail="User already exists")
    except SampleException as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    

