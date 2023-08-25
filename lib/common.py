
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
    username: str
    time: float
    date: float
    lang: str

    def __init__(self, username, lang, time, date = 0):
        self.username = username
        self.lang = lang
        self.time = time
        self.date = date

class Leaderboard:
    task: str
    user: User

    def __init__(self, task, user):
        self.task = task
        self.user = user
