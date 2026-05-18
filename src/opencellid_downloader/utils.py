import gzip
import shutil
from pathlib import Path

from opencellid_downloader.exceptions import DownloadError


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if it does not exist and return it as a Path."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def extract_gzip_file(
    gzip_path: str | Path,
    output_path: str | Path | None = None,
    keep_compressed: bool = True,
) -> Path:
    """Extract a .gz file and return the extracted file path.

    Args:
        gzip_path: Path to the compressed .gz file.
        output_path: Optional custom path for the extracted file.
        keep_compressed: Whether to keep the original .gz file.

    Returns:
        Path to the extracted file.

    Raises:
        DownloadError: If the file cannot be extracted.
    """
    gzip_path = Path(gzip_path)

    if not gzip_path.exists():
        raise DownloadError(f"Cannot extract missing file: {gzip_path}")

    if gzip_path.suffix != ".gz":
        raise DownloadError(f"Expected a .gz file. Received: {gzip_path}")

    extracted_path = Path(
        output_path) if output_path else gzip_path.with_suffix("")
    extracted_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with gzip.open(gzip_path, "rb") as compressed_file:
            with open(extracted_path, "wb") as extracted_file:
                shutil.copyfileobj(compressed_file, extracted_file)

        if not keep_compressed:
            gzip_path.unlink()

        return extracted_path

    except (OSError, gzip.BadGzipFile) as error:
        if extracted_path.exists():
            extracted_path.unlink()

        raise DownloadError(f"Could not extract gzip file: {error}") from error
