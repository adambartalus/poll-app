from flask import render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import redirect

from poll.model import db
from poll.models import PollVote, PollQuestion, PollOption, Poll
from poll.utils import poll_exists
from poll.utils import get_vote_count
from poll.poll import bp
from poll.poll.forms import CreatePollForm


@bp.route('/poll')
def poll():
    return redirect(url_for('poll.create_poll'))


@bp.route('/poll/<int:id_>', methods=['POST'])
@login_required
def vote_poll(id_):
    choices = request.form.getlist('choice')
    if choices:
        for choice in choices:
            db.session.add(PollVote(poll_option_id=choice))
        db.session.commit()
        return redirect(request.referrer)
    # TODO: handle invalid vote


@bp.route('/poll/<int:id_>')
def get_poll(id_):
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


@bp.route('/poll/create', methods=['GET', 'POST'])
def create_poll():
    form = CreatePollForm()
    if form.validate_on_submit():
        title = form.title.data
        options = form.answer_options.data
        multiple = form.multiple_choices.data

        options = filter(lambda x: x.strip(), options)

        new_poll = Poll(multiple=multiple)
        db.session.add(new_poll)
        db.session.flush()

        db.session.add(PollQuestion(poll_id=new_poll.id, text=title))

        for option in options:
            db.session.add(PollOption(poll_id=new_poll.id, text=option))
        db.session.commit()

        return redirect(url_for('poll.get_poll', id_=new_poll.id))
    return render_template('create_poll.html', form=form)
