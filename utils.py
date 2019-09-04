import cfg
import random

#------------------------------------------------------------------------------#
# Current commands and other utility dicts/lists

COMMANDS = [
    "!hello", "!commands"
]

BIRD_COMMANDS = [
    "!randomTANK", "!randomDPS", "!randomSUPPORT"
]

HEROES = {
    "TANK": [
        "D.Va", "Orisa", "Reinhardt", "Roadhog", "Sigma", "Winston",
        "Wrecking Ball", "Zarya"
        ]
    ,
    "DPS": [
        "Ashe", "Bastion", "Doomfist", "Genji", "Hanzo", "Junkrat", "McCree",
        "Mei", "Pharah", "Reaper", "Soldier 76", "Sombra", "Symmetra",
        "Torbjorn", "Tracer", "Widowmaker"
        ]
    ,
    "SUPPORT": [
        "Ana", "Baptiste", "Brigitte", "Lucio", "Mercy", "Moira", "Zenyatta"
        ]
}

#------------------------------------------------------------------------------#
# network functions

def chat(sock, msg):
    # Send a chat message to the server.
    sock.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))

def ban(sock, user):
    # Ban a user from the current channel
    chat(sock, ".ban {}".format(user))

def timeout(sock, user, seconds=600):
    # Timeout a user for ten minutes
    chat(sock, ".timeout {}".format(user, seconds))

#------------------------------------------------------------------------------#
#  Command handler

def command_handler(sock, username, message):
    check_cmd = message.strip()
    if username == "thebirdddd":
        if check_cmd in BIRD_COMMANDS:
            if check_cmd.startswith("!random"):
                try:
                    hero_class = check_cmd[7:]
                    hero_length = len(HEROES[hero_class])
                    rand = random.randint(0, hero_length)
                    hero = HEROES[hero_class][rand]
                    chat(sock, "{}!".format(hero))
                except:
                    pass
    if check_cmd in COMMANDS:
        if check_cmd == "!hello":
            chat(sock, "Hello, {} how you doin?".format(username))
        if check_cmd == "!commands":
            general_cmds = "EVERYONE: "
            for cmd in COMMANDS:
                general_cmds += "{} ".format(cmd)
            bird_cmds = "THEBIRDDDD: "
            for cmd in BIRD_COMMANDS:
                bird_cmds += "{} ".format(cmd)
            msg = "{} {}".format(general_cmds, bird_cmds)
            chat(sock, msg)
