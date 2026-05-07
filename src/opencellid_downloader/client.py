class OpenCellIdClient:
    """Client for interacting with OpenCellID downloads."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
