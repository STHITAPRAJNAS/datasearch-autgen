class DatabaseError(Exception):
    """Base class for database related errors."""
    pass

class ApiError(Exception):
    """Base class for API related errors."""
    pass

class BedrockError(Exception):
    """Base class for Bedrock related errors."""
    pass

class ValidationError(Exception):
    """Base class for validation errors."""
    pass