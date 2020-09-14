from typing import Optional
from starlette.exceptions import HTTPException


def abort(status_code: int, message: Optional[str] = None):
    raise HTTPException(status_code, detail=message)
