from flask import render_template
from flask_login import current_user, login_required

from poll.user import bp
from poll.utils import get_voted_polls


@bp.route('voted-polls')
@login_required
def voted_polls():
    polls = get_voted_polls(current_user)
    return render_template('voted_polls.html', polls=polls)
