class User:
    def __init__(self, nick, channel=None):
        self.nick = nick
        self.channel = channel

    def __str__(self):
        return self.nick

    def say(self, msg):
        if self.channel is None:
            raise ValueError("User not in channel")
        self.channel.user_say(self.nick, msg)

    def join(self, channel):
        if self.channel is not None:
            raise ValueError("User already in channel")
        self.channel = channel
        self.channel.add(self)

    def leave(self):
        if self.channel is None:
            raise ValueError("User not in channel")
        self.channel.remove(self)
        self.channel = None

    def change_nick(self, new_nick):
        self.channel.change_nick(self.nick, new_nick)
        self.nick = new_nick
