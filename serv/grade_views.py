from aiohttp import web
from .config import db_block, web_routes, render_html
from .utils import login_required

@web_routes.get("/grade")
@login_required
async def view_list_grades(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS stu_sn, no as stu_no, name as stu_name FROM student ORDER BY name
        """)
        students = list(db)

        db.execute("""
        SELECT sn AS cou_sn, term as cou_term, name as cou_name, teacher as cou_teacher FROM course ORDER BY name
        """)
        courses = list(db)

        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.no as stu_no,
            s.name as stu_name, 
            c.term as cou_term, 
            c.name as cou_name,
            c.teacher as cou_teacher,
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        ORDER BY stu_sn, cou_sn;
        """)

        items = list(db)

        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        ORDER BY stu_sn, cou_sn;
        """)
        grades = db.fetch_first()

    return render_html(request, 'grade_list.html',
                       students=students,
                       courses=courses,
                       grades=grades,
                       items=items)


@web_routes.get('/grade/edit/{stu_sn}/{cou_sn}')
def view_grade_editor(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    if stu_sn is None or cou_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT grade FROM course_grade
            WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s;
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn))

        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sn}, cou_sn={cou_sn}")

    return render_html(request, "grade_edit.html",
                       stu_sn=stu_sn,
                       cou_sn=cou_sn,
                       grade=record.grade)


@web_routes.get("/grade/delete/{stu_sn}/{cou_sn}")
def grade_deletion_dialog(request):
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
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sn}, cou_sn={cou_sn}")

    return render_html(request, 'grade_dialog_deletion.html', record=record)


@web_routes.get("/grade/select/{stu_sn}/{cou_sn}")
def grade_select_dialog(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")

    if stu_sn is None :
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
        WHERE stu_sn = %(stu_sn)s ;
        """, dict(stu_sn=stu_sn))

        records = list(db)

        db.execute("""
        SELECT sn AS stu_sn, name as stu_name FROM student 
        WHERE sn = %(stu_sn)s;
        """, dict(stu_sn=stu_sn))

        students = db.fetch_first()


    if records is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sn}")

    return render_html(request, 'grade_dialog_select.html', records=records, students=students)

@web_routes.get("/grade/tc/{stu_sn}/{cou_sn}")
def grade_tc_dialog(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")

    if cou_sn is None :
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")

    with db_block() as db:
        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name,
            c.term as cou_term, 
            g.grade 
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
        WHERE cou_sn = %(cou_sn)s ;
        """, dict(cou_sn=cou_sn))

        records = list(db)

        db.execute("""
        SELECT sn AS cou_sn, name as cou_name, term as cou_term FROM course 
        WHERE sn = %(cou_sn)s;
        """, dict(cou_sn=cou_sn))

        courses = db.fetch_first()


    if records is None:
        return web.HTTPNotFound(text=f"no such grade: cou_sn={cou_sn}")

    return render_html(request, 'grade_dialog_tc.html', records=records, courses=courses)
