# Network-Pinger

## About

A UDP client and server pinger to the computer engineering course of Federal University of Espírito Santo, Brazil.
This is a very simple implementation of a pinger, using UDP although ICMP is ideal for this type of application, once the main goal is learning.
The client can save all sent and received packet data to a csv file, while the server and the client can save the stdout output to a txt logger file. Default timeout is 10 seconds for both server and client.

## Running

Make sure you have ```Python 3.10.6``` or a more recent version and be in the root folder.

First, install all dependencies:

```pip install -r requirements.txt```

To run the server, do:

```python pinger/server_cli.py```

For the client, run:

```python pinger/client_cli.py```

Some parameters can be passed to  both cli, to see more about this add ```--help``` to the end of either command.


## Simulations

The server can simulate a few possible fauls, such as:
- Delayed response: Wait min **10ms** and max **200ms** to send the response
- Packet loss: Response packet is not sent to client with **25%** chance
- Packet protocol errors: Add a protocol error to packet with **25%** chance

The client handles the failures simulated by the server, considering them when calculating the statistics. All simulations must be enabled if desired as they are disabled by default.

## Server Parameters

Some parameters can be passed to the server cli to change certain behaviors. Are they:
- ```-l``` or ```--logger```: The server saves all stdout output in the server_log.txt file.
- ```-t NUMBER``` or ```--timeout NUMBER```: The server stops after **NUMBER** seconds with no requests.
- ```-sd``` or ```--simulate_delay```: The server allows packet delay response simulation.
- ```-sl``` or ```--simulate_loss```: The server allows packet loss simulation.
- ```-sp``` or ```--simulate_protocol_error```: The server allows packet protocol errors simulation.


An example to run a server cli with parameters is:

```python pinger/server_cli.py -t 2 -sd -sl -sp```

Server running with a timeout of 2 seconds and simulating delay and loss.


## Client Parameters

The client can receive parameters below by command line:
- ```-l``` or ```--logger```: The client saves all stdout output in the client_log.txt file.
- ```-t NUMBER``` or ```--timeout NUMBER```: The client will consider the packet lost after waiting for **NUMBER** seconds.
- ```-c``` or ```--csv```: The client saves all sent and received packet data in the packets_data.csv file.
-  ```-p NUMBER``` or ```--packets NUMBER```: The client will send **NUMBER** packets to the server.

An example to run a client cli with parameters is:

```python pinger/client_cli.py --timeout 1 --csv --packets 10```

## Example

Running the following commands in separate terminals:

```python pinger/server_cli.py -t 3 -sd -sl -sp -l```

```python pinger/client_cli.py --packets 5 --timeout 1 --csv --logger```

We got the following output files:

**server_log.txt:**
```
2022-11-06 00:46:54 - INIT  | UDP Server initialized
------------------------------------------------------------
2022-11-06 00:46:54 - CONFG | simulate_delay set as True
2022-11-06 00:46:54 - CONFG | simulate_loss set as True
2022-11-06 00:46:54 - CONFG | simulate_protocol_error set as True
------------------------------------------------------------
2022-11-06 00:46:54 - INIT  | Listen packets on 127.0.0.1:3000
2022-11-06 00:46:54 - INIT  | Response socket created
2022-11-06 00:46:54 - INFO  | Set 3 seconds as maximum no-request time
2022-11-06 00:46:55 - RECV  | packet received from 127.0.0.1:46239
2022-11-06 00:46:55 - INFO  | Simulating packet delay with 66.66ms
2022-11-06 00:46:55 - SENT  | response sent to 127.0.0.1:46239
2022-11-06 00:46:55 - RECV  | packet received from 127.0.0.1:46239
2022-11-06 00:46:55 - INFO  | Simulating packet ping/pong error
2022-11-06 00:46:55 - INFO  | Simulating packet delay with 160.68ms
2022-11-06 00:46:55 - SENT  | response sent to 127.0.0.1:46239
2022-11-06 00:46:55 - RECV  | packet received from 127.0.0.1:46239
2022-11-06 00:46:55 - INFO  | Simulating packet loss
2022-11-06 00:46:56 - RECV  | packet received from 127.0.0.1:46239
2022-11-06 00:46:57 - INFO  | Simulating packet delay with 182.56ms
2022-11-06 00:46:57 - SENT  | response sent to 127.0.0.1:46239
2022-11-06 00:46:57 - RECV  | packet received from 127.0.0.1:46239
2022-11-06 00:46:57 - INFO  | Simulating packet delay with 147.01ms
2022-11-06 00:46:57 - SENT  | response sent to 127.0.0.1:46239
2022-11-06 00:47:00 - ERROR | Maximum no-request time of 3 seconds exceeded
2022-11-06 00:47:00 - END   | Server connection closed
```

**client_log.txt:**
```
2022-11-06 00:46:55 - INIT  | UDP Client initialized
2022-11-06 00:46:55 - INIT  | Socket created
2022-11-06 00:46:55 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-06 00:46:55 - RECV  | Reply received successfully, rtt = 67ms
2022-11-06 00:46:55 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-06 00:46:55 - ERROR | Ping-pong received incorrectly
2022-11-06 00:46:55 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-06 00:46:56 - ERROR | Timeout waiting for response, packet was lost
2022-11-06 00:46:56 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-06 00:46:57 - RECV  | Reply received successfully, rtt = 184ms
2022-11-06 00:46:57 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-06 00:46:57 - RECV  | Reply received successfully, rtt = 147ms
----------------------------------------------------------------------
2022-11-06 00:46:57 - INFO  | Total time = 1.5608 seconds
2022-11-06 00:46:57 - INFO  | 5 packets transmitted, 3 received.
2022-11-06 00:46:57 - INFO  | 40.00% packet loss.
2022-11-06 00:46:57 - INFO  | rtt min/avg/max/mdev = 67.000/132.667/184.000/59.802 ms
----------------------------------------------------------------------
2022-11-06 00:46:57 - END   | Client socket closed
```

**packets_data.csv:**
```
sid_sent,sid_received,type_sent,type_received,timestamp_sent,timestamp_received,message_sent,message_received,rtt
00000,00000,0,1,5588,5655,wlnpnixkcqrtyudmib,wlnpnixkcqrtyudmib,67.0
00001,00000,0,1,5655,5655,mkuisdfpt,wlnpnixkcqrtyudmib,None
00002,0000,0,0,5816,0000,dwvtgkbzalpopif,TIMEOUTERROR,None
00003,00003,0,1,6817,7001,rtdigzvwxowvdrvjqozoav,rtdigzvwxowvdrvjqozoav,184.0
00004,00004,0,1,7001,7148,nvqvthszkpgfyo,nvqvthszkpgfyo,147.0
```

Note that when a packet is lost the timestamp is **'0000'**, type_received **'0'** and the rtt **None**.
