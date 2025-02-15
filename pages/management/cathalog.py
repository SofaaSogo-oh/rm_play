from .package import *
from data.movie import Movie
from .forms import ViewCathalog, MovieEd
from data.employee_view import UserPriveleges
from werkzeug.datastructures import MultiDict


@management_blueprint.route("/cathalog", methods=["GET", "POST"], defaults={"page": 1})
@management_blueprint.route("/cathalog/page/<int:page>", methods=["GET", "POST"])
def cathalog(page):
    curr_id = (
        flask_login.current_user.id
        if flask_login.current_user.is_authenticated
        else None
    )
    check_privelege = None

    movies = None
    form = ViewCathalog()
    per_page = (
        form.per_page.data
        if form.validate()
        else request.args.get("per_page", type=int, default=10)
    )

    offset = (page - 1) * per_page

    with db_session.create_session() as session:
        movies = session.query(Movie).limit(per_page).offset(offset)
        total_cnt = session.query(Movie).count()
        check_privelege = (
            session.query(UserPriveleges)
            .filter(
                (UserPriveleges.id == curr_id) & (UserPriveleges.name == "cathalog")
            )
            .first()
            if curr_id
            else None
        )

    total_pages = (total_cnt + per_page - 1) // per_page
    return render_template(
        "cathalog.html",
        movies=movies,
        form=form,
        current_page=page,
        total_pages=total_pages,
        per_page=per_page,
        check_privelege=check_privelege,
    )


@management_blueprint.route("/cathalog_edit", methods=["GET", "POST"])
def cathalog_edit():
    curr_id = (
        flask_login.current_user.id
        if flask_login.current_user.is_authenticated
        else None
    )

    check_privelege = None
    with db_session.create_session() as session:
        check_privelege = (
            session.query(UserPriveleges)
            .filter(
                (UserPriveleges.id == curr_id) & (UserPriveleges.name == "cathalog")
            )
            .first()
            if curr_id
            else None
        )
    if check_privelege is None:
        return redirect("/cathalog")

    form = MovieEd()
    edit_id = request.args.get("id", type=int, default=None)
    new_data = False
    render_page = lambda msg=None, form=form: render_template(
        "cathalog_edit.html", message=msg, form=form
    )
    with db_session.create_session() as session:
        try:
            if edit_id:
                edit_item = session.query(Movie).get(edit_id)
            else:
                edit_item = Movie()
                new_data = True
            if form.validate_on_submit():
                edit_item.name = form.name.data
                edit_item.description = form.description.data
                edit_item.price = form.price.data
                if new_data:
                    session.add(edit_item)
                session.commit()
                return render_page("Все окей", form)
        except IntegrityError as e:
            return render_page(f"Что-то пошло не так: {e}", form)
    return render_page()
