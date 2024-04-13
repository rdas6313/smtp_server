
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
