# Tornado with zmq sample project

This is my spare time "how-to-use xx?" project.
To get used to tornado5 with async background job. 

## prerequisite
- pip install tornado > 5.0
- pip install pyzmq

## Files
- wsserver.py
-- Web Application. Simple websocket (tornado ioloop)
- rate.py
-- Background Application. generate dummy FX rate per second. Using pyzmq pub/sub.
- getrate.py
-- ZMQ subscriber sample (pure asyncio)

## Run
- run wsserver.py
- run rate.py
- open browser http://localhost:8080


