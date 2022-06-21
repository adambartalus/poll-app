from flask import Blueprint, render_template, request, url_for, session
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, FieldList, BooleanField, SubmitField
from wtforms.validators import DataRequired

from poll.model import db
from poll.models import PollVote, PollQuestion, PollOption, Poll
from poll.utils import poll_exists
from poll.utils import get_vote_count


class CreatePollForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    answer_options = FieldList(StringField(''), min_entries=2, label='Answer options')
    multiple_choices = BooleanField('Multiple choices')


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


@bp.route('/poll/create', methods=['GET', 'POST'])
def create_poll():
    form = CreatePollForm()
    if form.validate_on_submit():
        title = form.title.data
        # options = request.form.getlist('answer-option')
        options = form.answer_options.data
        multiple = form.multiple_choices.data

        options = filter(lambda x: x.strip(), options)

        new_poll = Poll(multiple=multiple)
        db.session.add(new_poll)
        db.session.commit()

        db.session.add(PollQuestion(poll_id=new_poll.id, text=title))
        db.session.commit()

        for option in options:
            db.session.add(PollOption(poll_id=new_poll.id, text=option))
        db.session.commit()

        return redirect(url_for('poll.get_poll', id_=new_poll.id))
    return render_template('create_poll.html', form=form)


@bp.route('/poll/create/add_option', methods=['GET'])
def add_option():
    return {
        "valami": 2
    }
