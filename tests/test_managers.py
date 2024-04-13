
import sys
import pytest
sys.path.append('/Users/rajadas/Documents/projects/smtp_server')


class TestManagers:

    def make_manager(self):
        from Managers import CommandManager
        return CommandManager()

    @pytest.fixture(scope="function")
    def manager_func(self):
        print("Function manager")
        return self.make_manager()

    @pytest.fixture(scope="module")
    def manager_module(self):
        print("Module manager")
        return self.make_manager()

    @pytest.mark.parametrize("command,expected", [
        ("MAIL FROM: <rdas6313@gmail.com>", "mail"),
        ("Data", "data"),
        ("RCPT to: <abc@gmail.com>", "rcpt"),
        ("", None)
    ])
    def test_extract_command(self, manager_func, command, expected):
        cm = manager_func._CommandManager__extract_comand(command)
        assert cm == expected

    @pytest.mark.parametrize("last_id,command_id,expected", [
        (None, 0, True),
        (None, 2, False),
        (0, 2, True),
        (0, 3, False),
        (4, 2, True)

    ])
    def test_valid_command(self, manager_func, last_id, command_id, expected):
        manager_func._CommandManager__last_executed_command_id = last_id
        assert manager_func._CommandManager__is_requested_command_valid(
            command_id) == expected

    @pytest.mark.parametrize("req_command,expected", [
        ("EHLO", True), ("MAIL FROM: <rdas@ex.com>", False)
    ])
    def test_get_command(self, req_command, expected, manager_func):
        from Data import Request
        req = Request(req_command)
        res = manager_func.get_command(req)
        assert res[0] == expected

    @pytest.mark.parametrize("datalist", [
        (("EHLO", True), ("MAIL FROM: <rdas@ex.com>", True),
         ("RCPT TO: <abc@ex.com>", True), ("DATA", True)),
        (("MAIL FROM: <abc>", False), ("RSET", True)),
        (("RSET", True), ("NOOP", True)),
        (("EHLO", True), ("NOOP", True), ("MAIL FROM: <rdas@ex.com>", True), ("RSET", True),
         ("RCPT TO: <abc@ex.com>", False)),
        (("HELO", True), ("MAIL", True), ("RSET", True),
         ("MAIL", True), ("RCPT", True), ("DATA", True)),
        (("NOOP", True), ("HELO", True), ("MAIL", True), ("RSET", True),
         ("RCPT", False), ("DATA", False))
    ])
    def test_get_command_combined(self, datalist, manager_func):
        from Data import Request
        for data in datalist:
            req = Request(data[0])
            res = manager_func.get_command(req)
            print(res)
            assert res[0] == data[1]
