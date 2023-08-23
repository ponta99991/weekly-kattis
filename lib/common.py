
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
    score: float
    time: float
    date: float

    def __init__(self, username, score, time, date = 0):
        self.username = username
        self.score = score
        self.time = time
        self.date = date

class Leaderboard:
    task: str
    user: User

    def __init__(self, task, user = []):
        self.task = task
        self.user = user
