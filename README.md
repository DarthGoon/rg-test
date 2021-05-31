# rg-test-api
This is a sha256 hashing service for messages.  You can use this service to get a hash of a specific message, and subsequently use the hash to retrieve the original message.

### Usage
```
> curl -get http://34.73.16.103:5000/hash?msg=ThisIsTheWay
3a51322508caf567cf4147de234974cf70cee6cf65711d36a2030df4291b29e3

> curl -get http://34.73.16.103:5000/message?hash=3a51322508caf567cf4147de234974cf70cee6cf65711d36a2030df4291b29e3
ThisIsTheWay
```
## Architecture
This service is a containerized RESTful [Python 3.9](https://docs.python.org/3.9/) API, which leverages a hash library, and key/value to save corresponding messages and hashes.
 - [How does the API work?](https://github.com/DarthGoon/rg-test/blob/master/app/server.py)
 - [How does hashing work?](https://github.com/DarthGoon/rg-test/blob/master/app/hp.py)

The rg-test-api containers runs on a [GKE Autopilot cluster](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview); which contacts a gCloud instance of [MemoryStore for Redis](https://cloud.google.com/memorystore/docs/redis/redis-overview).
```
                         ┌───────┐
┌──────────────┐         │       │         ┌──────────┐
│              ├────────-│  API  ├────────-│          │
│              │         └───────┘         │          │
│   Load       │                           │          │
│    Balancer  │                           │  Store   │
│              │         ┌───────┐         │          │
│              ├────────-│       ├────────-│          │
└──────────────┘         │  API  │         └──────────┘
                         └───────┘
```
## Development
The rg-test-api uses docker for its local development environment.  Docker will provide a local instance of redis for storage; a version specific Python runtime; and a mirrored file system during development.
### Creating dev environment
1. Install [Docker](https://docs.docker.com/get-docker/)
2. `git clone git@github.com:DarthGoon/rg-test.git && cd rg-test/`
3. `make run`
### Testing
Test files are found alongside their units in the directory structure.
(ex. `hp.py` and [hp.test.py](https://github.com/DarthGoon/rg-test/blob/master/app/hp.test.pk))
Test files run inside the container environment, by executing-
`make test`
