class OpenCellIdDownloaderError(Exception):
    """Base exception for OpenCellID Downloader errors."""


class MissingApiKeyError(OpenCellIdDownloaderError):
    """Raised when an API key is required but missing."""


class CountryNotFoundError(OpenCellIdDownloaderError):
    """Raised when a country cannot be matched to an MCC code."""


class DownloadError(OpenCellIdDownloaderError):
    """Raised when a download fails."""
