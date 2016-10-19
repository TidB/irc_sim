import datetime
import glob
import re

import markovify


MINIMUM_MESSAGES = 1000
MAX_TRIES = 1000
RC_BOTS = ["Spacenet"]
RC_PATTERN = re.compile(
        "\[RC\] "
        "05(?P<action>-) "
        "10(?P<title>.+?) "
        "by "
        "06(?P<user>.+?) "
        "- "
        "(?P<link>http://wiki.tf/.+?) "
        "(\(03(?P<bytes>[+-]?\d+?)\) )?"
        "\(05(?P<time>\d\d:\d\d:\d\d)\) "
        "\[Via 07(?P<name>\w+?)\]"
    )
ALIASES = {
    "TidPleb": "TidB",
    "TidKek": "TidB",
    "TidNub": "TidB",
    "TidPro": "TidB",
    "TidSpam": "TidB",
    "TidNope": "TidB",
    "TidBuff": "TidB",
    "TidNerf": "TidB",
    "Nikyes": "TidB",
    "umm": "TidB",
    "Niknayy": "TidB",
    "Ghafetti": "TidB",
    "TidSHUTUP": "TidB",
    "Tark_": "Tark",
    "Faghetti|Juice": "Faghetti",
    "Faghetti|Food": "Faghetti",
    "Nixshadow|oops": "Nixshadow",
}


class DefaultDict(dict):
    def __init__(self, factory):
        self.factory = factory
        super().__init__()

    def __missing__(self, key):
        self[key] = self.factory(key)
        return self[key]


class User:
    def __init__(self, nick):
        self.nick = nick
        self.messages = []
        self.markov_chain = None


def handle_line(line, users):
    timestamp, line = line[1:20], line[22:]
    timestamp = datetime.datetime(
        year=int(timestamp[:4]),
        month=int(timestamp[5:7]),
        day=int(timestamp[8:10]),
        hour=int(timestamp[11:13]),
        minute=int(timestamp[14:16]),
        second=int(timestamp[17:19]),
    )
    if line[0] != "<":  # Nick and the message
        return
    nick, message = line.split(" ", maxsplit=1)
    nick = nick[1:-1]  # Exclude brackets
    nick = ALIASES[nick] if nick in ALIASES else nick  # Resolve alias
    if nick[1:-1] in RC_BOTS:
        #handle_rc(message)
        pass
    else:
        handle_user(users[nick], message)


def handle_user(user, message):
    user.messages.append(message)


def handle_rc(message):
    # TODO
    for group in RC_PATTERN.finditer(message):
        print(group.groupdict())


def create_markov(user):
    user.markov_chain = markovify.NewlineText("\n".join(user.messages))
    del user.messages


def save(user, path):
    with open(path.format(user.nick), "w") as file:
        file.write(user.markov_chain.chain.to_json())


def main(glob_folder, cache_folder):
    users = DefaultDict(User)
    for file_path in glob.iglob(glob_folder):
        with open(file_path, encoding="utf-8") as file:
            text = file.read()
            for line in re.split("\\n(?=\[)", text.strip()):
                handle_line(line, users)

    for nick, user in users.items():
        if len(user.messages) < MINIMUM_MESSAGES:
            users[nick] = None
            continue

        create_markov(user)
        save(user, cache_folder)
        print(nick)
