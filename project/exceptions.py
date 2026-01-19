from typing import Any


class ServiceError(Exception):
    """Base exception for service layer errors."""

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.context = context or {}
        super().__init__(message)


class EntityNotFoundError(ServiceError):
    """Raised when a required entity is not found."""

    def __init__(
        self,
        entity_type: str,
        identifier: str | None = None,
    ) -> None:
        self.entity_type = entity_type
        self.identifier = identifier

        message = f"{entity_type} not found"
        if identifier:
            message += f": {identifier}"

        context = {"entity_type": entity_type}
        if identifier:
            context["identifier"] = identifier

        super().__init__(message, context)


class ValidationError(ServiceError):
    """Raised when validation fails."""

    def __init__(
        self,
        message: str,
        field: str | None = None,
    ) -> None:
        self.field = field
        context = {}
        if field:
            context["field"] = field
        super().__init__(message, context)


class AuthenticationError(ServiceError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message)


class AuthorizationError(ServiceError):
    """Raised when user lacks permission."""

    def __init__(
        self,
        message: str = "Not authorized",
        required_role: str | None = None,
    ) -> None:
        self.required_role = required_role
        context = {}
        if required_role:
            context["required_role"] = required_role
        super().__init__(message, context)
