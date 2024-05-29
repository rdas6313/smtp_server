from .Data import Message
from .Managers import CommandManager


class SMTP:
    """ Creates SMTP server and runs it """

    def __init__(self, socket):
        if socket is None:
            raise AttributeError("Socket is required")
        self.message = Message()
        self.command_manager = CommandManager()
        self.socket = socket

    def start(self):
        pass
