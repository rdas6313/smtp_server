
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

        request = Request(req_msg)
        helo = Helo()
        should_continue, msg = helo.handel_request(Message(
            sender="", recipients=[], message=""), request)
        assert msg == expected


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

        mail = Mail()
        message = Message("", [], "")
        request = Request(req_msg)
        should_continue, msg = mail.handel_request(message, request)
        assert msg == expected


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

        rcpt = Rcpt()
        message = Message("", [], "")
        request = Request(req_msg)
        should_continue, msg = rcpt.handel_request(message, request)
        assert msg == expected


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
    def test_handel_request_and_data(self, inputs, outputs):
        from Commands import Data
        from Data import Request, Message
        import re
        pattern = "^354.+"
        message = Message("", [], "")
        request = Request(inputs[0])
        data = Data()
        should_continue, msg = data.handel_request(message, request)
        assert msg == outputs[0]
        if not re.search(pattern, msg):
            return

        should_continue, msg = data.handel_data(message, inputs[1])
        assert msg == outputs[1]


class TestQuitCommand:

    @pytest.mark.parametrize("input,output", [('QUIT', '221 BYE!'), ('quit', '221 BYE!'), ('quit to', '501 Command parameter error')])
    def test_quit(self, input, output):
        from Data import Request, Message
        from Commands import Quit

        message = Message("", [], "")
        request = Request(input)
        quit = Quit()
        should_continue, msg = quit.handel_request(message, request)
        assert msg == output
