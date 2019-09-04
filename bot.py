import cfg
import socket
import re
from time import sleep

def chat(sock, msg):
    # Send a chat message to the server.
    sock.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))

def ban(sock, user):
    # Ban a user from the current channel
    chat(sock, ".ban {}".format(user))

def timeout(sock, user, seconds=600):
    # Timeout a user for ten minutes
    chat(sock, ".timeout {}".format(user, seconds))

s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
chat(s, "Hello everyone!")
while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0) # return the entire match
        message = CHAT_MSG.sub("", response)
        print(username + ": " + message)
        if message.strip() == "!hello":
            chat(s, "Hello, {} how you doin?".format(username))
    sleep(1 / cfg.RATE)
