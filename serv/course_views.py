from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes, render_html
from .utils import login_required

#请求处理器handler
@web_routes.get("/course")
@login_required
async def view_course_list(request):
    return render_html(request, 'course_list.html')
