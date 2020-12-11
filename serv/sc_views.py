from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.get("/sc")
async def view_list_grades(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS stu_sn, name as stu_name FROM student ORDER BY name
        """)
        students = list(db)

        db.execute("""
        SELECT sn AS cou_sn, name as cou_name, term as cou_term, week as cou_week,
        day as cou_day, jie as cou_jie FROM course ORDER BY name
        """)
        courses = list(db)

        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name,
            c.term as cou_term, 
            c.week as cou_week,
            c.day as cou_day,
            c.jie as cou_jie,
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        ORDER BY stu_sn, cou_sn;
        """)

        items = list(db)

    return render_html(request, 'sc_list.html',
                       students=students,
                       courses=courses,
                       items=items)


@web_routes.get('/sc/edit/{stu_sn}/{cou_sn}')
def view_sc_editor(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    cou_name = request.match_info.get("cou_name")
    cou_term = request.match_info.get("cou_term")

    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    # if cou_name is None or cou_term is None:
    #     return web.HTTPBadRequest(text="cou_name, cou_term, must be required")


    with db_block() as db:
        db.execute("""
        SELECT cou_name FROM sc
            WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s;
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such sc: stu_sn={stu_sn}, cou_sn={cou_sn}, cou_name={cou_name},cou_term={cou_term}")

    return render_html(request, "sc_edit.html",
                       stu_sn=stu_sn,
                       cou_sn=cou_sn,
                       cou_name=record.cou_name)


@web_routes.get("/sc/delete/{stu_sn}/{cou_sn}")
def sc_deletion_dialog(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT g.stu_sn, g.cou_sn,
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s;
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such sc: stu_sn={stu_sn}, cou_sn={cou_sn}")

    return render_html(request, 'sc_dialog_deletion.html', record=record)
