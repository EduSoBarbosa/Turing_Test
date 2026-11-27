from secrets import compare_digest
from typing import Annotated

from fastapi import Header, HTTPException, Request


def authenticate(request: Request, api_key: Annotated[str | None, Header(alias="X-Admin-API-Key")] = None):
    expected = request.app.state.experiments.settings.admin_api_key.get_secret_value()
    if not expected or not api_key or not compare_digest(expected.encode(), api_key.encode()):
        raise HTTPException(status_code=401, detail="Valid administrator credentials required.")
