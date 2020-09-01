#!/usr/bin/env python3
import requests
from time import time


class Raw:

    def __init__(self, headers, client_id, secret):
        self.url = "https://ruqqus.com"
        self.client_id = client_id
        self.client_secret = secret
        self.token_expire_utc = 0
        self.refresh_token = None
        # self.getAccessToken(code=ABCDEFG)

    def get(self, *args, **kwargs):

        type = kwargs['type'].lower()
        self.getHeaders(user_agent="tester by @arkitekt")

        if type == "front":
            return requests.get(url=f"{self.url}/api/v1/front/listing",
                                headers=self.headers).json()

        elif type == "guild":
            return requests.get(url=f"{self.url}/api/v1/guild/{kwargs['guildName']}/listing",
                                headers=self.headers).json()

        elif type == "user":
            return requests.get(url=f"{self.url}/api/v1/user/{kwargs['username']}",
                                headers=self.headers).json()

        elif type == "post":
            return requests.get(url=f"{self.url}/api/v1/post/{kwargs['postId']}",
                                headers=self.headers).json()

        elif type == "comment":
            return requests.get(url=f"{self.url}/api/v1/comment/{kwargs['commentId']}",
                                headers=self.headers).json()

    def getHeaders(self, *args, **kwargs):

        # refresh token 30 seconds before expiration
        if self.token_expire_utc >= int(time() - 30):
            self.refreshToken()

        self.headers = {"Authorization": "Bearer " + self.access_token,
                        "user-agent": kwargs['user_agent']
                        }

    def refreshToken(self, *args, **kwargs):

        data = {"client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh",
                "refresh_token": self.refresh_token
                }

        r = requests.post(url=f"{self.url}/oauth/grant",
                          headers=self.headers,
                          data=data).json()

        self.access_token = r['access_token']
        return r

    def getAccessToken(self, *args, **kwargs):
        self.getHeaders()

        data = {"client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "code",
                "code": code
                }

        r = requests.post(url=f"{self.url}/oauth/grant",
                          headers=self.headers,
                          data=data).json()

        self.access_token = r['access_token']
        return r
