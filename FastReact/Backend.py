

import asyncio
import os
from fastapi.responses import Response
from fastapi import status as HTTP_STATUS, APIRouter
import rjsmin
import logging
import json

logger = logging.getLogger('uvicorn')

async def get_theme(resp: Response, theme: str):
    path = os.path.join(os.path.dirname(__file__), 'theme', theme+'.json')
    if not os.path.isfile(path):
        logger.error(f'Theme {theme} not available! returning default theme')
        path = os.path.join(os.path.dirname(__file__), 'theme', 'Light.json')
    theme_ =  await asyncio.gather(read_file(path))
    return json.loads(theme_[0])

async def get_available_theme(resp: Response):
    available_theme =  os.listdir(os.path.join(os.path.dirname(__file__), 'theme'))
    return [theme[:-5] for theme in available_theme]