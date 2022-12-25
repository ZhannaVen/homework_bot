class NotForSending(Exception):
    """Answers are not for forwarding."""
    pass


class EmptyAPIReply(NotForSending):
    """Received an empty response from the API."""
    pass


class InvalidTokens(NotForSending):
    """Error in environment variables."""
    pass


class InvalidResponseCode(Exception):
    """Invalid server response code."""
    pass
