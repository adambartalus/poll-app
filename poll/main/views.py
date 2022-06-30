from flask import render_template

from poll.main import bp
from poll.models import Poll


@bp.route('/')
def index():
    most_popular_polls = Poll.get_most_popular(5)
    most_recent_polls = Poll.get_most_recent(5)
    return render_template('main/index.html', most_popular_polls=most_popular_polls, most_recent_polls=most_recent_polls)
