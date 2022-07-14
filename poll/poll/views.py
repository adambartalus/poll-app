from flask import render_template, request, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from poll.extensions import db
from poll.models import PollVote, PollTitle, Poll
from poll.poll.forms import CreatePollForm
from poll.utils import poll_exists, custom_login_message, add_poll


def poll():
    return redirect(url_for('poll.create_poll'))


@custom_login_message(message='You have to log in to vote')
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
            flash('You have successfully voted on this poll', 'success')

        return redirect(url_for('poll.get_poll', id_=id_))
    flash('You have to select at least one option', 'error')

    return redirect(url_for('poll.get_poll', id_=id_))


def get_poll(id_):
    if not poll_exists(id_):
        return redirect(url_for('main.index'))

    poll_ = Poll.query.get(id_)
    title = PollTitle.query.filter_by(poll_id=id_).first().text
    options = poll_.options
    multiple = poll_.multiple

    if current_user.is_authenticated and current_user.voted_on(id_):
        if request.referrer != url_for('poll.get_poll', id_=id_, _external=True):
            flash('You have already voted on this poll', 'info')

    context = {
        'poll_id': id_,
        'title': title,
        'options': options,
        'multiple': multiple
    }

    return render_template('poll/poll.html', **context)


def get_poll_result(id_):
    poll_ = Poll.query.get(id_)

    return render_template('poll/poll_result.html', poll=poll_)


def create_poll():
    form = CreatePollForm()
    if form.validate_on_submit():
        title = form.title.data
        options = form.answer_options.data
        multiple = form.multiple_choices.data

        options = filter(lambda x: x.strip(), options)
        id_ = add_poll(current_app, title, options, multiple)

        return redirect(url_for('poll.get_poll', id_=id_))

    return render_template('poll/create_poll.html', form=form)
