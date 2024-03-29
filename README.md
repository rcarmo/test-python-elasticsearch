# Elasticsearch Python Client Profiling

This is a test repository that allows me to compare the official Elasticsearch client and a minimalist `asyncio` client.

## Purpose

The idea is to map out code structure and identify possible bottlenecks by profiling some REST API operations (starting with `GET /_nodes/_all`), and figure out how an `asyncio`/`aiohttp` implementation might differ.

The `aioelastic` folder contains a shim client based on my [`aioazstorage`](https://github.com/rcarmo/aioazstorage) wrappers that does the bare minimum required to talk to the server but tries to a) parse replies as fast as possible (using `ujson`) and provide a fully async interface (through an async generator for enumerating nodes).

## Usage

Both folders (`official-client` and `aioelastic`) have a `Makefile` to provision (`make deps`), test (`make test`) and generate PNG profiles (`make profile`) after running 10K API calls.

## Dependency Graphs

These were generated on an i5 iMac with Python 3.7.4 (installed via `brew` and `pyenv`) against the official Elasticsearch Docker container, running a single node.

### `official-client`

Besides using `feedparser` (which is interesting) the official client spends most of its time inside `recv_into`:

![](official-client/elastic.png)

### `aioelastic`

`aioelastic` does some date formatting and `uuid` generation upon every request (which I find invaluable for tracing requests), but otherwise spends most of its time inside `select.kqueue` (since I'm using `uvloop`):

![](aioelastic/aioelastic.png)
