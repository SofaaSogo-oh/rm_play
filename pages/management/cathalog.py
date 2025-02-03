from .package import *
from data.movie import Movie
from .forms import ViewCathalog

@management_blueprint.route("/cathalog", methods=["GET", "POST"], defaults={"page":1})
@management_blueprint.route("/cathalog/page/<int:page>", methods=["GET", "POST"])
def cathalog(page):
    movies = None
    form = ViewCathalog()
    per_page = form.per_page.data if form.validate() else request.args.get("per_page", type=int, default=10)

    offset = (page - 1) * per_page

    with db_session.create_session() as session:
        movies = session.query(Movie).limit(per_page).offset(offset)
        total_cnt = session.query(Movie).count()
    total_pages = (total_cnt + per_page - 1) // per_page
    return render_template("cathalog.html", 
                               movies=movies, 
                               form=form, 
                               current_page=page, 
                               total_pages=total_pages,
                               per_page=per_page)

@management_blueprint.route("/cathalog_edit", methods=["GET", "POST"])
def cathalog_edit():
    pass