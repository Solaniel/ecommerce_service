class ValidationErrors(Exception):
    def __init__(self, errors: list[dict]):
        self.errors = errors
        super().__init__("Validation failed")