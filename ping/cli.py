from server.udp_server import UDPServer
from server.server_interface import ServerInterface

server: ServerInterface = UDPServer()
server.connect('127.0.0.1', 3000)
server.listen()
server.disconnect()
