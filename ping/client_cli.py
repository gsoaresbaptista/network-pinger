from client import UDPClient

client = UDPClient('127.0.0.1', 3000)
client.send_to_server()
client.wait_response()
