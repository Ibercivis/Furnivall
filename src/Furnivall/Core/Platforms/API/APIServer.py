#!/usr/bin/env python
"""
    Furnivall API export server

"""

import asyncore
import collections
import logging
import socket


MAX_MESSAGE_LENGTH = 1024


class OpenedClient(asyncore.dispatcher):

     """Wraps a remote client socket."""

    def __init__(self, host, socket, address):
        asyncore.dispatcher.__init__(self, socket)
        self.host, self.outbox = host, collections.deque()

    def say(self, message):
        self.outbox.append(message)

    def handle_read(self):
        client_message = self.recv(MAX_MESSAGE_LENGTH)

    def handle_write(self):
        if not self.outbox: return
        message = self.outbox.popleft()
        self.send(message)


class AsyncServer(asyncore.dispatcher):

    """
        Implements a asyncronous TCP server to be used in furnivall api server
    """

    def __init__(self, address=('localhost', 0)):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.listen(1)
        self.remote_clients = []

    def handle_accept(self):
        socket, addr = self.accept() # For the remote client.
        self.remote_clients.append(RemoteClient(self, socket, addr))



class FurnivallApiServer(AsyncServer):
    """
        Implements the main API Server, based on a basic TCP server.
    """

    def handle_read(self):
        # Call the API methods
        self.read()
