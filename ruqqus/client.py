#!/usr/bin/env python3
from time import time

import requests


class RuqqusClient:
    def __init__(
        self,
        client_id,
        client_secret,
        code=None,
        access_token=None,
        refresh_token=None,
    ):

        self.headers = {}
        self.url = 'https://ruqqus.com'
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self._refresh_token = refresh_token
        self.code = code
        self.user_agent = f'python-ruqqus-{self.client_id}'
        self.token_expire_utc = 0
        self.header = {}
        self.refresh_headers()

        if not self.client_id or not self.client_secret:
            exit("You must provide both a 'client_id' and 'client_secret")
        elif (
            self.client_id
            and self.client_secret
            and not self.code
            and not self.access_token
        ):
            if refresh_token:
                self.refresh_token()
            else:
                exit(
                    "You must provide either a 'code', 'access_token', "
                    "or a 'refresh_token'."
                )
        elif (
            self.client_id
            and self.client_secret
            and self.code
            and not self.access_token
        ):
            if self._refresh_token:
                self.refresh_token()

            else:
                self.get_access_token()

    def admin(self):
        raise NotImplementedError()

    def mod(self):
        raise NotImplementedError()

    def identity(self):
        self.refresh_headers()
        return requests.get(
            url=f'{self.url}/api/v1/identity', headers=self.headers
        ).json()

    def user(self, username=None, type=None):
        self.refresh_headers()
        if not username:
            return {'error': 'You must provide a username.'}
        if type:
            type = str(type).lower()

        # Default to user
        if not type or type == 'user':
            return requests.get(
                url=f'{self.url}/api/v1/user/{username}', headers=self.headers
            ).json()

        elif type == 'is_available':
            return requests.get(
                url=f'{self.url}/api/v1/is_available/{username}',
                headers=self.headers,
            ).json()

        elif type == 'sub':
            return requests.post(
                url=f'{self.url}/api/follow/{username}', headers=self.headers
            ).json()

        elif type == 'unsub':
            return requests.post(
                url=f'{self.url}/api/unfollow/{username}', headers=self.headers
            ).json()
        else:
            return {'error': 'Invalid Call'}

    def guild(self, name=None, type=None):
        self.refresh_headers()
        if not name:
            return {'error': 'You must provide a guildName.'}

        if type:
            type = str(type).lower()

        if not type or type == 'guild':
            return requests.get(
                url=f'{self.url}/api/v1/guild/{name}',
                headers=self.headers,
            ).json()

        elif type == 'is_available':
            # Default to is_available
            return requests.get(
                url=f'{self.url}/api/v1/board_available/{name}',
                headers=self.headers,
            ).json()

        elif type == 'sub':
            return requests.post(
                url=f'{self.url}/api/v1/subscribe/{name}',
                headers=self.headers,
            ).json()

        elif type == 'unsub':
            return requests.post(
                url=f'{self.url}/api/v1/unsubscribe/{name}',
                headers=self.headers,
            ).json()
        else:
            return {'error': 'Invalid Call'}

    def submit_post(self, *, guild, title, url):
        self.refresh_headers()
        return requests.post(
            url=f'{self.url}/api/v1/submit',
            headers=self.headers,
            data={
                'board': guild,
                'title': title,
                'url': url,
            },
        ).json()

    def get_guild_posts(self, *, name, page=1, sort='hot'):
        self.refresh_headers()
        url = f'{self.url}/api/v1/guild/{name.lstrip("+")}/listing'
        response = requests.get(
            url=url,
            params={'page': page, 'sort': sort},
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def get(
        self,
        type=None,
        sort=None,
        time=None,
        guild_name=None,
        username=None,
        post_id=None,
        comment_id=None,
    ):

        self.refresh_headers()

        if not type:
            return {'error': "You must specify which 'type' of get to use"}

        else:
            type = str(type).lower()

        if time:
            time = str(time).lower()

            if time not in ['day', 'week', 'month', 'year']:
                return {'error': 'Invalid time parameter.'}

        if sort:
            sort = str(sort).lower()

            if sort not in ['top', 'hot', 'disputed', 'activity', 'new']:
                return {'error': 'Invalid sort parameter.'}

        if type == 'front':

            if sort:

                if time:

                    return requests.get(
                        url=(
                            f'{self.url}/api/v1/front/listing'
                            f'?sort={sort}&time={time}'
                        ),
                        headers=self.headers,
                    ).json()

                return requests.get(
                    url=f'{self.url}/api/v1/front/listing?sort={sort}',
                    headers=self.headers,
                ).json()

            return requests.get(
                url=f'{self.url}/api/v1/front/listing', headers=self.headers
            ).json()

        elif type == 'guild':

            if not guild_name:
                return {'error': 'You must provide a guildName'}

            else:
                guild_name = str(guild_name)

            if sort:
                if time:
                    return requests.get(
                        url=(
                            f'{self.url}/api/v1/guild/{guild_name}/listing'
                            f'?sort={sort}&time={time}'
                        ),
                        headers=self.headers,
                    ).json()

                return requests.get(
                    url=(
                        f'{self.url}/api/v1/guild/{guild_name}/listing'
                        f'?sort={sort}'
                    ),
                    headers=self.headers,
                ).json()

            return requests.get(
                url=f'{self.url}/api/v1/guild/{guild_name}/listing',
                headers=self.headers,
            ).json()

        elif type == 'user':

            if not username:
                return {'error': 'You must provide a userName.'}

            else:
                username = str(username)

            return requests.get(
                url=f'{self.url}/api/v1/user/{username}', headers=self.headers
            ).json()

        elif type == 'post':

            if not post_id:
                return {'error': 'You must provide a postId.'}

            else:
                post_id = str(post_id)

            return requests.get(
                url=f'{self.url}/api/v1/post/{post_id}', headers=self.headers
            ).json()

        elif type == 'comment':

            if not comment_id:
                return {'error': 'You must provide a commentId.'}

            else:
                comment_id = str(comment_id)
            return requests.get(
                url=f'{self.url}/api/v1/comment/{comment_id}',
                headers=self.headers,
            ).json()
        else:
            return {'error': 'Invalid Call'}

    def refresh_headers(self, user_agent=None, access_token=None):

        if self.access_token:
            self.headers = {'Authorization': 'Bearer ' + self.access_token}

        elif access_token:
            self.headers = {'Authorization': 'Bearer ' + access_token}

        else:
            return {'error': 'You must provide an accessToken.'}

        if user_agent:
            self.header['user-agent'] = user_agent
            self.user_agent = user_agent

        elif self.user_agent:
            self.header['user-agent'] = self.user_agent

        else:
            return {'error': 'You must provide a user-agent.'}

        # refresh token 30 seconds before expiration
        if self._refresh_token and self.token_expire_utc >= int(time() - 30):
            self.refresh_token()

    def refresh_token(self, refresh_token=None):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh',
        }

        if not self._refresh_token:

            if refresh_token:
                data['refresh_token'] = refresh_token

        else:
            data['refresh_token'] = self._refresh_token

        r = requests.post(
            url=f'{self.url}/oauth/grant', headers=self.headers, data=data
        ).json()

        self.access_token = r['access_token']

        return r

    def get_access_token(self):

        self.refresh_headers()

        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'code',
            'code': self.code,
        }

        r = requests.post(
            url=f'{self.url}/oauth/grant', headers=self.headers, data=data
        ).json()
        self.access_token = r['access_token']
        self._refresh_token = r['refresh_token']
        self.token_expire_utc = r['expires_at']
        return r
