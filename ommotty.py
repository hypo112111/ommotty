import socket
import random

SERVER, PORT = "irc.chat.twitch.tv", 6667
CHANNEL = "#default"
SERVINGOMMOS = 0

def set_channel():
    global CHANNEL
    CHANNEL = "#" + input("Enter channel name: ").strip().lower()

def set_ommono():
    global SERVINGOMMOS
    try:
        SERVINGOMMOS = int(input("Enter number of ommobots: "))
    except ValueError:
        print("Please enter a valid number.")
        SERVINGOMMOS = 0

class Ommobot:
    def __init__(self, token, nickname, channel):
        self.nickname = nickname
        self.channel = channel
        self.sock = socket.socket()

        try:
            self.sock.connect((SERVER, PORT))
            self.sock.send(f"PASS {token}\r\n".encode("utf-8"))
            self.sock.send(f"NICK {nickname}\r\n".encode("utf-8"))
            self.sock.send(f"JOIN {channel}\r\n".encode("utf-8"))
        except Exception as e:
            print(f"Connection error for {nickname}: {e}")
            self.sock = None  # Mark as inactive

    def send_message(self, message):
        if self.sock:
            try:
                self.sock.send(f"PRIVMSG {self.channel} :{message}\r\n".encode("utf-8"))
            except Exception as e:
                print(f"Message send error for {self.nickname}: {e}")

class OmmobotNet:
    def __init__(self):
        global CHANNEL, SERVINGOMMOS

        self.ommobots = []
        self.pool = []

        if CHANNEL == "#default":
            set_channel()
            print(f"Channel set to {CHANNEL}")
        if SERVINGOMMOS == 0:
            set_ommono()
            print(f"Serving {SERVINGOMMOS} ommobots")
        
        try:
            with open("ommos.txt", "r") as file:
                self.ommobots = [line.strip().split(" ") for line in file if line.strip()]
                print(f"Loaded {len(self.ommobots)} bots.")
        except FileNotFoundError:
            print("❌ Error: 'ommos.txt' file not found.")
            return

        self.make_pool()

    def make_pool(self):
        self.pool.clear()

        if len(self.ommobots) < SERVINGOMMOS:
            print("Not enough bots to make a pool.")
            return

        lines = random.sample(self.ommobots, SERVINGOMMOS)
        print(f"Creating pool of {len(lines)} bots.")

        for bot, token in lines:
            new_bot = Ommobot(token, bot, CHANNEL)
            if new_bot.sock:
                self.pool.append(new_bot)

        print(f"Connected {len(self.pool)} bots to {CHANNEL}")

    def send_message(self, message):
        self.make_pool()
        for bot in self.pool:
            bot.send_message(message)
        print(f"Sent message: {message}")

# Main runner
ommotty = OmmobotNet()

while True:
    msg = input("> ")
    if msg.lower() == "exit":
        break
    elif msg.lower() == "set_channel":
        set_channel()
    elif msg.lower() == "set_ommono":
        set_ommono()
    else:
        ommotty.send_message(msg)