class Error(Exception):
    """Base class for custom exceptions"""
    pass


class HtmlParsingError(Error):
    """Raised when the process of parsing the HTML goes wrong"""
    pass


class ConnectionRejectError(Error):
    """Raised when the HTTP connection is not possible"""
    pass
