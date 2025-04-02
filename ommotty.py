import socket
import random

def load_settings():
    with open("settings.txt", "r") as file:
        lines = [line.strip().split(" ") for line in file]
    return lines[0][1], int(lines[1][1]), lines[2][1], int(lines[3][1])

SERVER, PORT, CHANNEL, SERVINGOMMOS = load_settings()

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
        self.ommobots = []
        self.pool = []

        try:
            with open("ommos.txt", "r") as file:
                lines = [line.strip().split(" ") for line in file]
            
            for bot, token in lines:
                new_bot = Ommobot(token, bot, CHANNEL)
                if new_bot.sock:  # Add only successfully connected bots
                    self.ommobots.append(new_bot)

            print(f"Connected {len(self.ommobots)} bots to {CHANNEL}")
            self.make_pool()
        except Exception as e:
            print(f"Error loading bots: {e}")

    def make_pool(self):
        self.pool.clear()
        if len(self.ommobots) < SERVINGOMMOS:
            print("Not enough bots to make a pool.")
            return

        self.pool = random.sample(self.ommobots, SERVINGOMMOS)
        print(f"New pool created with {len(self.pool)} bots.")

    def send_message(self, message):
        for bot in self.pool:
            bot.send_message(message)
        print(f"Sent message: {message}")

ommotty = OmmobotNet()

while True:
    msg = input("> ")
    if msg.lower() == "exit":
        break
    elif msg.lower() == "new_pool":
        ommotty.make_pool()
    else:
        ommotty.send_message(msg)