class OIDCRequestParsingException(BaseException):
    """
    This exception is raised, when a parsing error occurs while parsing a OIDC request.
    """
    pass


class OIDCJWTException(BaseException):
    """
    This exception is raised during parsing or creating a JWT.
    """
    pass


class OIDCPKCEException(BaseException):
    """
    This exception is raised during the PKCE flow.
    """
    pass
