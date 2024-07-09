"""API module. Contains reusable functions/methods for the client application.
"""

import asyncio
import getpass
import ipaddress
import json
import netifaces
import sys
import time


class NetInfo:
    """Network information on which the client runs.
    """

    def __init__(self, *args, **kwargs):
        """Initialize self. See help(type(self)) for accurate signature.

        """

    def get_netinfo(self, interface='wlan0'):
        """Gets network information for a given interface of a device.

        Args:
            interface (str): (optional) a valid interface.

        Return:
            return a tuple containing the interface, the local ip address, and
            the prefix length.
        """

        try:
            # get the addresses for the specified interface
            addrs = netifaces.ifaddresses(interface)

            # get the IPv4 address information
            ipv4_info = addrs[netifaces.AF_INET][0]

            ipaddr = ipv4_info['addr']
            netmask = ipv4_info['netmask']

            # calculate the prefix length from netmask
            prefixlen = sum([bin(int(i)).count('1') for i in netmask.split('.')])

            return interface, ipaddr, prefixlen

        except (ValueError, KeyError, IndexError):
            return interface, None, None


    def get_hosts(self):
        """Get a list of active hosts within a network range.

        Return:
            return a list of ip addresses.
        """

        _, ipaddr, prefixlen = self.get_netinfo()

        if ipaddr and prefixlen:
            subnet = ipaddr.rsplit('.', 1)[0]
            subnet = subnet + '.' + '0'
            subnet = subnet + '/' + str(prefixlen)

            network = ipaddress.IPv4Network(subnet)
            hosts = list(network.hosts())
            flag = True
        else:
            hosts = []
            flag = False

        return flag, hosts


class Protocol(NetInfo):
    """MagNet Protocols for the client side.
    """

    def __init__(self, *args, **kwargs):
        """Initialize self. See help(type(self)) for accurate signature.
        """

        super().__init__(args, kwargs)

        # the current server/host being accessed
        self.port = 2024
        self.hostname = None
        self.host = {'name': None, 'io': (None, None), 'addr': None, 'port': 2024}

        self.hostnames = [self.hostname]
        self.hosts = [self.host]

        self.status = (None, None)  # status handler for requests and response

    def content_types(self):
        images = ['jpeg', 'png', 'gif', 'svg+xml', 'bmp', 'tiff', 'ico',
                  'x-icon', 'x-xbitmap', 'x-xpixmap']
        audios = ['mpeg', 'mp4', 'ogg', 'wav', 'aac', 'midi', 'webm', 'x-aac',
                  'x-mpegurl', 'x-realaudio']
        videos = ['mp4', 'ogg', 'webm', 'mpeg', 'quicktime', 'x-flv',
                  'avi', 'x-matroska']
        apps = ['json', 'xml', 'pdf', 'zip', 'x-gzip', '-xtar',
                'x-www-form-urlencoded', 'x-shockwave-flash', 'excel',
                'powerpoint', 'word', 'x-7z-compressed', 'vnd.api+json',
                'x-html+ul', 'x-protobuf', 'x-bzip2', 'x-xml-dtd', 'x-xml-xsl']
        multipart = ['form-data', 'mixed', 'alternative', 'related']

        all = {'image': images, 'audio': audios, 'video': videos,
               'application': apps, 'multipart': multipart}

        return all

    async def send(self, writer, message):
        if writer:
            try:
                writer.write(message.encode())
                await writer.drain()

                return (200, 'OK')
            except (ConnectionResetError, OSError):
                return 503, 'Bad Gateway'

        return 503, 'Bad Gateway'

    async def recv(reader):
        """Get response/message from server.

        Args:
            reader (obj): a StreamReader object to read data from.

        Return:
            return the received data in decoded form on success.
            return None on failure.
        """

        if reader:
            data = await reader.read(1024)

            return data.decode()

        return None

    async def connect(self, reader, writer, host, port, route, hostname=''):
        addr = header.get('host').split(':')
        host = addr[0]
        port = addr[1]

        hostname = header.get('hostname')
        route = header.get('route')

        try:
            reader, writer = await asyncio.open_connection(host, port)

            # check headers for validation (user agent? right source?...)
            status = await self.send_request(reader, writer, host, port,
                                             'HEAD', '/', hostname)
        except ConnectionRefusedError:
            status = (404, 'Bad Gateway')   # TODO

        return status

    async def head(self, reader, writer, header):
        request = json.dumps(header)
        status = await self.send(writer, request)
        if status != (200, 'OK'):
            return status

        response = await self.recv(reader)
        if not response:
            status = (404, 'Bad Gateway')
        else:
            response = json.loads(response)
            try:
                status = response.get('status')
                if status != (200, 'OK'):
                    return status

                hostname = response.get('hostname')
                addr = response.get('host')
                port = response.get('port')

                host = {'name': hostname, 'io': (reader, writer),
                        'addr': addr, 'port': port}


                if self.hostnames and self.hosts:
                    if hostname in self.hostnames:
                        length = len(self.hosts)
                        for i in range(length):
                            if self.hosts[i].get('name') == hostname:
                                self.hosts[i] = host

                                return (200, 'OK')

                self.hostnames += [hostname]
                self.hosts += [host]
                status = (200, 'OK')

            except (KeyError):
                status = (404, 'Bad Gateway')

        return status

    async def get(self, reader, writer, header):
        route = header.get('route')
        request = json.dumps(route).encode()
        status = await self.send(writer, request)
        if status != (200, 'OK'):
            return status

        response = await self.recv(reader)
        if not response:
            status = 503, 'Bad Gateway'
        else:
            response = json.loads(response)
            try:
                content = response.get('content')
                cotent_type = response.get('content-type')
                content_length = response.get('content-length')

                status = response.get('status')
            except (KeyError):
                status = 503, 'Bad Gateway'

        # do something with the response if all good

        return status

    async def send_request(self, reader, writer, host, port, method, route,
                   hostname, user_agent='magnet/0.0'):
        """Sends a HEAD request to host.

        Args:
            reader (stream): a StreamReader object to read response.
            writer (stream): a StreamWriter object to send requests.
            host (str): local ip address of host.
            port (str): port on which the host is binded to.
            method (str): the kind request to send (GET, HEAD, POST, PUT).
            request (obj): can be any object type, the content of request to make.
            hostname (str): (optional) the human friendly name used to identify
                            the host/
            route (str): (optional) location of data on server, tells the host
                         where to look for the data.
            proto (str): (optional) protocol factory.
            user_agent (str): (optional) the user agent used to make the
                              request.

        Return:
            return the a tuple object contaning status_code and status_string
        """

        print(route)
        accept_ranges = '*/*'   # TODO to be determined by the data type
        addr = f'{host}:{port}'
        date = time.strftime('%a, %d %b %Y %H:%M:%S %z')

        header = {
                  'method': method,
                  'route': route,
                  'host': addr,
                  'hostname': hostname,
                  'user-agent': user_agent,
                  'accept-ranges': accept_ranges,
                  'content': None,  # to be set by POST and PUT methods
                  'content-length': None,   # to be set by POST and PUT methods
                  'content-type': None,   # to be set by POST and PUT methods
                  'date': date,
                 }

        if method == 'CONNECT':
            status = await self.connect(reader, writer, host, port, route,
                                        hostname)

            return status

        else:
            if writer:
                if method == 'HEAD':
                    status = await self.head(reader, writer, header)

                elif method == 'GET':
                    status = await self.get(reader, writer, header)
                else:
                    status = 503, 'Bad Gateway'

        return status

    async def get_active_hosts(self, hosts=None, start=0, stop=256):
        flag = True
        if hosts is None:
            flag, hosts = self.get_hosts()
        if flag is False:
            self.hostnames = []
            self.hosts = []

            return (flag, self.hostnames, self.hosts)

        tasks = []
        length = len(hosts)
        port = self.port
        hostname = None

        for i in range(start, length):
            if i == stop:
                # get the remaining indices left
                await self.get_active_hosts(hosts, i, stop * 2)

                break

            reader, writer = None, None
            tasks += [self.send_request(reader, writer, hosts[i], port, 'HEAD',
                                        '/', hostname)]
            await asyncio.gather(*tasks)

        return (flag, self.hostnames, self.hosts)


class Auth(Protocol):
    """Handles account creation, authentications, etc, for the client side.
    """

    def __init__(self, *args, **kwargs):
        """Initialize self. See help(type(self)) for accurate signature.
        """

        super().__init__(args, kwargs)

    def create_client(self):
        """Set up a new client account.
        """

        self.stdout.write("    Setup a new Client...\n")
        self.stdout.write("=============================\n\n")

        msg = "Magnetism needs some data about the new Client\n"
        self.stdout.write(msg)
        self.stdout.write("(You can always change this data anytime)...\n\n")

        self.stdout.write("Enter a Display Name for the new Client: ")

        self.stdout.flush()

        try:
            dname = self.stdin.readline()
        except EOFError:
            pass

        self.stdout.write("\nEnter a Password for the new Client...\n")
        self.stdout.flush()

        try:
            passwd = getpass.getpass('(You can leave this field empty): ')
        except EOFError:
            self.stdout.write('\n')
            self.stdout.flush()
            pass
