from Data import Request
from Commands import *
from ReplyCodes import codes


class CommandManager:
    """ Creates and Manages SMTP commands """

    def __init__(self):
        self.__commands = {
            "ehlo": (0, EHLO()),
            "helo": (1, Helo()),
            "mail": (2, Mail()),
            "rcpt": (3, Rcpt()),
            "data": (4, Data()),
            "rset": (5, Rset()),
            "noop": (6, Noop()),
            "quit": (7, Quit())
        }
        self.__last_executed_command_id = None
        self.__command_map = {
            2: (0, 1, 4),
            3: (2,),
            4: (3,)
        }

    def __extract_comand(self, request: str) -> str:
        if not request:
            return None
        request = request.strip().lower()
        splited_request = request.split()
        return splited_request[0]

    def __is_requested_command_valid(self, command_id: int) -> bool:
        if command_id in self.__command_map:
            if self.__last_executed_command_id in self.__command_map[command_id]:
                return True
            else:
                return False
        return True

    def change_last_executed_command_id(self, command_id):
        if command_id == self.__commands.get("ehlo")[0] or command_id == self.__commands.get("rset")[0]:
            self.__last_executed_command_id = self.__commands.get("ehlo")[0]
        elif command_id != self.__commands.get("noop")[0] and command_id != self.__commands.get("quit")[0]:
            self.__last_executed_command_id = command_id

    def get_command(self, request: Request):
        command_req = self.__extract_comand(request.message)
        command_pair = self.__commands.get(command_req, None)
        if command_pair is None:
            return (False, codes.get("UNRECOGNIZED_COMMAND"))
        is_command_valid = self.__is_requested_command_valid(command_pair[0])
        if is_command_valid:
            self.change_last_executed_command_id(command_pair[0])
            return (True, command_pair[1])
        else:
            return (False, codes.get("BAD_COMMAND_SEQUENCE"))
