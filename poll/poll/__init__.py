from flask import Blueprint

bp = Blueprint(
    'poll',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/poll/static'
)

from poll.poll import poll
