import logging

from fastapi import HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException

from sample.common.config import get_settings

LOG = logging.getLogger(__name__)

api_keys = ["f83c831675f74cdfa63714c52ebf4dba", "ww5756mhmhjky8asdaw4v5675s9923Sh"]

if not get_settings().enable_api_key_validation:
    LOG.info("API KEY Validation check is turned off")

api_key_header = APIKeyHeader(name="X-AUTH-API-KEY", auto_error=False)


def get_api_key(api_key_header: str = Security(api_key_header)):
    if not get_settings().enable_api_key_validation:
        return
    if api_key_header in api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="API Key not valid"
        )
