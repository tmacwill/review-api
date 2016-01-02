import json
import kata.db
import requests

import api.lib

class User(kata.db.Object):
    __table__ = 'users'

class UserFromToken(kata.db.Container):
    def init(self, token):
        self.token = token

    def expire(self):
        return api.lib.DAY

    def key(self):
        return 'u:t:%s' % self.token

    def pull(self):
        return User.get({'token': self.token}, one=True)

class UserFromId(kata.db.MultiContainer):
    def expire(self):
        return api.lib.WEEK

    def key(self, item):
        return 'u:%s' % item

    def source(self):
        return User, 'id'

def create(facebook_token):
    response = requests.get(
        'https://graph.facebook.com/v2.5/me?fields=id,name,email',
        headers={
            'Authorization': 'OAuth %s' % facebook_token
        }
    )

    if response.status_code != 200:
        return

    # get user info from facebook SDK
    facebook_user = json.loads(response.text)
    facebook_id = facebook_user['id']
    email = facebook_user.get('email', '')
    name = facebook_user['name']

    # check if we already have a user with this facebook ID
    user = User.get({'facebook_id': facebook_user['id']}, one=True)
    if not user:
        return User.create({
            'facebook_id': facebook_id,
            'facebook_token': facebook_token,
            'email': email,
            'name': name,
            'token': api.lib.generate_slug(64)
        })

    # update existing user with latest facebook values
    sql = 'update %s ' % User.__table__
    sql += '''
        set facebook_token = %s, email = %s, name = %s
        where facebook_id = %s
    '''

    kata.db.execute(sql, (facebook_token, email, name, facebook_id))
    return user

def current_user(request):
    token = request.headers.get('AUTHORIZATION', '').split(' ')
    if len(token) < 2:
        return None

    return UserFromToken(token[1]).get()
