from poll.db import get_db


def poll_exists(id_):
    poll = get_db().execute(
        'SELECT *'
        ' FROM poll'
        ' WHERE id=?',
        [id_]
    ).fetchone()
    return poll is not None


def get_vote_count(poll_answer_id):
    c = get_db().execute(
        'SELECT count(*) as c'
        ' FROM poll_vote'
        ' WHERE answer_id=?',
        [poll_answer_id]
    ).fetchone()['c']
    return c
