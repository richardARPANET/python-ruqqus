#!/usr/bin/env python3
import requests
from time import time

class Raw:
    """
    Pass in a
    :client_id and :client_secret
    :code or :access_token or :refresh_token
    """
    def __init__(self, client_id, client_secret, code=None, access_token=None, refresh_token=None):

        self.headers = {}
        self.url = "https://ruqqus.com"
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.code = code
        self.user_agent = None
        self.token_expire_utc = 0
        self.header = {}

        self.getHeaders(userAgent="tester by @arkitekt")

        if not self.client_id or not self.client_secret:
            exit("You must provide both a 'client_id' and 'client_secret")

        elif self.client_id and self.client_secret and not self.code and not self.access_token:

            if refresh_token:
                self.refreshToken()

            else:
                exit("You must provide either a 'code', 'access_token', or a 'refresh_token'.")

        elif self.client_id and self.client_secret and self.code and not self.access_token:

            if self.refresh_token:
                self.refreshToken()

            else:
                self.getAccessToken()

    def admin(self):
        # TODO: admin stuff?
        pass

    def mod(self):
        # TODO: Mod stuff
        pass

    def identity(self):
        self.getHeaders()

        return requests.get(url=f"{self.url}/api/v1/identity",
                            headers=self.headers).json()

    def user(self, userName=None, type=None):

        self.getHeaders()

        if not userName:
            return {"error": "You must provide a username."}

        if type:
            type = str(type).lower()

        # Default to user
        if not type or type == "user":
            return requests.get(url=f"{self.url}/api/v1/user/{userName}",
                                 headers=self.headers).json()

        elif type == "is_available":
            return requests.get(url=f"{self.url}/api/v1/is_available/{userName}",
                                headers=self.headers).json()

        elif type == "sub":
            return requests.post(url=f"{self.url}/api/follow/{userName}",
                                headers=self.headers).json()

        elif type == "unsub":
            return requests.post(url=f"{self.url}/api/unfollow/{userName}",
                                 headers=self.headers).json()
        else:
            return {"error": "Invalid Call"}

    def guild(self, guildName=None, type=None):

        self.getHeaders(userAgent="tester by @arkitekt")

        if not guildName:
            return {"error": "You must provide a guildName."}

        if type:
            type = str(type).lower()


        if not type or type == "guild":
            return requests.get(url=f"{self.url}/api/v1/guild/{guildName}",
                                 headers=self.headers).json()

        elif type == "is_available":
            # Default to is_available
            return requests.get(url=f"{self.url}/api/v1/board_available/{guildName}",
                                headers=self.headers).json()

        elif type == "sub":
            return requests.post(url=f"{self.url}/api/v1/subscribe/{guildName}",
                                headers=self.headers).json()

        elif type == "unsub":
            return requests.post(url=f"{self.url}/api/v1/unsubscribe/{guildName}",
                                 headers=self.headers).json()
        else:
            return {"error": "Invalid Call"}



    def get(self, type=None, sort=None, time=None, guildName=None, userName=None, postId=None, commentId=None):

        self.getHeaders(userAgent="tester by @arkitekt")

        if not type:
            return {"error": "You must specify which 'type' of get to use"}

        else:
            type = str(type).lower()

        if time:
            time = str(time).lower()

            if time not in ["day", "week", "month", "year"]:
                return {"error": "Invalid time parameter."}

        if sort:
            sort = str(sort).lower()

            if sort not in ["top", "hot", "disputed", "activity", "new"]:
               return {"error": "Invalid sort parameter."}

        if type == "front":

            if sort:

                if time:

                    return requests.get(url=f"{self.url}/api/v1/front/listing?sort={sort}&time={time}",
                                        headers=self.headers).json()

                return requests.get(url=f"{self.url}/api/v1/front/listing?sort={sort}",
                                    headers=self.headers).json()

            return requests.get(url=f"{self.url}/api/v1/front/listing",
                                headers=self.headers).json()

        elif type == "guild":

            if not guildName:
                return {"error": "You must provide a guildName"}

            else:
                guildName = str(guildName)

            if sort:

                if time:

                    return requests.get(url=f"{self.url}/api/v1/guild/{guildName}/listing?sort={sort}&time={time}",
                                        headers=self.headers).json()

                return requests.get(url=f"{self.url}/api/v1/guild/{guildName}/listing?sort={sort}",
                                    headers=self.headers).json()

            return requests.get(url=f"{self.url}/api/v1/guild/{guildName}/listing",
                                headers=self.headers).json()

        elif type == "user":

            if not userName:
                return {"error": "You must provide a userName."}

            else:
                userName = str(userName)

            return requests.get(url=f"{self.url}/api/v1/user/{userName}",
                                headers=self.headers).json()

        elif type == "post":

            if not postId:
                return {"error": "You must provide a postId."}

            else:
                postId = str(postId)

            return requests.get(url=f"{self.url}/api/v1/post/{postId}",
                                headers=self.headers).json()

        elif type == "comment":

            if not commentId:
                return {"error": "You must provide a commentId."}

            else:
                commentId = str(commentId
                                )
            return requests.get(url=f"{self.url}/api/v1/comment/{commentId}",
                                headers=self.headers).json()
        else:
            return {"error": "Invalid Call"}

    def getHeaders(self, userAgent=None, accessToken=None):

        if self.access_token:
            self.headers = {"Authorization": "Bearer " + self.access_token}

        elif accessToken:
            self.headers = {"Authorization": "Bearer " + accessToken}

        else:
            return {"error": "You must provide an accessToken."}

        if userAgent:
            self.header["user-agent"] = userAgent
            self.user_agent = userAgent

        elif self.user_agent:
            self.header["user-agent"] = self.user_agent

        else:
            return {"error": "You must provide a user-agent."}

        # refresh token 30 seconds before expiration
        if self.refresh_token and self.token_expire_utc >= int(time() - 30):
            self.refreshToken()

    def refreshToken(self, refreshToken=None):

        data = {"client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh"}

        if not self.refresh_token:

            if refreshToken:
                data["refresh_token"] = refreshToken

        else:
            data["refresh_token"] = self.refresh_token

        r = requests.post(url=f"{self.url}/oauth/grant",
                          headers=self.headers,
                          data=data).json()

        self.access_token = r['access_token']

        return r

    def getAccessToken(self):

        self.getHeaders(userAgent="tester by @arkitekt")

        data = {"client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "code",
                "code": self.code
                }

        r = requests.post(url=f"{self.url}/oauth/grant",
                          headers=self.headers,
                          data=data).json()

        self.access_token = r['access_token']
        self.refresh_token = r['refresh_token']
        self.token_expire_utc = r['expires_at']
        return r