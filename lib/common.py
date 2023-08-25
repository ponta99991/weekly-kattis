
import struct
from collections import namedtuple
from dataclasses import dataclass

format_ = "6shhih50s2s"

# User = namedtuple('User',[
#     'username',
#     'score',
#     'time',
#     'date'
# ])

# Leaderboard = namedtuple('Leaderboard',[
#     'task',
#     'user'
# ])


class User:
    alias: str
    username: str
    runtime: float
    date: float
    lang: str

    def __init__(self, alias, username, lang, runtime, date = 0):
        self.alias = alias
        self.username = username
        self.lang = lang
        self.runtime = runtime
        self.date = date

class Leaderboard:
    task: str
    user: User

    def __init__(self, task, user):
        self.task = task
        self.user = user
