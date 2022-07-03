from flask import Blueprint

from poll.main import views

bp = Blueprint(
    'main',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/main/static'
)

bp.add_url_rule('/', view_func=views.index)
