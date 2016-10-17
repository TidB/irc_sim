import datetime
from sys import stdout


def do_step(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        args[0].default_step()

    return wrapper


class Channel:
    def __init__(self, name, users=None, output=stdout,
                 timestamp=datetime.datetime.now(), include_timestamp=True,
                 timestep=datetime.timedelta(seconds=1)):
        self.name = name
        self.users = [] if users is None else users
        self.output = output
        self.current_timestamp = timestamp
        self.include_timestamp = include_timestamp
        self.timestep = timestep

    def __str__(self):
        return self.name

    def step(self, step):
        self.current_timestamp += step

    def default_step(self):
        self.step(self.timestep)

    def generate_timestamp(self):
        return "[{}]".format(
            self.current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        )

    @do_step
    def _message(self, client, msg):
        print(
            "{timestamp}{client}{message}".format(
                timestamp=self.generate_timestamp() + " " if self.include_timestamp else "",
                client=client+" ",
                message=msg
            ),
            file=self.output
        )

    def say(self, msg):
        self._message("*", msg)

    def user_say(self, nick, msg):
        self._message("<"+nick+">", msg)

    def add(self, *users):
        for user in users:
            self.users.append(user)
            self.say("{nick} joined {channel}".format(
                nick=user.nick,
                channel=self.name
            ))

    def remove(self, *users):
        for user in users:
            try:
                self.users.remove(user)
                self.say("{nick} left {channel}".format(
                    nick=user.nick,
                    channel=self.name
                ))
            except ValueError:
                raise ValueError("User not in channel")

    def change_nick(self, old, new):
        self.say("{old} changed nick to {new}".format(
            old=old, new=new
        ))
