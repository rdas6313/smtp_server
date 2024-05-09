
import sys
import pytest
sys.path.append('/Users/rajadas/Documents/projects/smtp_server')

# to see printed output in pytest use -rP


class TestHeloCommand:
    @pytest.mark.parametrize("req_msg,expected",
                             [("Helo abc.com", True), ("helo ax.com", True),
                              ("helo ax com", False), ("Helo", False)])
    def test_get_parameter(self, req_msg, expected):
        from Data import Request
        from Commands import Helo
        request = Request(req_msg)
        helo = Helo()
        valid, parameter = helo.get_parameter_from_request(request)
        print(parameter)
        assert valid == expected

    @pytest.mark.parametrize("req_msg,expected", [("Helo abc.com", "250 domain.com"),
                                                  ("Helo", "501 Command parameter error"),
                                                  ("helo abc.com aw.com",
                                                   "501 Command parameter error"),
                                                  ("heLo abc.com", "250 domain.com")])
    def test_handel_request(self, req_msg, expected):
        from Data import Request, Message
        from Commands import Helo

        class Socket:
            def sendall(self, msg):
                assert msg == expected

        socket = Socket()
        request = Request(req_msg)
        helo = Helo()
        helo.handel_request(socket, Message(
            sender="", recipients=[], message=""), request)


class TestMailCommand:

    @pytest.mark.parametrize("req_msg, expected", [("MAIL FROM:<abc@ex.com>", True),
                                                   ("mail from:<abc@ex.com>", True),
                                                   ("mail:<abc@ex.com>", False),
                                                   ("mail from:", False),
                                                   ("mail from:abc@ex.com", False),
                                                   ("mail:", False),
                                                   ("mail:abc.com", False)])
    def test_is_valid_syntax(self, req_msg, expected):
        from Commands import Mail
        from Data import Request
        request = Request(req_msg)
        mail = Mail()
        assert mail.is_valid_syntax(request)[0] == expected

    @pytest.mark.parametrize("req_msg,expected", [("Mail from:<abc@gmail.com>", "abc@gmail.com"),
                                                  ("MAIL FROM:<abc@gmail.com>", "abc@gmail.com")])
    def test_get_parameter(self, req_msg, expected):
        from Commands import Mail
        from Data import Request
        request = Request(req_msg)
        mail = Mail()
        assert mail.get_parameter(request) == expected

    @pytest.mark.parametrize("req_msg,expected", [("MAIL FROM:<abc@ex.com>", "250 Ok"),
                                                  ("MAIL FROM:<abcex.com>",
                                                   "501 Command parameter error"),
                                                  ("MAIL FROM:<abc@ex.com>",
                                                   "250 Ok"),
                                                  ("mail from:<abc@ex.com>",
                                                   "250 Ok"),
                                                  ("mail:<abc@ex.com>",
                                                   "501 Command parameter error"),
                                                  ("mail from:",
                                                   "501 Command parameter error"),
                                                  ("mail from:abc@ex.com",
                                                   "501 Command parameter error"),
                                                  ("mail:", "501 Command parameter error"),
                                                  ("mail:abc.com", "501 Command parameter error")])
    def test_handel_request(self, req_msg, expected):
        from Data import Request, Message
        from Commands import Mail

        class Socket:
            def sendall(self, msg):
                assert msg == expected

        socket = Socket()
        mail = Mail()
        message = Message("", [], "")
        request = Request(req_msg)
        mail.handel_request(socket, message, request)


class TestRcptCommand:

    @pytest.mark.parametrize("req_msg, expected", [("RCPT TO:<abc@ex.com>", True),
                                                   ("rcpt to:<abc@ex.com>", True),
                                                   ("rcpt:<abc@ex.com>", False),
                                                   ("rcpt to:", False),
                                                   ("rcpt to:abc@ex.com", False),
                                                   ("rcpt:", False),
                                                   ("rcpt:abc.com", False)])
    def test_is_valid_syntax(self, req_msg, expected):
        from Commands import Rcpt
        from Data import Request
        request = Request(req_msg)
        rcpt = Rcpt()
        assert rcpt.is_valid_syntax(request)[0] == expected

    @pytest.mark.parametrize("req_msg,expected", [("RCPT TO:<abc@gmail.com>", "abc@gmail.com"),
                                                  ("rcpt to:<abc@gmail.com>", "abc@gmail.com")])
    def test_get_parameter(self, req_msg, expected):
        from Commands import Rcpt
        from Data import Request
        request = Request(req_msg)
        rcpt = Rcpt()
        assert rcpt.get_parameter(request) == expected

    @pytest.mark.parametrize("req_msg,expected", [("RCPT TO:<abc@ex.com>", "250 Ok"),
                                                  ("RCPT TO:<abcex.com>",
                                                   "501 Command parameter error"),
                                                  ("rcpt tO:<abc@ex.com>",
                                                   "250 Ok"),
                                                  ("rcpt to:<abc@ex.com>",
                                                   "250 Ok"),
                                                  ("rcpt:<abc@ex.com>",
                                                   "501 Command parameter error"),
                                                  ("rcpt to:",
                                                   "501 Command parameter error"),
                                                  ("rcpt to:abc@ex.com",
                                                   "501 Command parameter error"),
                                                  ("rcpt:", "501 Command parameter error"),
                                                  ("rcpt:abc.com", "501 Command parameter error")])
    def test_handel_request(self, req_msg, expected):
        from Data import Request, Message
        from Commands import Rcpt

        class Socket:
            def sendall(self, msg):
                assert msg == expected

        socket = Socket()
        rcpt = Rcpt()
        message = Message("", [], "")
        request = Request(req_msg)
        rcpt.handel_request(socket, message, request)


class TestDataCommand:

    @pytest.mark.parametrize("req_msg,expected", [("DATA", True), ("data", True), ("data a", False)])
    def test_is_valid_syntax(self, req_msg, expected):
        from Commands import Data
        from Data import Request
        request = Request(req_msg)
        data = Data()
        assert data.is_valid_syntax(request)[0] == expected

    @pytest.mark.parametrize("inputs,outputs", [(["data", "Content"], ["354 Send message content.End with <CRLF>.<CRLF>", "250 Ok"]),
                                                (["data to", "Content"], [
                                                 "501 Command parameter error"]),
                                                (["  data ", "Content"], ["354 Send message content.End with <CRLF>.<CRLF>", "250 Ok"])])
    def test_handel_request(self, inputs, outputs):
        from Commands import Data
        from Data import Request, Message

        class Socket:
            def __init__(self) -> None:
                self.index = 0

            def sendall(self, msg):
                assert msg == outputs[self.index]
                self.index += 1

            def read(self):
                return inputs[1]

        message = Message("", [], "")
        socket = Socket()
        request = Request(inputs[0])
        data = Data()
        data.handel_request(socket, message, request)


class TestQuitCommand:

    @pytest.mark.parametrize("input,output", [('QUIT', '221 BYE!'), ('quit', '221 BYE!'), ('quit to', '501 Command parameter error')])
    def test_quit(self, input, output):
        from Data import Request, Message
        from Commands import Quit

        class Socket:
            def sendall(self, msg):
                assert msg == output

        message = Message("", [], "")
        socket = Socket()
        request = Request(input)
        quit = Quit()
        quit.handel_request(socket, message, request)
