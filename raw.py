#!/usr/bin/env python3
import requests

class raw:

    def __init__(self, headers, client_id, secret):
        self.url = "https://ruqqus.com/"
        self.headers = headers
        self.client_id = client_id
        self.client_secret = secret

    def get(self, *args, **kwargs):
        type = kwargs['type'].lower()

        if type == "front":
            return requests.get(url=f"{self.url}api/v1/front/listing",
                                headers=self.headers).json()

        elif type == "guild":
            return requests.get(url=f"{self.url}api/v1/guild/{kwargs['guildName']}/listing",
                                headers=self.headers).json()

        elif type == "user":
            return requests.get(url=f"{self.url}api/v1/user/{kwargs['username']}",
                                headers=self.headers).json()

        elif type == "post":
            return requests.get(url=f"{self.url}api/v1/post/{kwargs['postId']}",
                                headers=self.headers).json()

        elif type == "comment":
            return requests.get(url = f"{self.url}api/v1/comment/{kwargs['commentId']}",
                               headers=self.headers).json()

    def refreshToken(self):
        data = {"client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh",
                "refresh_token": self.refresh_token
                }

        r = requests.post(url=f"{self.url}oauth/grant",
                             headers=self.headers,
                             data=data).json()

        self.access_token = r['access_token']

        self.headers = {"Authorization": "Bearer " + self.access_token,
                        "user-agent": self.headers['user_agent']
                        }
        return r
    def getAccessToken(self, code):
        data = {"client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "code",
                "code": code
                }

        r = requests.post(url=f"{self.url}oauth/grant",
                          headers=headers,
                          data=data).json()

        self.access_token = r['access_token']

        self.headers = {"Authorization": "Bearer " + self.access_token,
                        "user-agent": self.headers['user_agent']
                        }
        return r