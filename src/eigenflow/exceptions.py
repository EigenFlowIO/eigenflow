class EigenflowError(Exception):
    pass


class ValidationError(EigenflowError):
    pass


class ExtractionError(EigenflowError):
    pass


class ConfigurationError(EigenflowError):
    pass


class OperatorCompatibilityError(EigenflowError):
    """Raised when a graph/operator pairing is mathematically unsupported.

    The exception carries structured details so callers can convert an invalid
    pairing into an explicit analysis status rather than allowing downstream
    linear algebra to emit NaN/Inf values or opaque shape errors.
    """

    def __init__(self, operator, reason, message, **details):
        super().__init__(message)
        self.operator = operator
        self.reason = reason
        self.details = dict(details)

    def as_dict(self):
        return {
            "status": "incompatible",
            "operator": self.operator,
            "reason": self.reason,
            "message": str(self),
            **self.details,
        }
