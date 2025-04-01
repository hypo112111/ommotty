import socket

def load_settings():
  global SERVER, PORT, CHANNEL
  with open("settings.txt", "r") as file:
    lines = []
    for line in file:
      lines.append(line.strip().split(' '))
    SERVER, PORT, CHANNEL = lines[0][1], int(lines[1][1]), lines[2][1]
  

class ommobot:
  def __init__(self, TOKEN, NICKNAME, CHANNEL):
    # Connect to Twitch IRC
    self.sock = socket.socket()
    self.sock.connect((SERVER, PORT))
    self.sock.send(f"PASS {TOKEN}\n".encode("utf-8"))
    self.sock.send(f"NICK {NICKNAME}\n".encode("utf-8"))
    self.sock.send(f"JOIN {CHANNEL}\n".encode("utf-8"))
  
  # Function to send messages
  def send_message(self, message):
    self.sock.send(f"PRIVMSG {CHANNEL} :{message}\n".encode("utf-8"))

class ommobotnet:

  ommobots = []
  
  def __init__(self):
    bots, tokens = [], []
    with open("ommos.txt", "r") as file:
      lines = []
      for line in file:
        lines.append(line.strip().split(' '))
      for line in lines:
        bots.append(line[0])
        tokens.append(line[1])
    
    for bot, token in zip(bots, tokens):
      self.ommobots.append(ommobot(token, bot, CHANNEL))

    print(f"Connected to {CHANNEL}")
  
  def send_message(self, message):
    for bot in self.ommobots:
      bot.send_message(message)
    
    print(f"Sent: {message}")

# Example usage

load_settings()

ommotty = ommobotnet()

while True:
    msg = input("Enter message: ")
    if msg.lower() == "exit":
        break
    ommotty.send_message(msg)