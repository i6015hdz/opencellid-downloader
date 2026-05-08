from pathlib import Path

import requests
from tqdm import tqdm

from opencellid_downloader.exceptions import DownloadError


def download_file(
        url: str,
        output_path: str | Path,
        chunk_size: int = 1024 * 1024,  # 1 MB
        show_progress: bool = True,
        timeout: int = 30,
) -> Path:
    """ Download a file using streaming and save it on disk

        Args:
            url: The file URL to download.
            output_path: The path where the downloaded file will be saved.
            chunk_size: Number of bytes to read per chunk.
            show_progress: Whether to display a progress bar during download.
            timeout: Maximum time to wait for a response from the server, in seconds.

        Returns:
            The path to the downloaded file.

        Raises:
            DownloadError: If the download fails due to network issues or server errors.

    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = Path(str(output_path) + ".part")

    try:
        with requests.get(url, stream=True, timeout=timeout) as response:
            try:
                response.raise_for_status()
            except requests.HTTPError as error:
                raise DownloadError(
                    f"Download failed with status code {response.status_code}"
                ) from error

            total_size = int(
                response.headers.get("content-length")
                or response.headers.get("Content-Length")
                or 0
            )

            with open(temporary_path, "wb") as file:
                progressbar = tqdm(
                    total=total_size if total_size > 0 else None,
                    unit="B",
                    unit_scale=True,
                    desc=output_path.name,
                    disable=not show_progress,
                )

                with progressbar:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)
                            progressbar.update(len(chunk))

        temporary_path.replace(output_path)
        return output_path

    except requests.RequestException as error:
        if temporary_path.exists():
            temporary_path.unlink()

        raise DownloadError(f"Download request failed: {error}") from error

    except OSError as error:
        if temporary_path.exists():
            temporary_path.unlink()

        raise DownloadError(
            f"Could not write file to disk: {error}") from error
