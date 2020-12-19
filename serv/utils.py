"""
登录装饰器
"""
from aiohttp import web
def login_required(func):
    def wrapper(*args,**kwargs):

        # 请求对象
        request = args[0]
        cookie  = request.cookies
        username = cookie.get("username",None)
        password = cookie.get("password",None)
        if username=="1810650130" and password=="12345":
            #
            return func(*args,**kwargs)
        else:
            # 跳转到登录
            return web.HTTPFound(location="/login")

    return wrapper