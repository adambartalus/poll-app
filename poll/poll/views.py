from datetime import datetime

from flask import render_template, request, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from poll.model import db
from poll.models import PollVote, PollTitle, PollOption, Poll
from poll.poll import bp
from poll.poll.forms import CreatePollForm
from poll.utils import poll_exists, get_vote_count


@bp.route('/poll')
def poll():
    return redirect(url_for('poll.create_poll'))


@bp.route('/poll/<int:id_>', methods=['POST'])
@login_required
def vote_poll(id_):
    if current_user.voted_on(id_):
        flash('You have already voted on this poll', 'error')
        return redirect(url_for('poll.get_poll', id_=id_))
    choices = request.form.getlist('choice')
    if choices:
        if (not Poll.query.get(id_).multiple) and len(choices) > 1:
            flash('Multiple choices are not allowed on this poll', 'error')
        else:
            for choice in choices:
                db.session.add(PollVote(poll_option_id=choice, user_id=current_user.id))
            db.session.commit()
        return redirect(url_for('poll.get_poll', id_=id_))
    flash('You have to select at least one option', 'error')
    return redirect(url_for('poll.get_poll', id_=id_))


@bp.route('/poll/<int:id_>')
def get_poll(id_):
    if not poll_exists(id_):
        return redirect(url_for('main.index'))

    poll_ = Poll.query.get(id_)
    title = PollTitle.query.filter_by(poll_id=id_).first().text
    options = poll_.options
    multiple = poll_.multiple

    options = map(lambda x: {'id': x.id, 'text': x.text, 'count': get_vote_count(x.id)}, options)

    context = {
        'poll_id': id_,
        'title': title,
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

        new_poll = Poll(multiple=multiple, created=datetime.now())
        db.session.add(new_poll)
        db.session.flush()

        db.session.add(PollTitle(poll_id=new_poll.id, text=title))

        for option in options:
            db.session.add(PollOption(poll_id=new_poll.id, text=option))
        db.session.commit()

        return redirect(url_for('poll.get_poll', id_=new_poll.id))
    return render_template('create_poll.html', form=form)
