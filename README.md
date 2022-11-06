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
- Delayed response: Wait min 10ms and max 200ms to send the response
- Packet loss: Response packet is not sent to client with 25% chance

The client handles the failures simulated by the server, considering them when calculating the statistics. All simulations must be enabled if desired as they are disabled by default.

## Server Parameters

Some parameters can be passed to the server cli to change certain behaviors. Are they:
- ```-l``` or ```--logger```: The server saves all stdout output in the server_log.txt file.
- ```-t NUMBER``` or ```--timeout NUMBER```: The server stops after **NUMBER** seconds with no requests.
- ```-sd``` or ```--simulate_delay```: The server allows packet delay response simulation.
- ```-sl``` or ```--simulate_loss```: The server allows packet loss simulation.


An example to run a server cli with parameters is:

```python pinger/server_cli.py -t 2 -sd -sl```

Server running with a timeout of 2 seconds and simulating delay and loss.


## Client Parameters

The client can receive parameters below by command line:
- ```-l``` or ```--logger```: The client saves all stdout output in the client_log.txt file.
- ```-t NUMBER``` or ```--timeout NUMBER```: The client will consider the packet lost after waiting for **NUMBER** seconds.
- ```-c``` or ```--csv```: The client saves all sent and received packet data in the packets_data.csv file.

An example to run a client cli with parameters is:

```python pinger/client_cli.py --timeout 1 --csv```

## Example

Running the following commands in separate terminals:

```python pinger/server_cli.py -t 3 -sd -sl -l```

```python pinger/client_cli.py --timeout 1 --csv --logger```

We got the following output files:

**server_log.txt:**
```
2022-11-05 23:06:46 - INIT  | UDP Server initialized
------------------------------------------------------------
2022-11-05 23:06:46 - CONFG | Setting simulate_delay set as True
2022-11-05 23:06:46 - CONFG | Setting simulate_loss set as True
------------------------------------------------------------
2022-11-05 23:06:46 - INIT  | Listen packets on 127.0.0.1:3000
2022-11-05 23:06:46 - INIT  | Response socket created
2022-11-05 23:06:46 - INFO  | Set 3 seconds as maximum no-request time
2022-11-05 23:06:47 - RECV  | packet received from 127.0.0.1:40468
2022-11-05 23:06:47 - SENT  | response sent to 127.0.0.1:40468
2022-11-05 23:06:48 - RECV  | packet received from 127.0.0.1:40468
2022-11-05 23:06:48 - SENT  | response sent to 127.0.0.1:40468
2022-11-05 23:06:48 - RECV  | packet received from 127.0.0.1:40468
2022-11-05 23:06:48 - SENT  | response sent to 127.0.0.1:40468
2022-11-05 23:06:48 - RECV  | packet received from 127.0.0.1:40468
2022-11-05 23:06:48 - SENT  | response sent to 127.0.0.1:40468
2022-11-05 23:06:49 - RECV  | packet received from 127.0.0.1:40468
2022-11-05 23:06:49 - SENT  | response sent to 127.0.0.1:40468
2022-11-05 23:06:49 - RECV  | packet received from 127.0.0.1:40468
2022-11-05 23:06:50 - SENT  | response sent to 127.0.0.1:40468
2022-11-05 23:06:50 - RECV  | packet received from 127.0.0.1:40468
2022-11-05 23:06:50 - SENT  | response sent to 127.0.0.1:40468
2022-11-05 23:06:50 - RECV  | packet received from 127.0.0.1:40468
2022-11-05 23:06:50 - SENT  | response sent to 127.0.0.1:40468
2022-11-05 23:06:50 - RECV  | packet received from 127.0.0.1:40468
2022-11-05 23:06:50 - SENT  | response sent to 127.0.0.1:40468
2022-11-05 23:06:53 - ERROR | Maximum no-request time of 3 seconds exceeded
2022-11-05 23:06:53 - END   | Server connection closed
```

**client_log.txt:**
```
2022-11-05 23:06:46 - INIT  | UDP Client initialized
2022-11-05 23:06:46 - INIT  | Socket created
2022-11-05 23:06:46 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-05 23:06:47 - ERROR | Timeout waiting for response, packet was lost
2022-11-05 23:06:47 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-05 23:06:48 - ERROR | Timeout waiting for response, packet was lost
2022-11-05 23:06:48 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-05 23:06:48 - RECV  | Reply received successfully, rtt = 173ms
2022-11-05 23:06:48 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-05 23:06:48 - RECV  | Reply received successfully, rtt = 112ms
2022-11-05 23:06:48 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-05 23:06:49 - ERROR | Timeout waiting for response, packet was lost
2022-11-05 23:06:49 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-05 23:06:49 - RECV  | Reply received successfully, rtt = 145ms
2022-11-05 23:06:49 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-05 23:06:50 - RECV  | Reply received successfully, rtt = 87ms
2022-11-05 23:06:50 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-05 23:06:50 - RECV  | Reply received successfully, rtt = 115ms
2022-11-05 23:06:50 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-05 23:06:50 - RECV  | Reply received successfully, rtt = 70ms
2022-11-05 23:06:50 - SENT  | Message sent to server 127.0.0.1:3000
2022-11-05 23:06:51 - ERROR | Timeout waiting for response, packet was lost
----------------------------------------------------------------------
2022-11-05 23:06:51 - INFO  | Total time = 4.7056 seconds
2022-11-05 23:06:51 - INFO  | 10 packets transmitted, 6 received.
2022-11-05 23:06:51 - INFO  | 40.00% packet loss.
2022-11-05 23:06:51 - INFO  | rtt min/avg/max/mdev = 70.000/117.000/173.000/37.571 ms
----------------------------------------------------------------------
2022-11-05 23:06:51 - END   | Client socket closed
```

**packets_data.csv:**
```
sid_sent,sid_received,type_sent,type_received,timestamp_sent,timestamp_received,message_sent,message_received,rtt
00000,0000,0,0,6560,0000,p,TIMEOUTERROR,None
00001,0000,0,0,7560,0000,dofkrw,TIMEOUTERROR,None
00002,00002,0,1,8561,8734,gcwuubkigyacutawyolpeijd,gcwuubkigyacutawyolpeijd,173.0
00003,00003,0,1,8734,8846,ty,ty,112.0
00004,0000,0,0,8846,0000,vcitufrtxzfgjjxwuyvrmwnqyhstz,TIMEOUTERROR,None
00005,00005,0,1,9847,9992,sgiiudamqqgcjebwpfdljopjlnj,sgiiudamqqgcjebwpfdljopjlnj,145.0
00006,00006,0,1,9992,0079,zegmbchnidqhrbprzhigqfbc,zegmbchnidqhrbprzhigqfbc,87.0
00007,00007,0,1,0079,0194,dfsdlxewcwsttreeqobk,dfsdlxewcwsttreeqobk,115.0
00008,00008,0,1,0194,0264,yxwtkdpmptadohhslcxpiqyaoxfj,yxwtkdpmptadohhslcxpiqyaoxfj,70.0
00009,0000,0,0,0264,0000,fitwyaqoayqmzzooweaecczezgzljv,TIMEOUTERROR,None
```

Note that when a packet is lost the timestamp is **'0000'**, type_received **'0'** and the rtt **None**.
