from werkzeug.exceptions import HTTPException, default_exceptions
from flask import Response, render_template


def versatile_errorhandler(http_exception: HTTPException) -> Response:
    """Универсальный обработчик http ошибок, рендерящий шаблон с информацией"""
    if hasattr(http_exception, 'data'):
        error_desc = http_exception.data
    else:
        error_desc = http_exception.description

    return render_template(
        'back/error.html',
        error_code=http_exception.code,
        error_name=http_exception.name,
        error_description=error_desc)


def register_errorhandlers(app) -> None:
    """Регистрирует обработку всех поддерживаемыех http exceptions"""
    for status_code, http_exc in default_exceptions.items():
        if status_code < 400:
            continue
        app.register_error_handler(http_exc, versatile_errorhandler)
