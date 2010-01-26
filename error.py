class GameError(Exception): pass
class IllegalMovement(GameError): pass
class FocusError(GameError): pass
class AlreadyFocusedError(GameError): pass
class NotFocusedError(GameError): pass
