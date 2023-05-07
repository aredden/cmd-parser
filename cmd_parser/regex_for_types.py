import enum
import re
from typing import Any, Dict, List, Tuple, Union


class CmdType(enum.Enum):
    INT = enum.auto()
    STR = enum.auto()
    FLOAT = enum.auto()
    BOOL = enum.auto()

class RegexCommandType(object):
    def __init__(self, command_flag: str):
        self.command_flag = command_flag

    def parse(
        self, prompt: str, args_dict: Dict[Union[str, int], Any], default
    ) -> Tuple[str, Dict[Union[str, int], Any]]:
        """Replaces the longest match of self.regex in prompt with args passed to self.cast"""
        
        matches = self.regex_str.search(prompt)
        if matches:
            value = matches.group("args")
            args_dict[self.dest] = self.cast(value)
            span = matches.span()
            if prompt[span[-1] - 1] == "-":
                prompt = prompt[: span[0]] + prompt[span[1] - 2 :]
            else:
                prompt = prompt[: span[0]] + prompt[span[1] :]
        else:
            args_dict[self.dest] = default() if callable(default) else default
        return prompt, args_dict


class RegInt(RegexCommandType):
    def __init__(self, command_flag: str, dest: str = None, default=None):
        super().__init__(command_flag)
        self.regex_str = re.compile(
            r" -{1,2}" + re.escape(command_flag) + r" +(?P<args>[0-9]+)(?: -|$)"
        )
        self.regex_text = [command_flag]
        self.dest = dest if dest is not None else command_flag
        self.cast = int
        self.default = default 


class RegFloat(RegexCommandType):
    def __init__(self, command_flag: str, dest: str = None, default=None):
        super().__init__(command_flag)
        self.regex_str = re.compile(
            r" -{1,2}"
            + re.escape(command_flag)
            + r" +(?P<args>\d+(?:\.\d)?(?:e-?\d+)?)(?: -|$)"
        )
        self.regex_text = [command_flag]
        self.dest = dest if dest is not None else command_flag
        self.cast = float
        self.default = default


class RegStr(RegexCommandType):
    def __init__(self, command_flag: str, dest: str = None, default=None):
        super().__init__(command_flag)
        self.regex_str = re.compile(
            r" -{1,2}"
            + re.escape(command_flag)
            + r" +(?P<args>([^- ]+-{0,2}[^- ]{0,} {0,2})+)(?: -|$)"
        )
        self.regex_text = [command_flag]
        self.dest = dest if dest is not None else command_flag
        self.cast = str
        self.default = default

class RegexBool(RegexCommandType):
    def __init__(self, command_flag: str, dest: str = None, default=False):
        super().__init__(command_flag)
        self.regex_str = re.compile(r" -{1,2}" + re.escape(command_flag) + r"(?P<args>)(?: -|$)")
        self.regex_text = [command_flag]
        self.dest = dest if dest is not None else command_flag
        self.default = False if default is None else not default # True for default of False, False for default of True
        self.cast = lambda x: not self.default

class CommandParser:
    cmdtypes: CmdType = CmdType

    def __init__(self, remaining_text_dest: str = "prompt", commands=None):
        self.commands: List[RegexCommandType] = [] if commands is None else commands
        self.remaining_text_destination = remaining_text_dest
        for command in self.commands:
            assert isinstance(
                command, RegexCommandType
            ), f"command {command} is not a valid instance of RegexCommandType. You may be using the incorrect class to define your command arg."

    def parse(self, message: str) -> Tuple[Dict[str, Any], str]:
        args_dict = {}
        prompt = message
        for command in self.commands:
            prompt, args_dict = command.parse(prompt, args_dict, command.default)
        if self.remaining_text_destination:
            args_dict[self.remaining_text_destination] = prompt
        return args_dict

    def add_command(self, name: str, cmd_type: CmdType, destination: str = None, default=None, default_factory=None):
        if cmd_type == self.cmdtypes.INT:
            self.commands.append(RegInt(name, destination, default=default))
        elif cmd_type == self.cmdtypes.FLOAT:
            self.commands.append(RegFloat(name, destination, default=default))
        elif cmd_type == self.cmdtypes.STR:
            self.commands.append(RegStr(name, destination, default=default))
        elif cmd_type == self.cmdtypes.BOOL:
            self.commands.append(RegexBool(name, destination, default=default))
        else:
            raise NotImplementedError(
                "Have not implemented for command type " + str(cmd_type)
            )
        return self

    def add_command_from_instance(self, command: RegexCommandType):
        self.commands.append(command)
        return self
