from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/sc/add')
async def action_sc_add(request):
    params = await request.post()
    stu_sn = params.get("stu_sn")
    cou_sn = params.get("cou_sn")
    cou_name = params.get(" cou_name")
    cou_term = params.get("cou_term")
    cou_week = params.get("cou_week")
    cou_jie = params.get("cou_jie")

    if stu_sn is None or cou_sn is None or cou_name is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, sc must be required")

    try:
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
        # cou_name = (cou_name)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    try:
        with db_block() as db:
            db.execute("""
            INSERT INTO course_sc (stu_sn, cou_sn, cou_name) 
            VALUES ( %(stu_sn)s, %(cou_sn)s, %(cou_name)s)
            """, dict(stu_sn=stu_sn, cou_sn=cou_sn, cou_name=cou_name))
    except psycopg2.errors.UniqueViolation:
        query = urlencode({
            "message": "已经添加该学生的课程",
            "return": "/cou_name"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except psycopg2.errors.ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此学生或课程: {ex}")

    return web.HTTPFound(location="/cou_name")


@web_routes.post('/action/sc/edit/{stu_sn}/{cou_sn}')
async def edit_sc_action(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    params = await request.post()
    cou_name = params.get("cou_name")

    try:
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
        cou_name = float(cou_name)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    with db_block() as db:
        db.execute("""
        UPDATE sc SET cou_name=%(cou_name)s
        WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn, cou_name=cou_name))

    return web.HTTPFound(location="/cou_name")


@web_routes.post('/action/sc/delete/{stu_sn}/{cou_sn}')
def delete_sc_action(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with db_block() as db:
        db.execute("""
        DELETE FROM sc
            WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))

    return web.HTTPFound(location="/cou_name")
