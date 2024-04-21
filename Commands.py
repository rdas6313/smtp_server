from abc import ABC, abstractclassmethod
from Data import Request, Message
from Configuration import config
from ReplyCodes import codes
import re


class Command(ABC):
    """ Interface for command """

    @abstractclassmethod
    def handel_request(self, socket, mail: Message, request: Request):
        pass

    def send(self, socket, message):
        socket.sendall(message)

    def read(self, socket, eof):
        content = socket.read()
        return content


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
        valid, msg = self.is_valid_syntax(request)
        if not valid:
            print(msg[1])
            output = f"{msg[0]} {msg[1]}"
            self.send(socket, output)
            return
        sender = self.get_parameter(request)
        mail.sender = sender
        output = f"{codes.get("OK", ("", ""))[0]} {
            codes.get("OK", ("", ""))[1]}"
        self.send(socket, output)

    def is_valid_syntax(self, request: Request):
        if not request:
            return (False, codes.get("COMMAND_PARAMETER_ERROR", None))
        word = request.message.lower().strip().split(' ')
        if (len(word) != 2):
            return (False, codes.get("COMMAND_PARAMETER_ERROR", None))
        from_word = word[1].split(':')
        # print(from_word)
        # pattern = "^<.+@.+\.[a-zA-Z]+>$"
        pattern = "^<[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+>$"
        if len(from_word) != 2 or from_word[0] != "from" or not re.search(pattern, from_word[1]):
            return (False, codes.get("COMMAND_PARAMETER_ERROR", None))
        return (True, '')

    def get_parameter(self, request: Request):
        word = request.message.lower().strip().split(' ')
        parameter: str = word[1].split(':')[1]
        parameter = parameter.lstrip('<').rstrip('>')
        return parameter


class Rcpt(Command):
    """Implements Rcpt to command of SMTP protocol"""

    def handel_request(self, socket, mail, request):
        valid, msg = self.is_valid_syntax(request)
        if not valid:
            output = f"{msg[0]} {msg[1]}"
            self.send(socket, output)
            return False
        receiver = self.get_parameter(request)
        mail.recipients.append(receiver)
        output = f"{codes.get("OK", ("", ""))[0]} {
            codes.get("OK", ("", ""))[1]}"
        self.send(socket, output)
        return False

    def is_valid_syntax(self, request: Request):
        if not request:
            return (False, codes.get("COMMAND_PARAMETER_ERROR", None))
        word = request.message.lower().strip().split(' ')
        if (len(word) != 2):
            return (False, codes.get("COMMAND_PARAMETER_ERROR", None))
        from_word = word[1].split(':')
        # pattern = "^<.+@.+\.[a-zA-Z]+>$"
        pattern = "^<[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+>$"
        if len(from_word) != 2 or from_word[0] != "to" or not re.search(pattern, from_word[1]):
            return (False, codes.get("COMMAND_PARAMETER_ERROR", None))
        return (True, '')

    def get_parameter(self, request: Request):
        word = request.message.lower().strip().split(' ')
        parameter: str = word[1].split(':')[1]
        parameter = parameter.lstrip('<').rstrip('>')
        return parameter


class Data(Command):
    """Implements Data command of SMTP protocol"""

    def handel_request(self, socket, mail, request):
        valid, msg = self.is_valid_syntax(request)
        if not valid:
            output = f"{msg[0]} {msg[1]}"
            self.send(socket, output)
            return False
        code, msg = codes.get("SEND_MAIL_CONTENT", (0, ""))
        output = f"{code} {msg}"
        self.send(socket, output)
        eof = '.'
        content = self.read(socket, eof)
        mail.message = content
        code, msg = codes.get("OK", (0, ""))
        output = f"{code} {msg}"
        self.send(socket, output)
        return False

    def is_valid_syntax(self, request: Request):
        if not request or request.message.strip().lower() != "data":
            return (False, codes.get("COMMAND_PARAMETER_ERROR", None))
        return (True, '')


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
