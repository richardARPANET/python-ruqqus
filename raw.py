#!/usr/bin/env python3
import requests

class raw:

    def __init__(self, headers, client_id, secret):
        self.url = "https://ruqqus.com/"
        self.headers = headers
        self.client_id = client_id
        self.client_secret = secret

    def getFront(self):
        return requests.get(url=f"{self.url}api/v1/front/listing",
                            headers=self.headers).json()

    def getGuild(self, guildName):
        return requests.get(url=f"{self.url}api/v1/guild/{guildName}/listing",
                            headers=self.headers).json()

    def getUser(self, userName):
        return requests.get(url=f"{self.url}api/v1/user/{userName}",
                            headers=self.headers).json()

    def getPost(self, postId):
        return requests.get(url=f"{self.url}api/v1/post/{postId}",
                            headers=self.headers).json()

    def getComment(self, commentId):
        return requests.get(url = f"{self.url}api/v1/comment/{commentId}",
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