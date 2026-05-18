import os
from pathlib import Path
from urllib.parse import urlencode


from dotenv import load_dotenv

from opencellid_downloader.utils import ensure_directory, extract_gzip_file

from opencellid_downloader.exceptions import InvalidMccError, MissingApiKeyError
from opencellid_downloader.downloader import download_file
from opencellid_downloader.countries import get_mcc_codes


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
            output_dir: str | Path = "data",
            filename: str | None = None,
            show_progress: bool = True,
            unzip: bool = False,
            keep_compressed: bool = True,
    ) -> Path:
        """ Download OpenCellID data for a specific MCC code.
        args:
            MCC: Mobile Country Code (3-digit code), for example 334 for Mexico.
            output_dir: Folder where the downloaded file will be saved. Defaults to "data".
            filename: Optional custom filename for the downloaded file.
            show_progress: Whether to display a progress bar during download. Defaults to True.
            unzip: Whether to extract the downloaded .csv.gz file.
            keep_compressed: Whether to keep the original .csv.gz file after extraction.

            returns:
            path to the downloaded file.
        """
        mcc_string = self._validate_mcc(mcc)
        url = self.build_mcc_download_url(mcc_string)

        output_directory = ensure_directory(output_dir)
        output_filename = filename or f"{mcc_string}.csv.gz"
        output_path = output_directory / output_filename

        downloaded_path = download_file(
            url=url,
            output_path=output_path,
            show_progress=show_progress,
        )

        if unzip:
            return extract_gzip_file(
                downloaded_path,
                keep_compressed=keep_compressed,
            )

        return downloaded_path

    def download_country(
            self,
            country: str,
            output_dir: str | Path = "data",
            show_progress: bool = True,
            unzip: bool = False,
            keep_compressed: bool = True,
    ) -> list[Path]:
        """ Download OpenCellID data for a specific country by name or alias.

        Args:
                country: Country name or alias, such as "Mexico", "MX", or "USA".
                output_dir: Folder where downloaded files should be saved. Defaults to "data".
                show_progress: Whether to display a tqdm progress bar during download.
                unzip: Whether to extract downloaded .csv.gz files.
                keep_compressed: Whether to keep original .csv.gz files after extraction.

        Returns:
            List of paths to the downloaded files for each MCC associated with the country.

        Raises:
            CountryNotFoundError: If the country name or alias is not recognized, valid or not supported.
            MissingApiKeyError: If the API key is missing, not set or not available.
            DownloadError: If there is an error during the download process, such as network issues or invalid responses.

        """
        mcc_codes = get_mcc_codes(country)

        downloaded_files = []

        for mcc in mcc_codes:
            download_file = self.download_mcc(
                mcc=mcc,
                output_dir=output_dir,
                show_progress=show_progress,
                unzip=unzip,
                keep_compressed=keep_compressed,
            )
            downloaded_files.append(download_file)

        return downloaded_files
