from aiohttp import web
from .config import db_block, web_routes, render_html
from .utils import login_required

@web_routes.get("/")
@login_required

async def home_page(request):
    return web.HTTPFound(location="/student")

