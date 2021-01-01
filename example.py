import os

from ruqqus import RuqqusClient

# Docs on how to get these: https://ruqqus.com/help/oauth
RUQQUS_APP_ID = os.environ['RUQQUS_APP_ID']
RUQQUS_APP_SECRET = os.environ['RUQQUS_APP_SECRET']
RUQQUS_REFRESH_TOKEN = os.environ['RUQQUS_REFRESH_TOKEN']

ruqqus = RuqqusClient(
    client_id=RUQQUS_APP_ID,
    client_secret=RUQQUS_APP_SECRET,
    refresh_token=RUQQUS_REFRESH_TOKEN,
)


def get_all_guild_posts(name):
    all_posts = []
    page = 1
    while True:
        print('Getting guild posts...')
        posts = ruqqus.get_guild_posts(name=name, page=page)
        all_posts.extend(posts['data'])
        if not posts['next_exists']:
            break
        page += 1
    return all_posts


submissions = get_all_guild_posts(name='Ruqqus')
print(submissions)
