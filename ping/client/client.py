import socket
import random
import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ping.package import create_package


# generate message
content_size = random.randint(1, 30)
CONTENT = ''.join(random.choices(string.ascii_lowercase, k=content_size))

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.sendto(create_package(0, 0, CONTENT), ('127.0.0.1', 3000))
