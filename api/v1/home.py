# -*- coding: utf-8 -*-
from typing import Dict

from fastapi import APIRouter
from core.config import settings


router = APIRouter()


@router.get(path="/", summary="根站点", description="提供公共的导航路由", name="root")
def root() -> Dict:
    data = {
        "Get Started": "Hello FastAPI",
        "Public Sites": [
            "Interactive API docs: @{path}".format(path=settings.DOCS_URL),
            "Alternative API docs: @{path}".format(path=settings.REDOC_URL),
            "OpenAPI and JSON Schema: @{path}".format(path=settings.OPENAPI_URL)
        ],
        "README": "-"
    }
    return data
