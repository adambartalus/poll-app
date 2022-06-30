from flask import render_template
from flask_login import current_user, login_required

from poll.user import bp


@bp.route('voted-polls')
@login_required
def voted_polls():
    polls = current_user.get_voted_polls()
    return render_template('user/voted_polls.html', polls=polls)


@bp.route('my-polls')
@login_required
def my_polls():
    polls = current_user.polls
    return render_template('user/my_polls.html', polls=polls)
