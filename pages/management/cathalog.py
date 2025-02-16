from .package import *
from data.movie import Movie
from .forms import ViewCathalog, MovieEd, MovieDel
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
    """Редактирование/создание записи в каталоге фильмов."""

    curr_id = flask_login.current_user.id
    # Проверка привилегий
    with db_session.create_session() as session:
        check_privelege = UserPriveleges.check_user_privelege(curr_id, "cathalog", session)
        if check_privelege is None:
            return redirect("/cathalog")  # Возвращаем редирект, если нет прав

    edit_id = request.args.get("id", type=int)  # Убираем значение по умолчанию None, т.к. обрабатывается ниже
    movie = Movie()  # Объявляем переменную movie
    form = MovieEd()
    render_page = lambda msg=None: render_template(
        "cathalog_edit.html", message=msg, form=form, form_del=MovieDel()
    )
    edit_movie = lambda session: session.query(Movie).get(edit_id) 
    def movie_none_chk(movie):
        if movie is None:
            raise Exception("Фильм не найден")
    # Находим инфу по фильму, заполняем поля
    if request.method == "GET":
        with db_session.create_session() as session:
            try:
                if edit_id:
                    movie = edit_movie(session)
                    movie_none_chk(movie)
                    form.process(obj=movie)
            except Exception as e:
                return render_page(f"Ошибка: {e}")
        return render_page()
    if request.method == "POST":
        if form.validate_on_submit() and form.submit.data:
            with db_session.create_session() as session:
                try:
                    if edit_id: movie = edit_movie(session)
                    movie_none_chk(movie)
                    form.populate_obj(movie)
                    if not edit_id: session.add(movie)
                    session.commit()
                    return render_page("Все окей")
                except Exception as e:
                    session.rollback()
                    return render_page(f"Ошибка: {e}")
            return render_page()
