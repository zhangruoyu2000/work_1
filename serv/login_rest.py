from .config import db_block, web_routes, render_html
from aiohttp import web


@web_routes.post("/api/login")
async def loginapi(request):
    username="1810650130"
    password="12345"
    data = await request.json()

    if data.get("username",None)==username and data.get("password",None)==password:
        res = web.json_response({"res": 1})
        res.set_cookie("username", username)
        res.set_cookie("password", password)
    else:
        res = web.json_response({"res": 0})

    # 获取json数据
    return res

# 清空cookie
@web_routes.post("/api/logout")
async def loginapi(request):

    data = await request.json()

    res = web.json_response({"res": 1})

    res.del_cookie("username")
    res.del_cookie("password")

    return res