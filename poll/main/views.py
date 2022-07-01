from flask import render_template

from poll.models import Poll


def index():
    most_popular_polls = Poll.get_most_popular(5)
    most_recent_polls = Poll.get_most_recent(5)

    context = {
        'most_popular_polls': most_popular_polls,
        'most_recent_polls': most_recent_polls
    }

    return render_template('main/index.html', **context)
