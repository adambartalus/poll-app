from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from poll.db import get_db
from poll.utils import poll_exists
from poll.utils import get_vote_count

bp = Blueprint('poll', __name__)


@bp.route('/poll/<int:id_>', methods=['GET', 'POST'])
def get_poll(id_):
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice:
            get_db().execute(
                'INSERT INTO poll_vote (poll_id, answer_id)'
                ' VALUES (?, ?)',
                [id_, choice]
            )
            get_db().commit()
            return redirect(request.referrer)
    if not poll_exists(id_):
        return redirect(url_for('main.index'))

    db = get_db()
    question = db.execute(
        'SELECT *'
        ' FROM poll_question'
        ' WHERE poll_id=?',
        [id_]
    ).fetchone()['body']
    
    answers = db.execute(
        'SELECT *'
        ' FROM poll_answer'
        ' WHERE poll_id=?',
        [id_]
    ).fetchall()
    answers = map(lambda x: {'id': x['id'], 'text': x['body'], 'count': get_vote_count(x['id'])}, answers)
    return render_template('poll.html', poll_id=id_, question=question, answers=answers)


@bp.route('/poll', methods=['POST'])
def poll():
    question = request.form.get('question')
    answers = request.form.getlist('answer')
    answers = filter(lambda x: x.strip(), answers)
    db = get_db()
    db.execute(
        'INSERT INTO poll DEFAULT VALUES'
    )
    db.commit()
    max_id = db.execute(
        'SELECT *'
        ' FROM poll'
        ' ORDER BY id DESC'
        ' LIMIT 1'
    ).fetchone()['id']
    db.execute(
        'INSERT INTO poll_question (poll_id, body)'
        ' VALUES (?, ?)',
        (max_id, question)
    )
    for answer in answers:
        db.execute(
            'INSERT INTO poll_answer (poll_id, body)'
            ' VALUES (?, ?)',
            (max_id, answer)
        )
    db.commit()

    return redirect(url_for('poll.poll') + f'/{max_id}')
