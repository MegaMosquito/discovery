# LAN Discovery Utility
  
This utility enables basic service discovery on a LAN. Each node running this container listens on a particular UDP port, and also *broadcasts* information about itself onto that UDP port. All nodes running this container maintain a JSON array containing all of the data received from responding nodes.  This JSON array is made available locally via a simple REST API. The UDP port used is 5959 by default. The REST API is presented on port 5960 by default. Both of these port numbers are user-configurable, but of course they must be well known to other participants.

## UDP Is Unreliable, But That's Okay

All nodes on the LAN running this container will be competing to send data onto this UDP port. Also, UDP datagrams are inherently unreliable. So the broadcasting thread on each node continuously repeats its data on a slightly randomized schedule (details of that are configurable).

## Exactly What Data Is Broadcast

The exact data that is broadcast by each node is just a user-defined string. By defaukt, this string can contain up to 1023 characters (but that is configurable). In the examples shown in the next section it is a raw string, but it could be a string containingg JSON, XML, or yaml, if you prefer.

## REST API

The REST API responds to requests at URL path "/v1/discovered" and returns a JSON structure similar to the one shown below:

```
{
  "version": "1.0",
  "udp_port": 5959,
  "discovered": [
    { "ipv4": "10.0.0.106", "data": "iperf3 server" },
    { "ipv4": "10.0.0.23", "data": "iperf3 server" },
    { "ipv4": "10.0.0.17", "data": "cam streamer" }
  ]
}
```

It returns the current version of the discovery utility (could be different from the "/v1/" in the URL). It also shares the port number it used for discovery. Then it returns a lost of the nodes it discovered. There will be one entry in the list for each address that has responded so far (at the moment the REST API was invoked). Each entry will contain the respondent's IPv4 address, and whatever data string was provided within the UDP datagram.

For example, you could test the REST API server with a command like this:

```
curl -s localhost:5960/v1/discovered | jq
```

