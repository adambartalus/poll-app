from flask import Blueprint

from poll.user import views

bp = Blueprint(
    'user',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/user'
)

bp.add_url_rule('/voted-polls', view_func=views.voted_polls)
bp.add_url_rule('/my-polls', view_func=views.my_polls)
