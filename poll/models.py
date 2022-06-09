from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id_, username, password_hash):
        self.id = id_
        self.username = username
        self.password_hash = password_hash
