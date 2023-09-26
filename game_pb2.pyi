from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class wasHit(_message.Message):
    __slots__ = ["soldierID", "trueFlag"]
    SOLDIERID_FIELD_NUMBER: _ClassVar[int]
    TRUEFLAG_FIELD_NUMBER: _ClassVar[int]
    soldierID: int
    trueFlag: bool
    def __init__(self, soldierID: _Optional[int] = ..., trueFlag: bool = ...) -> None: ...

class Soldier(_message.Message):
    __slots__ = ["x", "y", "speed"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    speed: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., speed: _Optional[int] = ...) -> None: ...

class InitialValues(_message.Message):
    __slots__ = ["commander_id", "N", "M", "T", "S"]
    COMMANDER_ID_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    M_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    commander_id: int
    N: int
    M: int
    T: int
    S: int
    def __init__(self, commander_id: _Optional[int] = ..., N: _Optional[int] = ..., M: _Optional[int] = ..., T: _Optional[int] = ..., S: _Optional[int] = ...) -> None: ...

class Update(_message.Message):
    __slots__ = ["alive", "x", "y", "message", "soldierID"]
    ALIVE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SOLDIERID_FIELD_NUMBER: _ClassVar[int]
    alive: bool
    x: int
    y: int
    message: str
    soldierID: int
    def __init__(self, alive: bool = ..., x: _Optional[int] = ..., y: _Optional[int] = ..., message: _Optional[str] = ..., soldierID: _Optional[int] = ...) -> None: ...

class Missile(_message.Message):
    __slots__ = ["x", "y", "rad"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    RAD_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    rad: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., rad: _Optional[int] = ...) -> None: ...

class ServerOutput(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class Commander_alive_response(_message.Message):
    __slots__ = ["commanderId", "time", "all_dead"]
    COMMANDERID_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    ALL_DEAD_FIELD_NUMBER: _ClassVar[int]
    commanderId: int
    time: int
    all_dead: bool
    def __init__(self, commanderId: _Optional[int] = ..., time: _Optional[int] = ..., all_dead: bool = ...) -> None: ...
