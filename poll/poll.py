from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from poll.utils import poll_exists
from poll.utils import get_vote_count

from poll.model import db
from poll.models import PollVote, PollQuestion, PollOption, Poll

bp = Blueprint('poll', __name__)


@bp.route('/poll/<int:id_>', methods=['GET', 'POST'])
def get_poll(id_):
    if request.method == 'POST':
        choices = request.form.getlist('choice')
        if choices:
            for choice in choices:
                db.session.add(PollVote(poll_option_id=choice))
            db.session.commit()
            return redirect(request.referrer)
    if not poll_exists(id_):
        return redirect(url_for('main.index'))

    question = PollQuestion.query.filter_by(poll_id=id_).first().text
    options = PollOption.query.filter_by(poll_id=id_).all()
    multiple = Poll.query.get(id_).multiple

    options = map(lambda x: {'id': x.id, 'text': x.text, 'count': get_vote_count(x.id)}, options)

    context = {
        'poll_id': id_,
        'question': question,
        'options': options,
        'multiple': multiple
    }
    return render_template('poll.html', **context)


@bp.route('/poll', methods=['POST'])
def poll():
    question = request.form.get('question')
    answers = request.form.getlist('answer')
    multiple = request.form.get('multiple')

    answers = filter(lambda x: x.strip(), answers)

    new_poll = Poll(multiple=multiple is not None)
    db.session.add(new_poll)
    db.session.commit()

    db.session.add(PollQuestion(poll_id=new_poll.id, text=question))
    db.session.commit()

    for answer in answers:
        db.session.add(PollOption(poll_id=new_poll.id, text=answer))
    db.session.commit()

    return redirect(url_for('poll.poll') + f'/{new_poll.id}')
