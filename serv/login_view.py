from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes, render_html
from .utils import login_required


@web_routes.get("/login")
async def login(request):
    return render_html(request, 'login.html')