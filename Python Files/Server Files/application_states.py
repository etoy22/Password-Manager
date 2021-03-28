import enum


class ApplicationStates(enum.Enum):
    """
    Application states for the gui version
    """
    MAIN_MENU = 1
    SIGN_UP = 2
    LOGIN = 3
    GET_SERVICES = 4
    ADD_SERVICE = 5
    CHECK_SERVICE = 6
    UPDATE_SERVICE = 7
    DELETE_SERVICE = 8
    DELETE_ACCOUNT = 9
    LOGOFF = 10
    DISCONNECT = 11
