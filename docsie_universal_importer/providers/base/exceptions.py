class UniversalImporterError(Exception):
    """Base exception class."""


class ForbiddenError(UniversalImporterError):
    """Forbidden error."""


class NotFoundError(UniversalImporterError):
    """Not found."""


class UnauthorizedError(UniversalImporterError):
    """Unauthorized."""


class BadRequestError(UniversalImporterError):
    """Bad request."""
