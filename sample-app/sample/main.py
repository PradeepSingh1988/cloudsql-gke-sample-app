from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
import uvicorn

from sample.api import users
from sample import log_config

app = FastAPI(
    title="Sample Application",
    description="Sample application to manage Users",
    version="1.0.0",
)

app.include_router(users.router, prefix="/sample")
app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}")


@app.get("/", include_in_schema=False)
def index():
    """
    Check health
    """
    return {"health": "OK"}


if __name__ == "__main__":
    uvicorn.run("sample.main:app", port=9595, reload=True, log_config=log_config)
