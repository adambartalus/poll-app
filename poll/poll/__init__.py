from flask import Blueprint

from poll.poll import views

bp = Blueprint(
    'poll',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/poll/static'
)

bp.add_url_rule('/poll', view_func=views.poll)
bp.add_url_rule('/poll/<int:id_>', view_func=views.get_poll)
bp.add_url_rule('/poll/<int:id_>/result', view_func=views.get_poll_result)
bp.add_url_rule('/poll/<int:id_>', view_func=views.vote_poll, methods=['POST'])
bp.add_url_rule('/poll/create', view_func=views.create_poll, methods=['GET', 'POST'])
