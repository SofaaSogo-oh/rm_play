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
        check_privelege = (
            session.query(UserPriveleges)
            .filter(
                (UserPriveleges.id == curr_id) & (UserPriveleges.name == "cathalog")
            )
            .first()
        )
        if check_privelege is None:
            return redirect("/cathalog")  # Возвращаем редирект, если нет прав

    form = MovieEd()
    form_del = MovieDel()
    edit_id = request.args.get("id", type=int)  # Убираем значение по умолчанию None, т.к. обрабатывается ниже
    movie = None  # Объявляем переменную movie
    render_page = lambda msg=None, form=form: render_template(
        "cathalog_edit.html", message=msg, form=form, form_del=form_del
    )

    with db_session.create_session() as session:
        if edit_id:
            movie = session.query(Movie).get(edit_id)
            if movie is None:
                return render_page("Фильм не найден") # Обработка случая, если movie не найден
            # form.process(obj=movie) # Заполняем форму данными из объекта movie
        else:
            movie = Movie() # Создаем новый экземпляр Movie для новой записи

        if form.validate_on_submit():
            # Копируем данные из формы в объект Movie
            form.populate_obj(movie)
            try:
                if not edit_id:  #  Если это новая запись
                    session.add(movie)
                session.commit()
                return render_page("Все окей")  # Убираем form из аргументов render_page
            except IntegrityError as e:
                session.rollback() # откатываем транзакцию в случае ошибки
                return render_page(f"Ошибка: {e}", form)

        if form_del.validate_on_submit() and edit_id is not None: #проверяем, что edit_id существует.
            #Проверка нужна для того, чтобы нельзя было удалить то, чего нет
            session.delete(movie)
            try:
                session.commit()
                return render_page("Фильм удален") # Убираем form из аргументов render_page
            except IntegrityError as e:
                session.rollback() # откатываем транзакцию в случае ошибки
                return render_page(f"Ошибка при удалении: {e}")

    return render_page(form) # Убираем form из аргументов render_page
