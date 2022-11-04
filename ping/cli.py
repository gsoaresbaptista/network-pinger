from server import Server, UDPServer

server: Server = UDPServer()
server.connect('127.0.0.1', 3000)
server.listen()
server.disconnect()
