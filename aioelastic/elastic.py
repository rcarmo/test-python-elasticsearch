from aiohttp import ClientSession
from asyncio import sleep
from base64 import b64encode, b64decode
from datetime import datetime
from email.utils import formatdate
from hashlib import sha256, md5
from hmac import HMAC
from time import time, mktime
from urllib.parse import urlencode, quote_plus, quote
from uuid import uuid1, UUID
try:
    from ujson import dumps, loads
except ImportError:
    from json import dumps, loads

class Client:
    server = None
    port = None
    auth = None
    session = None

    def __init__(self, server="localhost", port=9200, auth=None, session=None):
        """Create a Client instance"""

        self.server = server
        self.port = port
        if session is None:
            session = ClientSession(json_serialize=dumps)
        self.session = session

    async def close(self):
        await self.session.close()

    def _headers(self, date=None):
        """Default headers for REST requests"""

        if not date:
            date = formatdate(usegmt=True) # if you don't use GMT, the API breaks
        return {
            'Accept': 'application/json', 
            'x-client-request-date': date,
            'x-client-request-id': str(uuid1()), #  useful for debugging
            'Connection': 'Keep-Alive'
        }

    async def getNodes(self, query={}):
        """Enumerate all nodes (includes plugins, internal parameters, etc.)"""

        canon = '/_nodes/_all'
        uri = 'http://{}:{}{}'.format(self.server, self.port, canon)
        async with self.session.get(uri, headers=self._headers()) as resp:
            if resp.status == 200:
                for key, item in (await resp.json(loads=loads))['nodes'].items():
                    yield item
            else:
                return


    async def createTable(self, name):
        """Create a new table"""
        canon = '/{}/Tables'.format(self.server)
        uri = 'https://{}.table.core.windows.net/Tables'.format(self.server)
        payload = dumps({"TableName": name})
        return await self.session.post(uri, headers=self._sign_for_tables(canon, payload), data=payload)
