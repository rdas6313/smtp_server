from abc import ABC, abstractclassmethod
from Data import Request, Message
from Configuration import config
from ReplyCodes import codes


class Command(ABC):
    """ Interface for command """

    @abstractclassmethod
    def handel_request(self, socket, mail: Message, request: Request):
        pass

    def send(self, socket, message):
        socket.sendall(message)


class Helo(Command):
    """Implements Helo command of SMTP protocol"""

    def handel_request(self, socket, mail: Message, request: Request):
        """ Handel Helo command request """
        valid, parameter = self.get_parameter_from_request(request)
        if not valid:
            code, code_msg = parameter
            msg = f"{code} {code_msg}"
        else:
            code, code_msg = codes.get("OK", (None, None))
            msg = f"{code} {config.get("domain", None)}"
            mail.clear()
        self.send(socket, msg)

    def get_parameter_from_request(self, request: Request):
        """ Extracts parameter from request """
        if not request:
            return (False, codes.get("COMMAND_PARAMETER_ERROR", None))
        command_with_parameter = request.message.strip().split()
        if len(command_with_parameter) != 2:
            return (False, codes.get("COMMAND_PARAMETER_ERROR", None))
        return (True, command_with_parameter[1])


class EHLO(Command):
    """Implements Ehlo command of SMTP protocol"""

    def handel_request(self, socket, mail, request):
        pass


class Mail(Command):
    """Implements Mail command of SMTP protocol"""

    def handel_request(self, socket, mail, request):
        pass


class Rcpt(Command):
    """Implements Rcpt to command of SMTP protocol"""

    def handel_request(self, socket, mail, request):
        pass


class Data(Command):
    """Implements Data command of SMTP protocol"""

    def handel_request(self, socket, mail, request):
        pass


class Rset(Command):
    """Implements Rset command of SMTP protocol"""

    def handel_request(self, socket, mail, request):
        pass


class Noop(Command):
    """Implements Noop command of SMTP protocol"""

    def handel_request(self, socket, mail, request):
        pass


class Quit(Command):
    """Implements Quit command of SMTP protocol"""

    def handel_request(self, socket, mail, request):
        pass
