from opencellid_downloader.utils import ensure_directory
from opencellid_downloader.exceptions import InvalidMccError, MissingApiKeyError
from opencellid_downloader.downloader import download_file
from dotenv import load_dotenv
import os
from pathlib import Path
from urllib.parse import urlencode


class OpenCellIdClient:
    """Client for interacting with OpenCellID downloads."""

    default_base_url = "https://opencellid.org/downloads.php"

    def __init__(
            self,
            api_key: str | None = None,
            base_url: str | None = None,
            load_env: bool = True,
    ):
        """ Create a new OpenCellIdClient instance.
        args:
            api_key: OpenCellID API access token. If not provided, the client
                     will try to read OPENCELLID_API_KEY from environment variables.
            base_url: Optional base URL for OpenCellID downloads. Defaults to the official
                     OpenCellID download URL. Also used for testing and advanced use.
            load_env: Whether to load environment variables from a .env file.
        """
        if load_env:
            load_dotenv()

        self.api_key = api_key or os.getenv("OPENCELLID_API_KEY")
        self.base_url = base_url or self.default_base_url

    def _require_api_key(self) -> str:
        """Return the API Key or raise an error if its missing."""
        if not self.api_key:
            raise MissingApiKeyError(
                "Missing OpenCellID API key."
                "Pass api_key='your_api_key' or set OPENCELLID_API_KEY in your .env file.")
        return self.api_key

    @staticmethod
    def _validate_mcc(mcc: int | str) -> str:
        """Validate and normalize the MCC code ."""
        mcc_string = str(mcc).strip()

        if not mcc_string.isdigit():
            raise InvalidMccError(f"MCC code must be numeric. Received: {mcc}")
        if len(mcc_string) != 3:
            raise InvalidMccError(
                f"MCC code must be a 3 digit number. Received: {mcc}")

        return mcc_string

    def build_mcc_download_url(self, mcc: int | str) -> str:
        """ Build the download URL for a specific MCC code."""
        api_key = self._require_api_key()
        mcc_string = self._validate_mcc(mcc)

        query_params = {
            "token": api_key,
            "type": "mcc",
            "file": f"{mcc_string}.csv.gz",
        }
        return f"{self.base_url}?{urlencode(query_params)}"

    def download_mcc(
            self,
            mcc: int | str,
            output_dir: str | Path = Path("data"),
            filename: str | None = None,
            show_progress: bool = True,
    ) -> Path:
        """ Download OpenCellID data for a specific MCC code.
        args:
            MCC: Mobile Country Code (3-digit code), for example 334 for Mexico.
            output_dir: Folder where the downloaded file will be saved. Defaults to "data".
            filename: Optional custom filename for the downloaded file.
            show_progress: Whether to display a progress bar during download. Defaults to True.

            returns:
            path to the downloaded file.
        """
        mcc_string = self._validate_mcc(mcc)
        url = self.build_mcc_download_url(mcc_string)

        output_directory = ensure_directory(output_dir)
        output_filename = filename or f"{mcc_string}.csv.gz"
        output_path = output_directory / output_filename

        return download_file(
            url=url,
            output_path=output_path,
            show_progress=show_progress,
        )
